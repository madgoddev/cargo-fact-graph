# CargoFactGraph

CargoFactGraph is a standalone, reusable GenLayer Intelligent Contract that turns a bounded bundle of caller-supplied public shipping-document plaintext into an immutable, consensus-backed fact-and-provenance graph.

It answers a narrow question:

> Which requested shipping facts are supported by the supplied documents, which excerpts support them, and where do documents make incompatible assertions in the exact same context?

It does **not** decide whether a document is authentic, forged, fraudulent, legally valid, authoritative, or controlling. It does not decide ownership, title, customs compliance, liability, delivery entitlement, or which source should prevail.

## Why GenLayer is necessary

Shipping records express the same facts with different labels, formats, abbreviations, qualifiers, and surrounding context. Determining that "port of discharge," "discharge location," and a named terminal describe the same requested role is semantic work. So is distinguishing a true incompatibility from a temporal update: an original ETA followed by a revised ETA is a revision, not a contradiction. GenLayer validators independently substantiate values, context qualifiers, revisions, support, and conflict scope against all supplied document text before any graph is stored.

The contract does not use arbitrary web retrieval. Callers submit bounded plaintext. Provenance labels are recorded as unverified descriptions, never treated as proof of source identity.

## Contract boundary

- **Caller owns:** selecting public documents, converting them to plaintext, choosing truthful descriptive labels, and deciding how to use a graph.
- **CargoFactGraph owns:** strict bundle validation, policy-bound content identity, a closed fact taxonomy, semantic extraction, support linkage, context-aware reconciliation, independent validator substantiation, and immutable storage.
- **Downstream systems own:** source authentication, legal/commercial decisions, risk scoring, payments, insurance, customs filings, title transfer, and user interfaces.

## Atomic records and policy identity

`create_graph(bundle_json)` canonicalizes the entire accepted bundle and derives:

- `bundle_content_id = sha256(canonical bundle)`
- `graph_id = cfg5:sha256(compilation_policy_version || NUL || canonical bundle)`
- `graph_content_id = sha256(canonical stored graph payload)`

The current compilation policy is `CARGO_FACT_RECONCILIATION/5`. Binding that policy into the graph ID prevents an interpretation cached under older extraction or reconciliation rules from being silently reused. `derive_bundle_identity` returns the bundle content ID, compilation policy version, and policy-bound graph ID.

A graph ID may be written only once. There are no edit, delete, administrator, payout, or upgrade methods. All storage writes occur in one transaction after consensus.

## Input

The JSON object must contain exactly:

```json
{
  "shipment_reference": "caller's local scope label",
  "requested_fact_types": ["CONTAINER_NUMBER", "ARRIVAL_DATE"],
  "documents": [
    {
      "document_id": "DOC-1",
      "document_type": "BILL_OF_LADING",
      "provenance_label": "unverified caller description",
      "content": "public plaintext ..."
    },
    {
      "document_id": "DOC-2",
      "document_type": "ARRIVAL_NOTICE",
      "provenance_label": "unverified caller description",
      "content": "public plaintext ..."
    }
  ]
}
```

Duplicate JSON keys, nonfinite JSON numbers, extra fields, unknown enum values, duplicate document IDs, and out-of-bound inputs are rejected. See `examples/reconciliation_bundle.json` for a complete example.

## Context-aware output graph

The immutable payload contains:

- document manifest entries with unverified labels and plaintext content hashes;
- normalized fact nodes from the requested closed taxonomy;
- support edges with exact verbatim excerpts;
- contradiction edges limited to incompatible nodes with an exact matching context;
- one explicit review record for every supplied document;
- a deterministic coverage note derived from resolved and unresolved types;
- unresolved requested fact types; and
- a permanent scope disclaimer.

Each fact node has a context with:

- `scope_key`: a conservative role, entity, leg, or event key;
- `assertion_mode`: `ACTUAL`, `ESTIMATED`, `SCHEDULED`, or `UNQUALIFIED`; and
- `record_status`: `CURRENT`, `SUPERSEDED`, or `UNSPECIFIED`.

A contradiction requires the same fact type and exact same context. A `SUPERSEDED` fact cannot participate. Estimated, scheduled, and actual dates remain distinguishable, while a revised ETA can preserve the superseded and current estimates without inventing a conflict.

The semantic consensus wire contains only fact objects, their nested document/excerpt supports, and unresolved requested types. The contract derives context-qualified fact keys internally under one 420-character bound, then deterministically assigns node and support-edge IDs. It derives every contradiction from two different normalized values with the same fact type and exact context, excluding any `SUPERSEDED` node. The fact-key limit remains exposed as `limits.max_fact_key_chars` by `get_protocol`.

