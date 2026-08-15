# Handoff

CargoFactGraph is a standalone, contract-only GenLayer project with no frontend
and no dependency on sibling projects.

## Current v5 candidate

Protocol/policy v5 reduces the model wire to nested semantic facts/supports plus
unresolved types. The contract derives fact keys, IDs, reviews, coverage, and
the exact-context contradiction set. Validators still audit the complete bundle
and candidate, but return only `{verdict, issue_code}`. The public
ABI remains 14 methods: thirteen views, one write, and no constructor arguments.

Local verification currently passes:

- GenVM lint and SDK validation: 3 checks, 14-method ABI;
- strict typecheck: zero diagnostics;
- direct tests: 98 passed; and
- isolated five-validator GLSim: 2 passed with five agrees per write.

The exact v5 source is deployed on StudioNet and Bradbury. StudioNet deployment,
semantic write, and exact graph readback finalized successfully. The Bradbury
deployment also finalized successfully with five agrees. Its single semantic
smoke finalized with an `AGREE` result and `FINISHED_WITH_RETURN`; the round
contained three agrees and two timeouts. Exact latest-final graph readback
passed, so v5 now has a finalized semantic pass on both networks.

Frozen source: SHA-256
`95CF918C045114337D05F652C586BB9FB77A770F6D342FBBD51964C37A25450A`,
42,460 bytes, 1,041 lines. Any source change invalidates this candidate and
requires a new hash, full verification, and renewed audit.

Current sanitized v5 records are `deployments/studionet.json` and
`deployments/bradbury.json`. Both records contain finalized semantic-write and
exact state-readback evidence.

## Historical v4 evidence

The exact v4 source SHA-256
`B6303AC060FF45DAE4C10208DA48E1CE1950D915FB919CDFCE9FB09AEEC8F4FD`
is preserved in `deployments/studionet-policy-v4.json` and
`deployments/bradbury-policy-v4.json`. StudioNet v4 semantic verification
passed. The identical Bradbury v4 deployment passed, while its sole semantic
smoke finalized unsuccessfully with disagreement and no state change. These
records are historical and must never be presented as v5 evidence.

## Packaging

Package only an explicit allowlist. Exclude `.git`, caches, `.glsim`,
`.gltest_artifacts`, `__pycache__`, bytecode, logs, raw receipts, traces, node
configurations, environment files, wallets, keys, keystores, and temporary
deployment helpers. Keep the ZIP checksum in a sibling `.sha256` file outside
the archive.
