import os
import json
import random
import hashlib
from datetime import datetime, timedelta
from bisect import bisect_right
from statistics import mean, pstdev


JSON_DIR = os.path.join(os.path.dirname(__file__), "JsonOrders")


def load_documents(max_docs=10000):
    docs = []
    files = sorted([f for f in os.listdir(JSON_DIR) if f.endswith('.json')])
    for fname in files:
        path = os.path.join(JSON_DIR, fname)
        with open(path, 'r', encoding='utf-8') as fh:
            arr = json.load(fh)
            for d in arr:
                docs.append(d)
                if len(docs) >= max_docs:
                    return docs
    return docs


def hashed_shard(key, num_shards):
    if key is None:
        key = ''
    h = hashlib.md5(str(key).encode('utf-8')).hexdigest()
    return int(h, 16) % num_shards


def ranged_shard(value_ts, boundaries):
    # boundaries: sorted list of upper-bound timestamps for each shard except last
    return bisect_right(boundaries, value_ts)


def compute_boundaries(timestamps, num_shards):
    timestamps = sorted(timestamps)
    n = len(timestamps)
    boundaries = []
    for i in range(1, num_shards):
        idx = int(i * n / num_shards)
        boundaries.append(timestamps[idx])
    return boundaries


def analyze_distribution(assignments, num_shards):
    counts = [0] * num_shards
    for s in assignments:
        counts[s] += 1
    avg = mean(counts)
    sd = pstdev(counts) if len(counts) > 1 else 0.0
    imbalance = max(counts) / min([c for c in counts if c > 0]) if min([c for c in counts if c > 0])>0 else float('inf')
    return {'counts': counts, 'avg': avg, 'stddev': sd, 'max': max(counts), 'min': min(counts), 'imbalance_ratio': imbalance}


def simulate(docs, num_shards=4, sample_queries=200):
    # pick shard keys
    customer_keys = []
    date_ts = []
    for d in docs:
        cid = None
        try:
            cid = d.get('customerSnapshot', {}).get('_id')
        except Exception:
            cid = None
        customer_keys.append(cid)
        od = d.get('orderDate')
        try:
            ts = datetime.fromisoformat(od).timestamp()
        except Exception:
            ts = 0.0
        date_ts.append(ts)

    # hashed on customer id
    hashed_assign = [hashed_shard(k, num_shards) for k in customer_keys]
    hashed_stats = analyze_distribution(hashed_assign, num_shards)

    # ranged on orderDate
    boundaries = compute_boundaries(date_ts, num_shards)
    ranged_assign = [ranged_shard(ts, boundaries) for ts in date_ts]
    ranged_stats = analyze_distribution(ranged_assign, num_shards)

    # query simulations
    # point lookups by customer id: pick sample customer ids (existing)
    existing_customers = [k for k in set(customer_keys) if k is not None]
    point_samples = random.sample(existing_customers, min(sample_queries, len(existing_customers)))

    hashed_point_shards = []
    ranged_point_shards = []
    for cid in point_samples:
        # which shards contain documents for this customer
        indices = [i for i, k in enumerate(customer_keys) if k == cid]
        shards_h = set(hashed_assign[i] for i in indices)
        shards_r = set(ranged_assign[i] for i in indices)
        hashed_point_shards.append(len(shards_h))
        ranged_point_shards.append(len(shards_r))

    # range queries on dates: pick random windows
    min_ts, max_ts = min(date_ts), max(date_ts)
    window_seconds = 7 * 24 * 3600  # 7 days
    range_samples = []
    ranged_query_shards = []
    hashed_query_shards = []
    for _ in range(min(sample_queries, 200)):
        start = random.uniform(min_ts, max_ts - window_seconds)
        end = start + window_seconds
        # documents matching
        idxs = [i for i, ts in enumerate(date_ts) if start <= ts <= end]
        if not idxs:
            continue
        shards_h = set(hashed_assign[i] for i in idxs)
        shards_r = set(ranged_assign[i] for i in idxs)
        hashed_query_shards.append(len(shards_h))
        ranged_query_shards.append(len(shards_r))

    result = {
        'num_docs': len(docs),
        'num_shards': num_shards,
        'hashed_stats': hashed_stats,
        'ranged_stats': ranged_stats,
        'hashed_point_avg_shards': mean(hashed_point_shards) if hashed_point_shards else 0,
        'ranged_point_avg_shards': mean(ranged_point_shards) if ranged_point_shards else 0,
        'hashed_range_avg_shards': mean(hashed_query_shards) if hashed_query_shards else 0,
        'ranged_range_avg_shards': mean(ranged_query_shards) if ranged_query_shards else 0,
    }
    return result


def main():
    print('Loading documents (sample)...')
    docs = load_documents(max_docs=5000)
    print(f'Loaded {len(docs)} documents')
    res = simulate(docs, num_shards=4, sample_queries=200)
    print('\n=== Sharding Simulation Summary ===')
    print(f"Documents: {res['num_docs']}, Shards: {res['num_shards']}")
    print('\n-- Hashed on customer _id distribution --')
    print(res['hashed_stats'])
    print('\n-- Ranged on orderDate distribution --')
    print(res['ranged_stats'])
    print('\n-- Query routing (avg number of shards touched) --')
    print(f"Point lookup (hashed): {res['hashed_point_avg_shards']:.2f} shards")
    print(f"Point lookup (ranged): {res['ranged_point_avg_shards']:.2f} shards")
    print(f"Range query 7-day (hashed): {res['hashed_range_avg_shards']:.2f} shards")
    print(f"Range query 7-day (ranged): {res['ranged_range_avg_shards']:.2f} shards")


if __name__ == '__main__':
    main()
