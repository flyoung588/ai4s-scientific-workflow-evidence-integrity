#!/usr/bin/env python3
"""Synthetic interruption/cache fixture. Standard library only; no cluster/LLM.

Run: python3 case.py --out NEW_DIRECTORY
Outputs are deliberately small; input, process, checkpoint and verdict are separate.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def write(p, obj):
    Path(p).write_text(json.dumps(obj, sort_keys=True, indent=2) + '\n')

def worker(a):
    src = Path(a.input)
    d = json.loads(src.read_text())
    binding = {'input_sha256': digest(src), 'code_sha256': digest(__file__)}
    i, x = 0, d['x0']
    if a.resume:
        cp = json.loads(Path(a.resume).read_text())
        if cp['binding'] != binding and not a.unsafe:
            print('CHECKPOINT_BINDING_REJECTED', flush=True)
            return 22
        i, x = cp['i'], cp['x']
    while i < len(d['data']):
        x = (d['a'] * x + d['data'][i]) % d['modulus']
        i += 1
        if a.interrupt_at == i:
            write(a.checkpoint, {'i': i, 'x': x, 'binding': binding,
                                'experiment': a.experiment, 'producer_attempt': a.attempt})
            print('CHECKPOINT_DURABLE', flush=True)
            # Parent sends SIGTERM after observing this actual checkpoint.
            while True:
                time.sleep(1)
    write(a.result, {'value': x, 'input_sha256': digest(src),
                     'experiment': a.experiment, 'attempt': a.attempt})
    return 0

def run_case(out):
    out.mkdir(parents=True, exist_ok=False)
    data = {'a': 3, 'x0': 7, 'modulus': 997, 'data': list(range(1, 21))}
    write(out / 'input.json', data)
    write(out / 'evaluation-contract.json', {
        'origin': 'SYNTHETIC_FIXTURE', 'claim': 'integer recurrence final value',
        'criterion': 'exact integer equality with independently implemented closed form',
        'supported_scope': 'only this deterministic numerical fixture',
        'excluded': ['physical science', 'statistical independence', 'scientific discovery',
                     'Argo deployment', 'OpenTelemetry deployment', 'Kubernetes DRA deployment'],
        'evaluator': 'evaluate.py', 'evaluator_sha256': digest(Path(__file__).with_name('evaluate.py'))})
    events = []
    def invoke(name, inp='input.json', resume=None, unsafe=False, interrupt=False, experiment='experiment-A'):
        args = [sys.executable, str(Path(__file__).resolve()), '--worker',
                '--input', str(out / inp), '--result', str(out / (name + '.result.json')),
                '--experiment', experiment, '--attempt', name]
        if resume:
            args += ['--resume', str(out / resume)]
        if unsafe:
            args += ['--unsafe']
        if interrupt:
            args += ['--interrupt-at', '8', '--checkpoint', str(out / 'checkpoint.json')]
        started = time.time()
        if interrupt:
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            # Worker emits one line only after writing and closing the checkpoint.
            first = p.stdout.readline()
            if first.strip() != 'CHECKPOINT_DURABLE':
                p.kill()
                raise RuntimeError('checkpoint handshake failed')
            p.terminate()
            stdout, stderr = p.communicate(timeout=10)
            stdout = first + stdout
            rc = p.returncode
        else:
            p = subprocess.run(args, capture_output=True, text=True, timeout=10)
            stdout, stderr, rc = p.stdout, p.stderr, p.returncode
        e = {'attempt': name, 'experiment': experiment, 'command': args,
             'started_unix': started, 'exit_code': rc, 'stdout': stdout, 'stderr': stderr,
             'input_sha256': digest(out / inp), 'resume_checkpoint_sha256': digest(out / resume) if resume else None,
             'result_sha256': digest(out / (name + '.result.json')) if (out / (name + '.result.json')).exists() else None}
        events.append(e)
        return rc

    assert invoke('attempt-1', interrupt=True) == -15
    assert invoke('attempt-2', resume='checkpoint.json') == 0
    assert invoke('fresh-run', experiment='experiment-B-clean-recomputation') == 0
    v = json.loads((out / 'attempt-2.result.json').read_text())['value']
    f = json.loads((out / 'fresh-run.result.json').read_text())['value']
    changed = dict(data, a=4)
    write(out / 'changed-input.json', changed)
    assert invoke('changed-resume-rejected', inp='changed-input.json', resume='checkpoint.json') == 22
    assert invoke('changed-fresh', inp='changed-input.json', experiment='experiment-C-changed') == 0
    assert invoke('changed-unsafe-resume', inp='changed-input.json', resume='checkpoint.json', unsafe=True,
                  experiment='experiment-C-changed') == 0
    # A deliberately incomplete cache key ignores a, data and code.
    bad_key = lambda d: str(len(d['data']))
    good_key = lambda inp: hashlib.sha256(json.dumps({
        'input': digest(out / inp), 'code': digest(__file__),
        'python': platform.python_version(), 'platform': platform.platform(),
        'protocol': 'integer-recurrence-v1'}, sort_keys=True).encode()).hexdigest()
    write(out / 'cache-entry.json', {'bad_key': bad_key(data), 'good_key': good_key('input.json'),
                                   'producer_attempt': 'attempt-2', 'output_sha256': digest(out / 'attempt-2.result.json')})
    write(out / 'cache-reuse.json', {'source': 'attempt-2.result.json', 'producer_attempt': 'attempt-2',
                                  'cache_hit': True, 'new_simulation_execution': False,
                                  'input_sha256': digest(out / 'input.json'), 'value': v})
    def evaluate(name, inp, result):
        args = [sys.executable, str(Path(__file__).with_name('evaluate.py')), str(out / inp), str(out / result)]
        r = subprocess.run(args, capture_output=True, text=True, timeout=10)
        write(out / (name + '.evaluation.json'), {'command': args, 'exit_code': r.returncode,
                                                 'stdout': r.stdout, 'stderr': r.stderr,
                                                 'evaluator_sha256': digest(Path(__file__).with_name('evaluate.py'))})
        return json.loads(r.stdout), r.returncode
    pos, prc = evaluate('resumed', 'input.json', 'attempt-2.result.json')
    cached, crc = evaluate('cached', 'input.json', 'cache-reuse.json')
    stale, src = evaluate('stale-cache', 'changed-input.json', 'cache-reuse.json')
    unsafe, urc = evaluate('unsafe-resume', 'changed-input.json', 'changed-unsafe-resume.result.json')
    missing, mrc = evaluate('missing', 'input.json', 'does-not-exist.json')
    checks = {'real_process_interruption': events[0]['exit_code'] == -15,
              'resumed_matches_clean': v == f, 'resumed_passes_closed_form': prc == 0,
              'cached_value_passes_but_is_not_new_execution': crc == 0,
              'coarse_cache_key_collides': bad_key(data) == bad_key(changed),
              'complete_declared_key_changes': good_key('input.json') != good_key('changed-input.json'),
              'stale_cache_fails_current_evaluation': src == 1,
              'changed_checkpoint_binding_rejected': events[3]['exit_code'] == 22,
              'unsafe_resume_completes_but_fails_evaluation': events[5]['exit_code'] == 0 and urc == 1,
              'missing_result_is_not_evaluated': missing['status'] == 'NOT_EVALUATED' and mrc == 2}
    write(out / 'process-events.json', events)
    write(out / 'summary.json', {'checks': checks, 'passed': sum(checks.values()), 'total': len(checks),
                                'values': {'resumed': v, 'fresh': f, 'stale_cache_evaluation': stale,
                                           'unsafe_resume_evaluation': unsafe},
                                'origin': 'SYNTHETIC_FIXTURE', 'tool_execution': 'REAL_LOCAL_SUBPROCESSES',
                                'independence': 'different evaluator implementation; same author, same fixture, no external independent review',
                                'cost': 'NO_ADDITIONAL_PAID_API_OR_CLOUD', 'scientific_claim': 'NOT_EVALUATED'})
    write(out / 'artifact-hashes.json', {p.name: digest(p) for p in sorted(out.glob('*.json'))})
    print(json.dumps({'passed': sum(checks.values()), 'total': len(checks), 'out': str(out)}, indent=2))
    return 0 if all(checks.values()) else 1

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--worker', action='store_true')
    p.add_argument('--out')
    p.add_argument('--input'); p.add_argument('--result'); p.add_argument('--resume')
    p.add_argument('--unsafe', action='store_true'); p.add_argument('--interrupt-at', type=int)
    p.add_argument('--checkpoint'); p.add_argument('--experiment'); p.add_argument('--attempt')
    a = p.parse_args()
    sys.exit(worker(a) if a.worker else run_case(Path(a.out)))
