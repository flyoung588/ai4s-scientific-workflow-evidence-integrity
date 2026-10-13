# Reviewer guide

**Internal review candidate. Publication, licensing and third-party scientific review remain pending.**

The intended review is small: determine whether the retained evidence supports the stated engineering boundaries and whether the short whitepaper example is useful. The package does not ask reviewers to endorse a new scientific workflow platform or a theory of autonomous research.

## A short source-first review

1. Read the claim ceiling in [README.md](README.md), then the scenario table in [CASE_STUDY.md](CASE_STUDY.md). Check that successful execution, numerical agreement, evidence binding and scientific validity are separate claims.
2. Inspect `src/cwl/worker.py` and `evaluator.py`. Verify the interrupted child versus wrapper distinction, the pre-mutation checkpoint reference, the stable logical-effect key, and the separate arithmetic and binding axes.
3. Inspect the intentionally deficient baseline and `src/components/research.py`. Distinguish the baseline’s coarse local cache (767 versus the changed expected value 623) from CPython `lru_cache` (21 versus 28). Confirm that the RNG is Python's local generator, and OpenTelemetry uses an in-memory exporter. The examples should not be attributed to an untested workflow controller.
4. If reproducing, use a fresh directory and the commands in [REPRODUCE.md](REPRODUCE.md). Review `fixtures/acceptance-contract.json`, the source-bound reference receipt under `results/reference-run/` and actual retained bytes. The preserved baseline’s ten checks are context for the later sixteen controls; neither their sum nor six matched CWL scenarios counts new discoveries. Record a reproduction failure rather than changing an expected result to make the run pass.
5. Challenge one negative control: examine a foreign-bound correct number, a duplicate committed effect, a corrupt checkpoint, or a broken evaluation link. Then inspect the ordinary control to ensure the check distinguishes the intended change.

## Questions that would improve the contribution

- Does the exact result/input/checkpoint binding cover the stated local claim without suggesting that a hash authenticates its issuer?
- Are evaluation outputs represented as evaluation outputs, with the result being evaluated kept as an input?
- Does the treatment of a retained span losing an evidence attribute add useful detail beyond the already-discussed sampling limitation?
- Do the runtime receipts make a controlled child interruption and normal wrapper completion distinguishable?
- Are the four application records—contract, attempt/checkpoint receipt, evaluation report and evidence index—sufficient for this example without prescribing a new standard?
- Would a shorter or differently scoped §5 example better serve the working group's five-page document?

## How to report a finding

Identify the source file or evidence artifact, the expected observation, the actual observation and the narrow consequence. Keep missing evidence, an implementation error, an invalid scientific claim and a proposed extension distinct. A critique can correctly conclude that a claim should be narrowed or removed; a passing rerun is not the only useful outcome.

If a reviewer runs the package independently, record that person's own environment and changes rather than inheriting the producer's independence label. An external rerun would need its own evidence before L4 could change; AI role separation and another local environment do not satisfy that condition. Even independent engineering reproduction would not by itself validate a real scientific result.

## Boundaries for the working group

The §4.4 proposal is an optional small addition to an existing contribution, not a repeat submission. The §5 case is synthetic and local. Placement, credit and acceptance are decisions for the working group. No group membership, authorship assignment, text adoption or formal collaboration is implied by preparing the files. No license or rights to redistribute code have been granted by the candidate status. Generated execution artifacts should be checked for local paths or identifiers before any separately approved publication.


Publication note: human approval now permits this personal technical case and Apache-2.0 original reproduction code. Historical preparation fields are retained as history. Working-group adoption and independent third-party replication remain unproven.
