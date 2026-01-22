import json
import os
from json import JSONDecodeError

def loadJsonFile(path):
    if not isinstance(path, str):
        raise ValueError('path must be a string')
    if not os.path.isabs(path):
        # allow workspace-relative paths
        path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(path):
        raise FileNotFoundError(f'File not found: {path}')
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except JSONDecodeError as e:
            raise ValueError(f'Invalid JSON in file {path}: {e}')
    if not isinstance(data, (dict, list)):
        raise ValueError('JSON must be an object or an array')
    return data
