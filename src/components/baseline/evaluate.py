#!/usr/bin/env python3
"""Independent algorithm, not independent author/reviewer; synthetic exact oracle."""
import json
from pathlib import Path
import sys
def evaluate(inp, result):
    if not Path(result).exists():
        return {'status': 'NOT_EVALUATED', 'reason': 'RESULT_UNAVAILABLE'}, 2
    d = json.loads(Path(inp).read_text())
    r = json.loads(Path(result).read_text())
    n, m, a = len(d['data']), d['modulus'], d['a']
    expected = (pow(a, n, m) * d['x0'] + sum(pow(a, n-i-1, m) * x for i, x in enumerate(d['data']))) % m
    ok = r['value'] == expected
    return {'status': 'SUPPORTED' if ok else 'FAILED', 'expected': expected,
            'observed': r['value'], 'scope': 'integer recurrence equality only'}, 0 if ok else 1
if __name__ == '__main__':
    obj, rc = evaluate(*sys.argv[1:])
    print(json.dumps(obj, sort_keys=True))
    sys.exit(rc)
