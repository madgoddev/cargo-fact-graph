# CargoFactGraph Security and Design Audit

Audit date: 2026-08-12

Audited contract: `contracts/cargo_fact_graph.py`

Current v5 candidate SHA-256: `95CF918C045114337D05F652C586BB9FB77A770F6D342FBBD51964C37A25450A`

## Outcome

The original v1 candidate was independently reviewed and was not approved because it could misclassify a revised ETA as a contradiction, lacked explicit fact context, accepted duplicate JSON keys, did not independently normalize the leader result inside each validator, did not delimit every caller-controlled label as untrusted prompt data, and did not bind compilation policy into cache identity.

Protocol and policy v2 resolved those findings. A subsequent independent review found one inconsistent reference bound: valid context-qualified keys above 224 characters could be used by support edges but not contradiction endpoints. That was resolved with one centralized 420-character limit.

A Bradbury v2 smoke then exposed a liveness defect: the model was asked to author an unconstrained `coverage_note`, while deterministic substring filtering could reject even a harmless negative disclaimer. Protocol and policy v3 removed model-authored coverage and review narratives from the consensus wire. The contract derives those fields from accepted graph structure using fixed templates.

A live StudioNet v3 smoke exposed a separate validator-interface defect. Deterministic normalization intentionally removed assigned `fact_node_id` and `support_edge_id` fields from the consensus wire, but the validator prompt still required exact lists of those opaque IDs. Even a substantively sound candidate could therefore be rejected for failing an impossible echo task. Protocol and policy v4 remove every document/node/edge ID echo from the audit response. Validators now make the same independent full-evidence judgment through one closed verdict, nine semantic booleans, and a closed issue-code list. Context defaults and explicit revision handling are also stated symmetrically in leader and validator prompts. Local static, direct, and five-validator GLSim verification passes, an independent review approved the exact frozen source, and a live v4 StudioNet deployment plus semantic smoke finalized successfully with exact state readback.

The sole v4 Bradbury semantic smoke later separated two failure modes: round zero
returned a structurally valid fixture-consistent candidate but timed out without
consensus, while later leaders proposed invalid contradiction contexts and were
rejected deterministically. Protocol/policy v5 reduces liveness surface without
weakening the semantic audit. The wire now contains only nested facts/supports
and unresolved types; the contract derives fact keys, IDs, reviews, coverage,
contradictions, and contradiction text. The validator response is exactly two
fields. Local lint, strict type checking, 98 direct tests, and two isolated
five-validator tests pass. Independent review approved the exact v5 hash; exact
deployments now pass on StudioNet and Bradbury. The StudioNet semantic write and
readback finalized successfully. The Bradbury semantic write also finalized
with agreement, successful execution, and exact latest-final readback.

## Resolved independent-audit findings

### Revision is not contradiction

- Fact nodes now carry source-grounded `assertion_mode` and `record_status` qualifiers.
- The leader and validator policies explicitly state that an original ETA followed by a revised ETA is a temporal update, not a contradiction.
- The included example stores the earlier estimate as `SUPERSEDED` and the revised estimate as `CURRENT` with no conflict edge.
- Estimated, scheduled, actual, and unqualified assertions are distinct closed modes.

### Safe contradiction scope

- Each fact has a bounded `scope_key` plus closed assertion and record qualifiers.
- Fact identity includes the complete context.
- Deterministic code permits a contradiction only between different values of the same type with exact context equality.
- A `SUPERSEDED` node cannot participate in a contradiction.
- Validators must reject coexistable entities, roles, legs, temporal states, and revisions mislabeled as conflicts.
- Direct tests cover a valid same-context conflict, different-context rejection, superseded-node rejection, and the revision-without-conflict example.

### Strict JSON boundary

- Bundle and string-form model JSON use duplicate-key-rejecting `object_pairs_hook` parsing.
- Nonfinite JSON constants are rejected.
- Exact keys, exact closed enums, bounds, uniqueness, and UTF-8 byte caps remain enforced.

### Independent validator normalization

- The leader returns a normalized consensus-wire candidate without assigned IDs.
- Every validator independently normalizes that candidate against the complete bundle before constructing its semantic review prompt.
- The validator also checks that reserialization equals the leader wire candidate, preventing hidden extra data or noncanonical structure.
- The accepted wire candidate is normalized once more before graph assembly and atomic storage.
- Malformed leaders, normalization failures, malformed audits, invalid verdict/code pairings, and rejection verdicts fail closed.

### Answerable validator audit schema

