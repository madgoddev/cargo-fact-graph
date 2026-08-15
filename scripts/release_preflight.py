"""Offline, fail-closed release freeze checks for CargoFactGraph v5."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "contracts" / "cargo_fact_graph.py"
ABI = ROOT / "abi.json"
FIXTURE = ROOT / "examples" / "reconciliation_bundle.json"
PROJECTION = ROOT / "examples" / "leader_candidate.json"

SOURCE_SHA256 = "95CF918C045114337D05F652C586BB9FB77A770F6D342FBBD51964C37A25450A"
SOURCE_BYTES = 42_460
ABI_SHA256 = "31CD77F8469FBA83BF8AA7B5EA3CA689A44DFBAFD856AD1FC98896094D182794"
FIXTURE_SHA256 = "9447D97FDCD563C310D88AFC0E8A59D8FC413301AA5538889A646EBC91F72BB3"
PROJECTION_SHA256 = "69D8035DEEBEC58723E317487F2A4C26763B7C61BF5B4E8F7C30CAFB7098287C"
PROJECTION_BYTES = 1_662
EXPECTED_BUNDLE_ID = (
    "sha256:02cd89465d07b2c4cda57163700e51c3e198c61c338b8314a9064f1232b37aa5"
)
EXPECTED_GRAPH_ID = (
    "cfg5:27fdc4f4c09f19b4556b0f619285e105f4f28db2f9f69d79dbffd7bde63406ed"
)
POLICY_VERSION = "CARGO_FACT_RECONCILIATION/5"
PINNED_DEPENDENCY = (
    '# { "Depends": "py-genlayer:'
    "1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6"
    '" }'
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def canonical(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


def normalized_bundle(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError("fixture root is not an object")
    documents = value.get("documents")
    requested = value.get("requested_fact_types")
    shipment = value.get("shipment_reference")
    if not isinstance(documents, list) or not isinstance(requested, list):
        raise RuntimeError("fixture arrays are missing")
    if not isinstance(shipment, str):
        raise RuntimeError("fixture shipment_reference is missing")
    normalized_documents: list[dict[str, str]] = []
    for document in documents:
        if not isinstance(document, dict):
            raise RuntimeError("fixture document is not an object")
        normalized_documents.append(
            {
                "content": str(document["content"]).strip(),
                "document_id": str(document["document_id"]).strip(),
                "document_type": str(document["document_type"]).strip().upper(),
                "provenance_label": str(document["provenance_label"]).strip(),
            }
        )
    normalized_documents.sort(key=lambda item: item["document_id"])
    return {
        "documents": normalized_documents,
        "requested_fact_types": sorted(str(item).strip().upper() for item in requested),
        "shipment_reference": shipment.strip(),
    }


def main() -> None:
    source = SOURCE.read_bytes()
    abi_bytes = ABI.read_bytes()
    fixture_bytes = FIXTURE.read_bytes()
    projection_bytes = PROJECTION.read_bytes()
    if len(source) != SOURCE_BYTES or sha256(source) != SOURCE_SHA256:
        raise RuntimeError("contract source release freeze mismatch")
    source_text = source.decode("utf-8")
    if source_text.splitlines()[0] != PINNED_DEPENDENCY:
        raise RuntimeError("pinned GenVM dependency header mismatch")
    if "py-genlayer:test" in source_text or "py-genlayer:latest" in source_text:
        raise RuntimeError("local-only GenVM runner alias found")
    if sha256(abi_bytes) != ABI_SHA256:
        raise RuntimeError("ABI release freeze mismatch")
    if sha256(fixture_bytes) != FIXTURE_SHA256:
        raise RuntimeError("fixture release freeze mismatch")
    if sha256(projection_bytes) != PROJECTION_SHA256:
        raise RuntimeError("semantic projection fixture freeze mismatch")
    projection = json.loads(projection_bytes)
    if set(projection) != {"fact_nodes", "unresolved_fact_types"}:
        raise RuntimeError("semantic projection root shape mismatch")
    if len(canonical(projection).encode("utf-8")) != PROJECTION_BYTES:
        raise RuntimeError("semantic projection canonical byte count mismatch")
    if any(
        forbidden in canonical(projection)
        for forbidden in ('"fact_key"', '"support_edges"', '"contradictions"')
    ):
        raise RuntimeError("legacy high-entropy projection field found")

    abi = json.loads(abi_bytes)
    methods = abi.get("methods")
    ctor = abi.get("ctor")
    if not isinstance(methods, dict) or not isinstance(ctor, dict):
        raise RuntimeError("ABI root shape mismatch")
    views = sum(method.get("readonly") is True for method in methods.values())
    writes = sum(method.get("readonly") is not True for method in methods.values())
    if (
        len(methods) != 14
        or views != 13
        or writes != 1
        or ctor.get("params") != []
        or set(methods) != {
            "create_graph",
            "derive_bundle_identity",
            "get_contradictions_page",
            "get_document_manifest",
            "get_document_reviews",
            "get_fact_nodes_page",
            "get_facts_by_type",
            "get_graph_header",
            "get_graph_payload",
            "get_protocol",
            "get_support_edges_page",
            "get_unresolved_fact_types",
            "has_graph",
            "list_graph_ids",
        }
    ):
        raise RuntimeError("ABI public surface mismatch")

    bundle_text = canonical(normalized_bundle(json.loads(fixture_bytes)))
    bundle_digest = hashlib.sha256(bundle_text.encode("utf-8")).hexdigest()
    graph_digest = hashlib.sha256(
        (POLICY_VERSION + "\x00" + bundle_text).encode("utf-8")
    ).hexdigest()
    bundle_id = f"sha256:{bundle_digest}"
    graph_id = f"cfg5:{graph_digest}"
    if bundle_id != EXPECTED_BUNDLE_ID or graph_id != EXPECTED_GRAPH_ID:
        raise RuntimeError("fixture content identity mismatch")

    print(
        json.dumps(
            {
                "abiSha256": ABI_SHA256,
                "bundleContentId": bundle_id,
                "constructorParameterCount": 0,
                "fixtureSha256": FIXTURE_SHA256,
                "graphId": graph_id,
                "projectionCanonicalBytes": PROJECTION_BYTES,
                "projectionSha256": PROJECTION_SHA256,
                "publicMethodCount": 14,
                "sourceBytes": SOURCE_BYTES,
                "sourceSha256": SOURCE_SHA256,
                "status": "PASS",
                "viewMethodCount": 13,
                "writeMethodCount": 1,
            },
            separators=(",", ":"),
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
