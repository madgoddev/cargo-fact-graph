# Limitations

- Inputs are caller-supplied plaintext. The contract does not fetch, authenticate, timestamp, or prove the existence of a public source.
- Provenance labels are unverified descriptions and may be false or incomplete.
- Content hashes identify the submitted normalized plaintext, not an original PDF, website, signature, or issuing system.
- Semantic consensus can still be wrong, especially with ambiguous, incomplete, multilingual, OCR-corrupted, or domain-specific documents.
- The graph records stated facts and incompatibilities; it does not select a controlling source.
- No authenticity, forgery, fraud, legal validity, ownership, title, customs, sanctions, liability, insurance, payment, or delivery-entitlement conclusion is produced.
- Context qualifiers and revision status are semantic outputs. Validators can still misidentify an entity, role, leg, assertion mode, or whether a record was superseded.
- A contradiction is deterministically limited to different values with the exact same normalized context; a superseded value cannot participate. This favors avoiding false conflict edges and may under-report a conflict when context is ambiguous.
- An original ETA followed by a revised ETA is represented as a temporal revision, not a contradiction. Estimated, scheduled, and actual dates remain distinct assertion modes.
- The closed taxonomy intentionally excludes arbitrary caller-defined predicates.
- Full input plaintext is visible in transaction calldata even though storage retains only hashes and cited excerpts. Do not submit confidential or personal documents.
- Downstream contracts must pin the network, contract address, protocol version, compilation policy version, graph ID, bundle content ID, and graph content ID, then apply their own domain rules.
