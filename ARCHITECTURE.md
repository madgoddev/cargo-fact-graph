# Architecture

## Consensus-owned transition

1. A caller submits a strict bounded plaintext bundle.
2. Deterministic code rejects duplicate JSON keys and validates exact shape, closed enums, sizes, uniqueness, and canonical content.
3. The graph identity binds both the canonical bundle and `CARGO_FACT_RECONCILIATION/5` policy.
4. A leader proposes only context-qualified fact nodes with nested exact supports, plus unresolved types.
5. Deterministic normalization rejects unknown taxonomy or qualifier values, non-verbatim excerpts, incomplete requested-type coverage, duplicate records, and unsafe bounds. It derives fact keys, node IDs, support-edge IDs, per-document reviews, coverage, and every contradiction. A conflict is derived for every different value with the same fact type and exact context unless either node is `SUPERSEDED`.
6. The leader returns a normalized consensus-wire candidate. Every validator independently runs the same normalization again before semantic review.
7. Each validator receives the complete canonical bundle and independently normalized semantic projection. It substantively audits every document, fact, support relation, normalization, context, revision, unresolved type, and contract-derived same-context conflict. It returns exactly `verdict` and one closed `issue_code`; only `ACCEPT` + `NONE` votes true.
8. Only the accepted wire candidate is normalized once more, assembled into one canonical graph payload, and written atomically.

Malformed leaders, normalization exceptions, malformed audits, invalid verdict/code pairings, and every rejection verdict fail closed.

## Graph model

- `document_manifest[]`: document ID, closed document type, unverified provenance label, plaintext content hash.
- `fact_nodes[]`: deterministic node ID, closed requested type, normalized value, display value, and context.
- `fact_nodes[].context`: bounded `scope_key`, closed `assertion_mode`, and closed `record_status`.
- `support_edges[]`: deterministic edge ID, document ID, fact-node ID, exact source excerpt.
- `contradictions[]`: deterministic contradiction ID, same-type node pair, exact shared context, and fixed contract-owned explanation.
- `document_reviews[]`: one deterministic contract-derived coverage observation for every input document.
- `unresolved_fact_types[]`: requested types for which no adequately supported node was found.

`assertion_mode` is one of `ACTUAL`, `ESTIMATED`, `SCHEDULED`, or `UNQUALIFIED`. `record_status` is one of `CURRENT`, `SUPERSEDED`, or `UNSPECIFIED`.

Contradictions are deterministically created when two nodes have different values, the same fact type, and byte-for-byte identical normalized context. A `SUPERSEDED` node is ineligible. Validators must therefore reject contexts that would collapse revision transitions, estimated-versus-actual differences, or coexistable entities, roles, legs, packages, ports, or dates into a false conflict.

Fact keys never appear on the model wire. The contract derives `FACT_TYPE|SCOPE_KEY|ASSERTION_MODE|RECORD_STATUS|normalized_value` and enforces `MAX_FACT_KEY_CHARS = 420`. The central constructor rejects any future component combination that exceeds that coherence bound.

The original full plaintext is not copied into contract storage. It remains present in public transaction input; the graph stores content hashes and exact cited excerpts.

## Prompt trust boundary

The bundle and candidate are placed inside explicit `BEGIN_UNTRUSTED_*` and `END_UNTRUSTED_*` delimiters. The prompt states that every field is data, including shipment reference, document IDs, provenance labels, document content, and candidate values. Embedded instructions, role changes, and output requests must be ignored. No URL is fetched. IDs, conflict prose, coverage notes, and document reviews are not accepted from the model.

## Identity and immutability

`bundle_content_id` identifies only canonical caller input. `graph_id` is separately derived as `cfg5:sha256(compilation_policy_version || NUL || canonical_bundle)`. This prevents a graph compiled under one semantic policy from occupying or satisfying the cache identity for a later policy.

No mutation endpoint exists. The canonical graph payload is stored as one JSON value and independently hashed. Auxiliary indexes are written in the same transaction and never updated.

## Consensus-footprint reduction

For the published fixture, v5's canonical semantic projection is 1,662 bytes,
down from v4's 2,212-byte wire by 550 bytes (24.86%). The validator prompt is
5,452 bytes rather than 6,150, and the compact accepting audit is 40 bytes with
two fields rather than 330 bytes with eleven fields. One nominal leader plus
five-validator round therefore carries 32,185 prompt bytes instead of 35,669,
excluding outputs and runtime envelopes. These are deterministic fixture
measurements, not guarantees about network latency or model behavior.

## Consensus policy

The leader performs open-ended extraction. Validators do not approve merely because fields and enums are well formed. They independently compare the normalized candidate to all supplied evidence and reject if any value, context, revision status, or support relation is unsupported; any normalization invents meaning; any material requested fact or same-context conflict is omitted; any revision is mislabeled as a contradiction; or any forbidden judgment appears. The prompt fixes conservative defaults: same-shipment facts use `SHIPMENT` unless the evidence establishes a narrower real-world scope, unqualified assertions use `UNQUALIFIED`, records use `UNSPECIFIED` absent explicit status, and explicit revisions keep one scope with earlier `SUPERSEDED` and later `CURRENT` nodes.
