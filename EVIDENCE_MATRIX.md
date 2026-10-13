# Evidence matrix

This is the expected interpretation of the frozen controls. The new unified entrypoint’s retained reference receipt reports **PASS_SCOPED_ENGINEERING_ACCEPTANCE** on 2026-10-13; its original observations are under `results/reference-run/`. `expectation_met=true` may mean that a deliberately defective baseline accepted invalid evidence. It must not be relabeled as a scientific pass.

## Review levels

| Level | What a matching observation establishes | What it does not establish |
|---|---|---|
| L1 — software behavior | Actual local components produce the enumerated observations, including deliberate failures | General reliability, deployment readiness or scientific correctness |
| L2 — local bytes and relationships | Specified digests/manifests and declared experiment/input/attempt/effect/evaluation links satisfy local checks or detect controlled faults | Authentication, trusted issuer, complete causal provenance, complete checkpoint state or scientific independence |
| L3 — fixture evaluation | An integer result matches or fails an explicitly synthetic closed-form oracle | Real-domain validity, new knowledge, causal or generalization claims |
| L4 — independent third-party replication | NOT_PERFORMED | No external reproduction, scientific validation, adoption or discovery may be inferred |

These levels are local documentation conventions, not names of a community standard or a certification ladder.

## Sixteen component expectations

The component output directory contains a JSON file beginning with each ID below and a `summary.json` retaining the complete identifiers and observations.

| ID | Actual control and expected observation | Primary retained evidence | Level/limit |
|---|---|---|---|
| C01 | Old evaluator accepts value 767 with foreign experiment/input metadata | `old-evaluator-foreign.process.json`, `foreign-result.json` | L3 value alone; L2 deficiency intentionally observed |
| C02 | Added local binding guard rejects the foreign result | `C02_binding_guard_rejects_foreign.json` | L2; unsigned local contract |
| C03 | Different input bytes yield the same number; old evaluator accepts, binding guard rejects | `aliased-input.json`, `old-evaluator-alias.process.json` | L2 is not implied by numerical equality |
| C04 | Mutated checkpoint state resumes with process exit 0 but fails arithmetic; byte guard identifies mutation | `corrupted-checkpoint.json`, `old-corrupted-evaluation.process.json` | L2/L3; baseline flaw, not a platform defect |
| C05 | Old worker permits a new experiment label on a continuation; guard rejects silent relabeling | `relabeled-result.json`, `old-relabeled-checkpoint.process.json` | L2; changing identity is not independence |
| C06 | Full Python RNG state continues the stream; seed-only restart does not | `rng-state.json`, `C06_rng_continuity_requires_rng_state.json` | Local RNG only; no GPU/distributed state claim |
| C07 | Cache omits changed coefficient and returns 21; explicit dependency returns 28 | `C07_real_lru_cache_hidden_dependency.json` | CPython `lru_cache`; no CWL/Argo cache execution |
| C08 | Commit then lost acknowledgement yields two unsafe rows versus one keyed row | `retry.db`, `C08_retry_repeats_committed_effect.json` | Local Tenacity/SQLite idempotency only |
| C09 | A returned scientific failure does not trigger an OSError retry policy | `C09_scientific_failure_does_not_trigger_exception_retry.json` | One actual call; execution policy differs from evaluation |
| C10 | SIGKILL before SQLite commit leaves the previous state `(8,123)` | `crash.db`, `C10_sqlite_uncommitted_crash_recovery.json` | Process-crash rollback; not power-loss durability |
| C11 | `ALWAYS_OFF` exports no span | `otel-off.spans.json` | Actual in-memory SDK sampling |
| C12 | Retained span status `OK` coexists with a failed domain verdict | `otel-on.spans.json` | Instrumentation status is not domain evaluation |
| C13 | A retained span loses its evidence attribute under a two-attribute limit | `otel-limited.spans.json`, C13 record | L2 link loss; dropped-attribute count is retained |
| C14 | RO-Crate serializes/reloads a foreign-bound result that the application rejects | `crate/`, C14 record | Library loading, not complete profile validation |
| C15 | Mutated crate input still reloads; external digest differs | `crate-tampered/`, C15 record | L2 digest check is separate from this read operation |
| C16 | Three actual evaluations lead to three different controlled dispositions | `adaptive-transitions.json` | Bounded interface; allocation effect NONE |

## Ten preserved baseline checks

These provide regression context and overlap the later controls; they are not ten additional scientific experiments. Inspect `baseline/summary.json`, `baseline/process-events.json` and `baseline/artifact-hashes.json` under the reference run.

| Check group | Frozen observation |
|---|---|
| Interruption, resumed/fresh agreement, arithmetic evaluation | Actual SIGTERM; resumed = fresh = 767; original fixture evaluates correctly |
| Cached value and declared identity | Cached 767 still passes the old numerical criterion but is not a new execution; the coarse key collides while the declared dependency key changes |
| Changed coefficient and checkpoint guard | Fresh expected value is 623; stale cache remains 767; changed binding is rejected |
| Unsafe continuation | Bypassed guard finishes normally with value 38, which fails against 623 |
| Missing result | `NOT_EVALUATED`, distinct from a failed numerical result |

The baseline marker named `CHECKPOINT_DURABLE` is not proof of durable storage; that implementation writes and closes before the process interruption. Later controls deliberately demonstrate deficiencies remaining in this baseline.

## Six CWL scenario expectations

For every scenario, inspect its `run.receipt.json`, `expectation.json`, retained temporary files and actual output artifacts. `verify_existing.py` additionally reads the result, report, effect database and artifact digests; it does not rerun computation.

| Scenario | Workflow exit | Oracle value/status | Binding/effect/link result | Expected claim disposition |
|---|---:|---|---|---|
| `none` | 0 | 767, `SUPPORTED_FIXTURE` | All local checks; one effect row | `RECORD_SCOPED_FIXTURE` |
| `foreign-result` | 0 | 767, `SUPPORTED_FIXTURE` | Experiment/input false | `WITHHOLD_FIXTURE_CLAIM` |
| `checkpoint-corrupt` | Nonzero; historically 1 | Not evaluated | Guard 22, checkpoint-byte check false; no bundle | No downstream claim |
| `retry-unsafe` | 0 | 767, `SUPPORTED_FIXTURE` | Two effect rows; idempotency false | `WITHHOLD_FIXTURE_CLAIM` |
| `broken-link` | 0 | 767, `SUPPORTED_FIXTURE` | Result-to-evaluation index link false | `WITHHOLD_INVALID_EVIDENCE_LINK` |
| `numerical-failure` | 0 | 0, `FAILED_FIXTURE` | Local binding/effect/link checks remain valid | `WITHHOLD_FIXTURE_CLAIM` |

In every produced bundle, `real_scientific_status` remains `NOT_EVALUATED`. An invalid binding does not prove a scientific hypothesis false; it withholds the claim based on that evidence.

## Native provenance audit

The reference entrypoint uses `--native`; the extra execution supports provenance-format inspection only and is not counted as another independent experiment. Its audit verifies a BagIt manifest, rejects a controlled equal-length mutation, parses PROV and retains the failed numerical boundary. Graph counts are runtime observations, not fixed universal acceptance targets. Qualified usage/generation relations count as relations even when direct `prov:used`/`prov:wasGeneratedBy` predicates are absent. No full Workflow Run profile validator, authenticated provenance, collector deployment or independent scientific assessment is exercised.
