# Scientific Workflow Evidence Integrity: A Reproducible Failure-Injection Case Study

**Public personal technical case v1.0.0 — external review pending. Original reproduction code: Apache-2.0.**

This package demonstrates a narrow problem: a workflow can complete, produce the expected number, and package its artifacts while its evidence is unsuitable for the intended claim. The examples make those boundaries observable with synthetic inputs and actual local software components.

Start here. [CASE_STUDY.md](CASE_STUDY.md) explains the example; [REPRODUCE.md](REPRODUCE.md) provides the commands; [EVIDENCE_MATRIX.md](EVIDENCE_MATRIX.md) maps every control to its evidence and limits. [REVIEWER_GUIDE.md](REVIEWER_GUIDE.md) identifies the small set of claims worth challenging. [§4.4 proposal](whitepaper/SECTION_4_4_PROPOSAL.md) and [§5 case study](whitepaper/SECTION_5_CASE_STUDY.md) provide separate short texts for working-group review.

## What is included

| Location | Purpose |
|---|---|
| `src/components/research.py` | Sixteen component expectations, including deliberately successful bad implementations and observed failures |
| `src/components/baseline/` | Original synthetic worker, evaluator and checkpoint bytes, plus ten retained baseline checks; known defects remain for negative controls |
| `src/cwl/worker.py`, `evaluator.py` | The checkpoint/resume/evaluation/package tools and a separate arithmetic implementation |
| `src/cwl/run_case.py`, `workflow/` | Six actual local CWL workflow scenarios |
| `src/cwl/verify_existing.py` | Read-only adjudication from retained result bytes, receipts, hashes and SQLite rows |
| `src/cwl/audit_native.py` | Native PROV/BagIt inspection and an explicitly corrupted copy |
| `tests/run_acceptance.py` | Standard-library entrypoint for the preserved studies and saved-evidence adjudication |
| `fixtures/acceptance-contract.json` | Frozen expectation identifiers, key numerical values and scope |
| `results/reference-run/` | Original bytes from this package’s isolated local acceptance run |
| `requirements.txt` | Complete pinned environment, including CWL and native-provenance audit dependencies |
| `requirements-components.txt` | Smaller pinned environment for component and baseline checks |

The source modules and synthetic baseline are copied unchanged from the recorded studies. The acceptance entrypoint is additional packaging code; it does not turn their verdicts into scientific approval. No fetched source-document archive or private research material is part of this candidate.

## Reproduce the complete acceptance set

From the package root, with an unused output directory:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tests/run_acceptance.py --out results-new --native
```

The unified entrypoint completed in a fresh isolated Python 3.11.12 environment on 2026-10-13, 05:19:09–05:19:28 UTC, with `PASS_SCOPED_ENGINEERING_ACCEPTANCE`. Its [receipt](results/reference-run/summary.json) records all frozen checks as true: the original sixteen component expectations, ten baseline checks, six CWL scenarios, read-only byte/database adjudication and native PROV/BagIt audit. These are checks of controlled behavior, including expected failures; they are not counts of independent experiments or scientific discoveries.

The tested historical configuration was Python 3.11.12 on macOS/POSIX. Dependency installation uses the network; the fixture calculations require no model, cloud account or paid API. Native execution is not an operating-system sandbox. The tests deliberately terminate their own subprocesses and write local SQLite files, so run them only in a fresh working directory after reading the source.

## Claim ceiling

The package uses four local review levels, not an external certification scheme: **L1** software behavior under enumerated controls; **L2** retained local bytes and application relationships, without authentication; **L3** an exact synthetic integer criterion; **L4** independent third-party replication, **NOT_PERFORMED**. A different algorithm or clean environment does not establish independent authorship, new data, causality or scientific discovery.

Caching is exercised only in CPython's `lru_cache` component control and the retained local baseline context. The CWL integration does not test CWL caching or deploy Argo memoization. Retry is implemented by Tenacity inside a tool; it is not a workflow-controller retry experiment. CWL and BagIt are supporting technologies, not represented as CNCF projects. Argo/Kubernetes deployment and distributed storage durability remain unverified.

Prepared with substantial AI assistance for Fei Yang's technical review. No working-group adoption, authorship, institutional affiliation or deployment is implied. The human publication gate approved Apache-2.0 for the original reproduction code; see [license scope](LICENSE_SCOPE.md).

Release evidence: [internal independent QA](evidence/INTERNAL_INDEPENDENT_QA.json), [release status](RELEASE_STATUS.json), [rights and license status](LICENSE_CANDIDATE.md). Internal clean reproduction is completed; independent third-party replication has not occurred. Historical HOLD fields in retained evidence describe the prepublication stage; current publication is human-approved. This repository is not an official CNCF project or endorsement.