- The validator still receives the complete canonical bundle and independently normalized candidate, so it must judge every source, fact, support relation, normalization, context, revision, unresolved type, conflict, and forbidden-judgment boundary.
- The response contains exactly `verdict` and one closed `issue_code`; it contains no requested document, node, or edge ID echo.
- Only `ACCEPT` and `NONE` votes true.
- `REJECT` requires one closed non-`NONE` code. Every rejection votes false.
- The schema identity `CARGO_FACT_VALIDATOR_AUDIT/5` and closed issue taxonomy are exposed by `get_protocol`.
- A regression captures the validator prompt and proves the impossible v3 ID fields are absent. Another replays the structurally valid live Studio round-one candidate and proves it can pass under a compliant semantic audit.

### Complete prompt-injection boundary

- Bundle and candidate blocks use explicit `BEGIN_UNTRUSTED_*` / `END_UNTRUSTED_*` delimiters.
- Prompts state that shipment reference, provenance labels, document IDs, document plaintext, display values, and every candidate field are untrusted data.
- Embedded instructions, role changes, and output requests must be ignored.
- No arbitrary URL or web request interface exists.

### Policy-bound identity and coherence

- `bundle_content_id` remains a pure canonical-input hash.
- `graph_id` is now `cfg5:sha256(CARGO_FACT_RECONCILIATION/5 || NUL || canonical_bundle)`.
- A candidate cached under one compilation policy therefore cannot occupy the identity for another policy.
- Policy version is returned by `derive_bundle_identity`, stored in graph payloads, exposed in headers and protocol metadata, and checked on every material read.
- Material reads also recheck canonical payload encoding, graph ID, bundle content ID, and graph content hash.

### Uniform fact-key bounds

- `MAX_FACT_KEY_CHARS = 420` bounds each contract-derived fact key; fact keys no longer appear in model output.
- Central key construction checks the limit, so accepted-candidate reconstruction and validator re-normalization cannot silently create an out-of-policy key.
- A direct boundary test stores two independent active estimated-arrival assertions as a valid same-context conflict whose endpoint keys exceed the former 224-character limit; the fixture contains no revision wording.
- Boundary tests exercise long contract-derived keys and deterministic conflicts without exposing key references to the model.
- `get_protocol` publishes the bound as `limits.max_fact_key_chars`.

### Deterministic stored narratives

- The leader wire contains only fact nodes with nested supports and unresolved fact types.
- Every validator independently re-normalizes and semantically audits those substantive fields against the complete bundle.
- Per-document review status and prose are derived solely from whether the document supplies a support edge.
- Coverage prose is derived solely from resolved and unresolved requested-type counts.
- Contradictions, contradiction IDs, and fixed contradiction text are derived solely from normalized facts and exact context.
- Extra model-authored IDs, fact keys, standalone edges, contradictions, explanations, `coverage_note`, or `document_reviews` fail exact-shape validation.
- A direct regression proves that a source sentence saying it does not establish authenticity or prove fraud does not self-trigger rejection.
- The validator prompt rejects forbidden judgments in every semantic candidate field; there is no model-authored stored contradiction prose.

## Other reviewed properties

- Closed document and fact taxonomies; bounded bundle, document, graph, and page sizes.
- Every requested type resolves to supported nodes or is explicitly unresolved.
- Every node has at least one exact verbatim source excerpt.
- Validators assess semantic support, not substring presence alone, against all supplied documents.
- Every document receives exactly one deterministic review consistent with its edge coverage.
- Node, edge, and contradiction IDs are assigned only after deterministic sorting.
- Authenticity, forgery, fraud, title, ownership, legal, customs, and liability judgments are outside the protocol; stored reviews, coverage, disclaimers, and contradiction text are contract-owned.
- Graph writes are atomic and append-only; there are no admin, edit, delete, payout, insurance, escrow, or upgrade methods.
- Bounded read and pagination methods reject missing graphs and unsafe limits.

## Verification

- Current v5 candidate source: 42,460 bytes, 1,041 lines.
- GenVM lint and SDK validation: pass; three lint checks.
- ABI: 14 public methods, one write, thirteen views, zero constructor parameters.
- Strict type check: zero errors, warnings, or information diagnostics.
- Direct tests: 98 passed.
- Five-validator isolated GLSim: 2 passed.
- Combined automated tests: 100 passed.
- ABI SHA-256: `31CD77F8469FBA83BF8AA7B5EA3CA689A44DFBAFD856AD1FC98896094D182794`.

