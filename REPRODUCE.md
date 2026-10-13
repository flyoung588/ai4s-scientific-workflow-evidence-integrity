# Reproduction instructions

**Release state: human-approved public technical case. Unified package clean-run result: PASS_SCOPED_ENGINEERING_ACCEPTANCE.**

The actual reference receipt is [results/reference-run/summary.json](results/reference-run/summary.json), produced on 2026-10-13 from 05:19:09 to 05:19:28 UTC. This is a local producer run, not third-party replication.

## Environment and complete entrypoint

Use a fresh directory and Python 3.11.12 if matching the historical local environment. macOS/POSIX was exercised; Windows and cross-platform equivalence were not. A virtual environment must not inherit system packages. The complete requirements file preserves the 48 pinned entries from the prior CWL integration environment. The component-only file preserves its 19 pinned entries. Package pins reproduce that environment; they are not a supply-chain or vulnerability audit.

From the package root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tests/run_acceptance.py --out results-new --native
```

`results-new` must not already exist. Preserve a failed run in place and use another directory for a justified retry. The entrypoint checks the sixteen original component expectations, ten retained baseline checks and six CWL scenario expectations, then adjudicates saved CWL evidence. With `--native`, it also executes the numerical-failure scenario to inspect native provenance and manifests. A successful acceptance exit means the expected observations were obtained, including expected workflow rejection and known bad-baseline behavior. These are overlapping controls within synthetic studies, not independent scientific experiments.

Inspect `results-new/summary.json`, `process-events.json`, `environment.json` and `hashes.json`, plus the individual `*.receipt.json` files. Substudy evidence is under `components/`, `baseline/` and `cwl/`; saved-evidence adjudication is `cwl-adjudication.json`; the native audit is `native/audit/audit.json`. The retained reference run uses the same structure under `results/reference-run/`. The summary binds the runner and frozen-contract hashes. The environment identity covers only its declared OS, Python and package fields. Preserve the original output bytes; do not rewrite embedded temporary paths to make a receipt appear portable.

## Component-only route

This runs the sixteen component expectations and ten baseline checks, without the CWL integration or native provenance audit:

```sh
python3 -m venv .venv-components
.venv-components/bin/python -m pip install -r requirements-components.txt
.venv-components/bin/python tests/run_acceptance.py --out results-components-new --components-only
```

Read `results-components-new/summary.json`, `components/summary.json`, each component `C01_...json` through `C16_...json`, and `baseline/summary.json`. The original evaluator and worker in `baseline/` contain intentional retained weaknesses; they must not be used as production scientific validators. Raw subprocess receipts, span exports, databases, original and tampered crates, and hashes are part of the evidence.

## CWL route and saved-evidence adjudication

This is an alternative source-level route when inspecting the original CWL study separately; it is not required after the complete entrypoint. With the complete environment installed:

```sh
.venv/bin/python src/cwl/run_case.py --out results-cwl-new
.venv/bin/python src/cwl/verify_existing.py --run results-cwl-new --out results-cwl-adjudication-new.json
```

The second command reads saved evidence and does not rerun the workflow. Each scenario has `job.json`, `run.receipt.json`, `expectation.json`, `outputs/` and retained `tmp/` artifacts. Five scenarios produce `outputs/bundle/`; `checkpoint-corrupt` should stop at the resume guard with no downstream bundle. Its failed receipt remains under `tmp/`.

The runner gives each workflow 45 seconds, the checkpoint handshake 5 seconds, and the side effect at most two attempts. Slow-host timeouts are execution failures to investigate, not scientific negatives. Keep the actual timeout evidence. Do not regenerate the workflow definitions with `--generate` during review: the candidate preserves their existing bytes.

## Native provenance audit

The complete command includes this audit through `--native`. It executes the numerical-failure scenario once more with native provenance enabled; that is an evidence-format check, not another independent experiment. The entrypoint removes `ORCID`, `CWL_FULL_NAME`, `CWLTOOL_OPTIONS` and `PYTHONPATH` from child environments and disables user/host provenance.

For source-level inspection instead of the complete entrypoint, the commands below follow the separate CWL route. Ensure the same environment variables are unset; do not rerun them merely to increase execution counts:

```sh
mkdir -p native-new/outputs native-new/tmp
.venv/bin/cwltool --no-container --leave-tmpdir --no-doc-cache --disable-user-provenance --disable-host-provenance --provenance native-new/provenance --outdir native-new/outputs --tmp-outdir-prefix native-new/tmp/ src/cwl/workflow/workflow.cwl results-cwl-new/numerical-failure/job.json
.venv/bin/python src/cwl/audit_native.py --bag native-new/provenance --out native-audit-new --boundary native-new/outputs/bundle/boundary.json
```

Inspect `results-new/native/audit/audit.json` for the complete command, or `native-audit-new/audit.json` for the manual route: original manifest validation should pass and the equal-length corrupted copy should be rejected. The retained reference audit observes both conditions. The retained boundary should still report a failed synthetic numerical evaluation. PROV may use qualified usage/generation relationships; zero direct `prov:used` links alone is not proof of missing provenance. Native payload manifests use SHA1 in the recorded configuration; this is not an authentication or malicious-collision-resistance qualification.

## Interpreting errors and preserving evidence

The expected checkpoint child exit is `-15` after actual SIGTERM; its wrapper can still complete the declared controlled-interruption stage. The corrupt-checkpoint guard exits `22`, leading to a nonzero CWL workflow exit. A committed side effect returns `75` to simulate a lost acknowledgement, then `0` on retry. A numerical failure is preserved as data despite normal process exit. Consult the matrix before calling any of these a reproduction failure.

The package's calculations do not need a network, but native execution and `NetworkAccess:false` are not a verified network-isolation boundary. No container daemon, cluster, model or instrument is started by these instructions. Generated receipts can include local paths and environment details; review actual output bytes before any future publication. Raw failures must remain available locally even if a public subset later needs redaction.


Publication note: human approval now permits this personal technical case and Apache-2.0 original reproduction code. Historical preparation fields are retained as history. Working-group adoption and independent third-party replication remain unproven.
