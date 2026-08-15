# Testing Record

Test date: 2026-08-12

## Verified toolchain

- Python 3.12.13
- `genvm-linter` 0.11.0
- `genlayer-test` 0.29.2
- Pytest 9.1.1
- Pyright 1.1.411
- GLSim with exactly five validators

## Final results

```text
GenVM lint / SDK validation: PASS
ABI extraction:              PASS (14 methods: 1 write, 13 views)
Strict typecheck:             PASS (0 errors, 0 warnings, 0 info)
Direct tests:                 PASS (98/98)
Five-validator GLSim:         PASS (2/2)
Total automated tests:        PASS (100/100)
StudioNet v5 deployment:      PASS (FINALIZED, 3 agree, 2 idle)
StudioNet v5 semantic smoke:  PASS (FINALIZED, 3 agree, 2 idle)
Bradbury v5 deployment:       PASS (FINALIZED, 5 agree)
Bradbury v5 semantic smoke:   PASS (FINALIZED, 3 agree, 2 timeout)
```

The Bradbury smoke finalized with an `AGREE` consensus result and
`FINISHED_WITH_RETURN`. All five validators committed and revealed; the exposed
round votes were three agrees and two timeouts.

## Current v5 network evidence

- StudioNet exact deployment and semantic smoke: **PASS** with finalized graph
  readback for two documents, five facts, eight supports, the ETA revision, zero
  contradictions, and zero unresolved types.
- Bradbury exact deployment: **PASS** (`FINALIZED`, five agrees).
- Bradbury semantic smoke: **PASS** (`FINALIZED`, `AGREE`,
  `FINISHED_WITH_RETURN`; three agrees and two timeouts). Exact latest-final
  readback matches the complete expected v5 graph, including the graph-content
  hash and ETA revision semantics.

Sanitized v5 evidence is in `deployments/studionet.json` and
`deployments/bradbury.json`.

## Historical v4 Bradbury evidence

- Historical exact v4 deployment: **PASS** (`FINALIZED`, 5 agree).
- Semantic smoke: **UNAVAILABLE** as successful-write evidence. The sole
  authorized transaction finalized with disagreement and
  `FINISHED_WITH_ERROR`; latest-final and latest-nonfinal state remained empty.
- No operator retry, appeal, or manual finalization was performed.

The Bradbury result verifies deployment and interface identity, not a successful
semantic state transition. It is not included in the all-pass summary above and
does not support a dual-network semantic-pass claim. Sanitized evidence is in
`deployments/bradbury-policy-v4.json`.

Both GLSim writes asserted:

- exactly five validator votes;
- every vote was `agree`;
- exactly five validator execution receipts;
- every validator execution result was `SUCCESS`;
- the leader execution succeeded before any read assertion;
- persisted policy-bound identity, counts, pages, exact excerpts, revision contexts, and disclaimer were readable afterward.

The historical v4 StudioNet smoke independently exercised the real model-backed
path and stored
`cfg4:4559d69da203fa35fbf64a3ec479b259de14122fe28cf18a1f7771c751ad94c6`.
Its sanitized record remains in `deployments/studionet-policy-v4.json`; it is not
v5 evidence.

## v5 regression coverage

The direct suite additionally proves:

- strict nested fact/support projection shape with no fact keys, standalone
  support edges, model contradictions, or model contradiction prose;
- verbatim excerpts, known documents, per-fact support, global 128-support
  bounds, duplicate rejection, and permutation-stable derived IDs;
- exact-context deterministic conflicts, `SUPERSEDED` exclusion, 55-conflict
  success, and fail-closed behavior above the 64-conflict bound;
- the revised ETA fixture remains five nodes, eight supports, zero conflicts,
  and zero unresolved types;
- validators independently re-normalize the full semantic projection; and
- exactly one two-field accepting audit encoding votes true.

For the canonical fixture, the v5 wire is 1,662 bytes, the leader prompt is
4,925 bytes, the validator prompt is 5,452 bytes, the compact accepting audit is
40 bytes, and one nominal leader plus five-validator prompt footprint is 32,185
bytes. The equivalent v4 wire, validator prompt, accepting audit, and nominal
round were 2,212, 6,150, 330, and 35,669 bytes respectively.

## Reproduction

Install the pinned development requirements in a Python 3.12 virtual environment, ensure its command directory is on `PATH`, then run from this project root:

```powershell
genvm-lint check contracts/cargo_fact_graph.py --json
genvm-lint schema contracts/cargo_fact_graph.py --output abi.json
genvm-lint typecheck contracts/cargo_fact_graph.py --strict --json
pytest tests/direct -q
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_glsim_5.ps1
```

The integration harness uses isolated port 4013 by default, refuses to attach to an unidentified process already using that port, starts a hidden GLSim process with `--validators 5`, waits for the JSON-RPC endpoint, runs only `tests/integration`, and terminates the simulator in a `finally` block. Pass `-Port <number>` to select another isolated port.

## Windows tooling note

`genlayer-test` 0.29.2 attempts to unlink a temporary stdin backing file while fd 0 still holds it. Windows rejects that cleanup order. `support/windows_gltest_compat.py` changes only the timing of test-runner tempfile deletion; it does not alter contract source, calldata, consensus logic, stored values, or assertions. It is loaded by the direct-test conftest and GLSim bootstrap only.

## ABI fingerprint

- `abi.json` SHA-256: `31CD77F8469FBA83BF8AA7B5EA3CA689A44DFBAFD856AD1FC98896094D182794`
- Current v5 audit-candidate source SHA-256:
  `95CF918C045114337D05F652C586BB9FB77A770F6D342FBBD51964C37A25450A`
- Current v5 audit-candidate source bytes: `42,460`
- Current v5 audit-candidate source lines: `1,041`
- Semantic projection fixture SHA-256:
  `69D8035DEEBEC58723E317487F2A4C26763B7C61BF5B4E8F7C30CAFB7098287C`

Any contract-source change invalidates this candidate and requires rerunning the
entire verification suite. Historical v4 fingerprints remain in their
versioned deployment evidence.
