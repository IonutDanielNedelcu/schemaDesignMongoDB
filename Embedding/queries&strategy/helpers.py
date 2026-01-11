import time

def timeQuery(collection, query, name="Query", limit=None, projection=None, sort=None, hint=None):
    # Time a query execution and return results (elapsed in ms)
    start = time.time()
    cursor = collection.find(query, projection)
    if sort:
        cursor = cursor.sort(sort)
    if hint:
        cursor = cursor.hint(hint)
    if limit:
        cursor = cursor.limit(limit)
    results = list(cursor)  # Force execution
    elapsed = (time.time() - start) * 1000  # ms
    print(f"{name}: {elapsed:.2f}ms ({len(results)} documents)")
    return results, elapsed

def timeAggregation(collection, pipeline, name="Aggregation"):
    # Time an aggregation pipeline
    start = time.time()
    results = list(collection.aggregate(pipeline))
    elapsed = (time.time() - start) * 1000
    print(f"{name}: {elapsed:.2f}ms ({len(results)} documents)")
    return results, elapsed

def explainQuery(collection, query, projection=None, sort=None, hint=None):
    # Get detailed explain plan for a query
    cursor = collection.find(query, projection)
    if sort:
        cursor = cursor.sort(sort)
    if hint:
        cursor = cursor.hint(hint)
    explain = cursor.explain()
    return explain

def printExplainSummary(explain):
    # Print a readable summary of explain output
    if 'executionStats' in explain:
        stats = explain['executionStats']
        print()
        print(f"Execution Stats:")
        print(f"Execution time: {stats.get('executionTimeMillis', 0)}ms")
        print(f"Documents examined: {stats.get('totalDocsExamined', 0):,}")
        print(f"Documents returned: {stats.get('nReturned', 0):,}")
        
        examined = stats.get('totalDocsExamined', 0)
        returned = stats.get('nReturned', 0)
        if examined > 0:
            ratio = returned / examined
            print(f"Efficiency ratio: {ratio:.2%}")
            if ratio < 0.1:
                print("!!! LOW EFFICIENCY - Consider adding an index!")
    
    if 'queryPlanner' in explain:
        planner = explain['queryPlanner']
        winningPlan = planner.get('winningPlan', {})
        stage = winningPlan.get('stage', 'UNKNOWN')
        
        print()
        print(f"Query Plan:")
        print(f"    Stage: {stage}")
        
        if stage == 'COLLSCAN':
            print("!!! COLLECTION SCAN - No index used!")
        elif 'inputStage' in winningPlan:
            inputStage = winningPlan['inputStage']
            if 'indexName' in inputStage:
                print(f"    Using index: {inputStage['indexName']}")