Every fact node must have at least one support. Every excerpt must be an exact substring of its labelled document. Validators additionally check whether the excerpt semantically supports the node, whether normalization and context are source-grounded, whether revision handling is sound, whether every document was considered, and whether deterministic same-context conflicts would be sound and complete. Their response is deliberately low entropy: exactly `verdict` and one closed `issue_code`. Only `ACCEPT` plus `NONE` votes true.

The leader cannot author fact keys, graph IDs, support-edge references, contradictions, explanations, coverage notes, or per-document reviews. It returns only nested facts and supports plus unresolved fact types. The contract derives IDs, reviews, coverage, the complete contradiction set, and fixed contradiction text.

Every field in the bundle is explicitly delimited as untrusted prompt data, including `shipment_reference`, document IDs, provenance labels, and document plaintext. Candidate fields are also untrusted. Each validator independently re-normalizes the leader candidate before semantic review.

## Read interface

The contract exposes bounded reads for headers, full payloads, manifests, document reviews, unresolved types, facts by type, and paginated nodes, edges, and contradictions. Page size is capped at 25. JSON collection methods return canonical JSON strings to keep the ABI stable for downstream contracts.

## Development

The first line pins the production GenVM Python runner. The project includes direct-mode tests and a five-validator GLSim integration test. No frontend is included.

```powershell
genvm-lint check contracts/cargo_fact_graph.py
genvm-lint schema contracts/cargo_fact_graph.py --output abi.json
genvm-lint typecheck contracts/cargo_fact_graph.py --strict
pytest tests/direct -v
powershell -ExecutionPolicy Bypass -File scripts/run_glsim_5.ps1
```

The PowerShell harness applies a project-local cleanup-timing workaround for a Windows-only `genlayer-test` 0.29.2 tempfile issue, starts exactly five GLSim validators, runs the integration suite, and stops the simulator.

## Deployment status

The exact v5 source has passed local lint, strict type checking, 98 direct tests,
and two isolated five-validator GLSim tests. It is also deployed on StudioNet
and Bradbury with exact source, ABI, and protocol readback.

The StudioNet deployment and semantic smoke both finalized successfully. Exact
readback verified the expected `cfg5` identity, two documents, five facts, eight
support edges, the superseded/current ETA pair, no contradictions, and no
unresolved types. See `deployments/studionet.json`.

The Bradbury deployment finalized successfully with five agrees. Its single
semantic smoke also finalized with an `AGREE` consensus result and
`FINISHED_WITH_RETURN`; the exposed round contained three agrees and two
timeouts. Exact latest-final readback verified the expected graph and bundle
identities, canonical graph-content hash, two documents, five facts, eight
support edges, the superseded/current ETA pair, no contradictions, and no
unresolved types. See `deployments/bradbury.json`.

### Historical v4 network evidence

The historical StudioNet record at `deployments/studionet-policy-v4.json` verifies the exact
v4 source and ABI. Deployment transaction
`0xadedd6c36abb43775054ef9330c16d98e79f8d8129682513d898c0ffc744df89`
finalized successfully with five validator agrees. The one-write semantic smoke
`0x513241ebe3457595afad7d9ad4d1b70a4739a7fa1edc90a28d65fb97ac786ace`
also finalized successfully and stored the expected policy-bound graph. Final
readback verified two documents, five fact nodes, eight support edges, the
superseded/current ETA pair, no contradictions, and no unresolved types.

The historical Bradbury record at `deployments/bradbury-policy-v4.json` verifies that the
identical v4 bytes were deployed in transaction
`0xa855ffbae9c02fad91133300d0043d7fa0e58121ce794ed6926b43927713ffac`.
The deployment finalized successfully with five of five validator agrees, and
final reads reconfirmed the exact source, schema, protocol, policy, audit schema,
and empty initial state.

The sole authorized Bradbury semantic smoke
`0x1ac8fdf53c98928a2b83868b9d9f9561b866412299bd12d788796ab42ec9f51a`
finalized with disagreement and a failed execution. Its first round returned a
structurally valid, fixture-consistent candidate, but three validators timed out
and two agreed. Later leader candidates were rejected by the contract's exact
fact-context rule. Latest-final and latest-nonfinal reads both remained empty.
No operator retry, appeal, or manual finalization was performed. Accordingly,
Bradbury deployment and interface verification pass, but Bradbury semantic-write
verification is unavailable for this frozen build. This is a network-limited
v4 release and does not claim a dual-network semantic pass. Neither historical
record is evidence for v5.

## License

MIT. See `LICENSE`.