GLSim assertions verify exactly five unanimous votes and five successful validator executions for each consensus-backed graph write. The test runner uses static validator mocks, so it demonstrates full five-validator execution but does not claim heterogeneous model behavior.

Current v5 StudioNet verification deployed the exact frozen source in
`0x72d9d9afe16b93d52524dd30bda4f394ac2da0eb1693e3f706bc313dc35feeab`.
The semantic smoke
`0x3600d494f55ac6c84f863964b98647395a837cc318bf43b20946c2e8d010cb5c`
finalized with majority agreement and successful execution. Exact readback
matched the v5 graph and bundle identities, two documents, five fact nodes,
eight support edges, the ETA revision pair, and zero conflicts or unresolved
types.

The exact v5 source also deployed successfully on Bradbury in
`0xb04426d99ae8c4626bb9b31303ae5915d013a27dcf53c82e36259154229b0e5f`
with five agrees. Its one semantic smoke
`0x2b240e396eb4347f20e50567ad903e3b2b028fb0df61e0d01ac7da0110fa6ea8`
finalized with an `AGREE` result and `FINISHED_WITH_RETURN`; the exposed round
contained three agrees and two timeouts. Exact latest-final readback matches the
expected graph and bundle identities, canonical graph-content hash, complete
manifest/reviews/nodes/edges, bounded typed reads, ETA revision semantics, and
zero contradictions or unresolved types.

Historical v4 StudioNet verification deployed the exact v4 frozen source in transaction
`0xadedd6c36abb43775054ef9330c16d98e79f8d8129682513d898c0ffc744df89`
and stored the example graph in
`0x513241ebe3457595afad7d9ad4d1b70a4739a7fa1edc90a28d65fb97ac786ace`.
Both transactions finalized with agreement and successful execution. Readback
matched the expected v4 bundle and graph identities, five semantic fact nodes,
eight exact support edges, the ETA revision pair, and zero conflicts or
unresolved types.

The identical v4 source then deployed successfully on Bradbury in transaction
`0xa855ffbae9c02fad91133300d0043d7fa0e58121ce794ed6926b43927713ffac`.
It finalized with five agrees, and post-finality reads matched the frozen source,
14-method schema, v4 protocol identities, and zero initial state. The one
authorized semantic smoke
`0x1ac8fdf53c98928a2b83868b9d9f9561b866412299bd12d788796ab42ec9f51a`
finalized with disagreement and `FINISHED_WITH_ERROR`. Round zero produced a
structurally valid, fixture-consistent five-node/eight-edge candidate, but its
vote was two agrees and three timeouts. Rounds one and two instead failed the
deterministic exact-context rule for contradiction endpoints. No graph was
stored in either latest-final or latest-nonfinal state. This bounded observation
did not establish a reproducible source defect; it also did not verify a
Bradbury semantic write. No operator retry, appeal, or manual finalization was
performed. Sanitized records are preserved under explicit `*-policy-v4.json`
filenames and are not v5 evidence. Current sanitized v5 records are
`deployments/studionet.json` and `deployments/bradbury.json`.

The linter emitted only informational code `I200`, noting that a newer runner exists. This build retains the concrete pinned runner required for its frozen verification candidate.

## Residual risks

- Caller-supplied plaintext and provenance labels are unauthenticated and can be false.
- Correlated validators can misunderstand ambiguous, multilingual, OCR-damaged, incomplete, or specialist records.
- Context and revision qualifiers are semantic and can be misclassified despite consensus checks.
- Full plaintext is public transaction calldata and cited excerpts are stored publicly.
- Model unavailability or disagreement can prevent liveness without creating partial state.
- Downstream consumers must pin network, contract address, protocol version, compilation policy version, graph ID, bundle content ID, graph content ID, and finalized successful transaction state.

## Originality statement

CargoFactGraph was implemented as a standalone contract-only project for this task. Its substantive architecture, taxonomy, context model, reconciliation policy, prompts, graph layout, fixtures, tests, and documentation were authored for this project. It has no sibling-project dependency. Generic SDK idioms and a test-only Windows cleanup-order compatibility technique are not project logic.

As a mechanical originality check on v2, 54 distinct non-import contract lines of at least 80 trimmed characters were compared against 35 sibling-project contract sources, with zero exact long-line matches. The exact v5 freeze subsequently passed independent review, local verification, and finalized StudioNet deployment plus semantic-smoke verification. Its exact Bradbury deployment and semantic smoke also finalized successfully with exact latest-final readback, establishing the v5 dual-network semantic pass recorded in the sanitized deployment evidence.
