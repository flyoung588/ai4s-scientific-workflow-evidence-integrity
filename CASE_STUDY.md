# From an interrupted calculation to a bounded claim

The example computes an integer recurrence over twenty fixed synthetic inputs. An iterative worker produces the answer; a separate closed-form implementation supplies the expected value, 767. The algorithms differ, but they share authorship and known inputs. Their agreement establishes only this fixture's arithmetic property.

## The actual local workflow

The CWL reference executor runs four stages: checkpoint, resume, evaluate and package. The checkpoint child writes its state and is terminated with SIGTERM after a handshake. The wrapper records that interruption. Resume verifies a pre-mutation checkpoint digest together with the declared experiment, input, worker and index bounds. The pre-mutation reference is local and unsigned.

During resume, a separate child commits one logical side effect to SQLite and then returns a controlled lost-acknowledgement code. Tenacity invokes it again. A stable effect key and a uniqueness constraint leave one row. A deliberately unsafe scenario omits that constraint and leaves two. This is a local idempotency demonstration, not a general exactly-once guarantee for external instruments, concurrent workers or distributed systems.

Evaluation consumes actual result and receipt bytes. It records arithmetic and binding checks separately. Packaging writes an RO-Crate and an evidence index. A readable crate is not treated as evidence that its result, input and evaluation links are correct. The evaluation report is an output of the evaluation activity; the candidate result is an input to that activity.

| CWL scenario | Expected process observation | Evidence consequence |
|---|---|---|
| `none` | Workflow completes; value 767; one effect row | Record a scoped fixture result |
| `foreign-result` | Workflow completes; value remains 767 | Reject experiment/input binding |
| `checkpoint-corrupt` | Resume guard exits 22; workflow fails before evaluation/package | Retain failed receipt; no downstream bundle |
| `retry-unsafe` | Workflow completes; two effect rows | Reject the local idempotency obligation |
| `broken-link` | Workflow completes and artifacts remain readable | Reject the result-to-evaluation index link |
| `numerical-failure` | Workflow completes; observed 0, expected 767 | Preserve a failed fixture evaluation; withhold its claim |

The six expectations include normal results, incorrect results, incomplete evidence and intentional execution failure. Counting matched expectations as successful science would invert the purpose of the controls.

## Component controls that the DAG does not subsume

The separate component study preserves an earlier evaluator that accepts the expected number even when the result belongs to another experiment. It also shows why changing an experiment label does not make a resumed calculation an independent replicate. A Python random stream needs its actual RNG state for exact continuation; restarting the seed does not supply the missing state.

The preserved baseline also retains ten original checks. Its normal resumed and fresh answers are both 767. Changing the coefficient from 3 to 4 makes the fresh expected answer 623, while a coarse local cache returns the stale 767. Bypassing the checkpoint binding guard lets an old state resume to 38 with a normal process exit. These are concrete dependency and continuation counterexamples; the later component controls expose additional weaknesses that those ten checks alone do not exclude. The baseline’s literal `CHECKPOINT_DURABLE` marker records a write-and-close handshake, not a demonstrated power-loss durability guarantee.

A second cache example is CPython `lru_cache`: an unlisted mutable coefficient changes from 3 to 4, while the cached answer remains 21 instead of 28. Including the coefficient in the key gives the expected value. This exposes an application dependency omission, not a cache-library defect. There is no cache stage in the CWL DAG and no Argo cache deployment in the package.

OpenTelemetry controls show two separate losses: an `ALWAYS_OFF` sampler exports no span, while a retained span with an attribute limit can lose its evidence reference. Another retained span has execution status `OK` while carrying a failed domain verdict. These were in-memory SDK tests, not collector, network or backend retention tests. An independent evidence index is therefore checked without relying on a trace attribute as its only link.

## Existing provenance is useful, with a defined scope

The native-provenance audit uses cwltool's PROV records and BagIt package. In the retained reference run, a valid bag passed and an equal-length byte mutation failed checksum validation, even though the associated workflow completed and its numerical evaluation failed. This motivates using existing integrity tools while retaining a separate evaluation boundary. It does not demonstrate full Workflow Run RO-Crate profile compliance, authenticated provenance or scientific validity.

The candidate supplies four small application interfaces: a declared experiment contract; attempt/checkpoint receipts; an evaluation report; and an evidence index. They are examples, not a proposed new standard, mandatory controller API or autonomous resource-allocation system. The example never turns an evaluation result into authority to start a new experiment.

## Evidence and limitations

The package’s single-entrypoint clean run completed on 2026-10-13 from 05:19:09 to 05:19:28 UTC. All six acceptance checks in [the retained summary](results/reference-run/summary.json) are true, including the original controls, byte/database adjudication and native audit. Same-machine reproduction and additional AI code review remain distinct from third-party scientific replication.

L1 covers software behavior under enumerated controls; L2 covers local retained bytes and relationships without authentication; L3 covers an exact synthetic integer criterion; L4 independent third-party replication is **NOT_PERFORMED**. No claim is made about Argo/Kubernetes controllers, GPU or distributed checkpointing, power-loss durability, real scientific holdouts, causal inference, out-of-distribution performance or autonomous discovery.

## Primary references

The case follows existing [CWL workflow input/output semantics](https://www.commonwl.org/user_guide/topics/workflows.html), [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) and [Workflow Run RO-Crate's Process Run profile](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/). The component limits are documented in the [OpenTelemetry tracing SDK specification](https://opentelemetry.io/docs/specs/otel/trace/sdk/) and [CPython cache documentation](https://docs.python.org/3/library/functools.html#functools.lru_cache). The native integrity check uses [BagIt-python](https://github.com/LibraryOfCongress/bagit-python). [Argo retry documentation](https://argo-workflows.readthedocs.io/en/release-4.0/retries/) is background for architectural comparison, not evidence that Argo was executed here.
