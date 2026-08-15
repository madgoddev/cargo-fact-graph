import json
from pathlib import Path

import pytest
from genlayer_py.types import SimConfig
from gltest import get_contract_factory, get_validator_factory
from gltest.assertions import tx_execution_succeeded
from gltest.clients import get_gl_client
from gltest.utils import extract_contract_address


ROOT = Path(__file__).resolve().parents[2]


def validator_context(candidate: dict) -> dict:
    audit = {
        "verdict": "ACCEPT",
        "issue_code": "NONE",
    }
    mock_responses = {
        "nondet_exec_prompt": {
            r"(?s).*producing a bounded shipping-document fact reconciliation graph.*": json.dumps(
                candidate
            ),
            r"(?s).*independent validator of a proposed CargoFactGraph.*": json.dumps(
                audit
            ),
        },
        "eq_principle_prompt_comparative": {},
        "eq_principle_prompt_non_comparative": {},
    }
    validators = get_validator_factory().batch_create_mock_validators(
        count=5, mock_llm_response=mock_responses
    )
    return {"validators": [validator.to_dict() for validator in validators]}


@pytest.fixture(scope="module")
def deployed_address() -> str:
    factory = get_contract_factory("CargoFactGraph")
    receipt = factory.deploy_contract_tx(args=[])
    assert tx_execution_succeeded(receipt)
    return extract_contract_address(receipt)


def read(address: str, function_name: str, args: list):
    return get_gl_client().read_contract(
        address=address,
        function_name=function_name,
        args=args,
    )


def write(address: str, function_name: str, args: list, context: dict) -> dict:
    client = get_gl_client()
    tx_hash = client.write_contract(
        address=address,
        function_name=function_name,
        args=args,
        sim_config=SimConfig(**context),
    )
    return client.wait_for_transaction_receipt(
        transaction_hash=tx_hash,
        interval=0.1,
        retries=100,
    )


def assert_five_validator_agreement(receipt: dict) -> None:
    consensus = receipt["consensus_data"]
    assert len(consensus["votes"]) == 5
    assert set(consensus["votes"].values()) == {"agree"}
    assert len(consensus["validators"]) == 5
    assert all(
        validator["execution_result"] == "SUCCESS"
        for validator in consensus["validators"]
    )


@pytest.mark.integration
def test_five_validator_reconciliation_flow(deployed_address):
    bundle = json.loads((ROOT / "examples" / "reconciliation_bundle.json").read_text("utf-8"))
    candidate = json.loads((ROOT / "examples" / "leader_candidate.json").read_text("utf-8"))
    context = validator_context(candidate)
    assert len(context["validators"]) == 5
    identity = read(deployed_address, "derive_bundle_identity", [json.dumps(bundle)])
    receipt = write(
        deployed_address,
        "create_graph",
        [json.dumps(bundle)],
        context,
    )
    assert tx_execution_succeeded(receipt)
    assert_five_validator_agreement(receipt)

    assert read(deployed_address, "has_graph", [identity["graph_id"]]) is True
    header = read(deployed_address, "get_graph_header", [identity["graph_id"]])
    payload = json.loads(
        read(deployed_address, "get_graph_payload", [identity["graph_id"]])
    )

    assert header["graph_id"] == identity["graph_id"]
    assert header["bundle_content_id"] == identity["bundle_content_id"]
    assert header["document_count"] == 2
    assert header["fact_node_count"] == 5
    assert header["support_edge_count"] == 8
    assert header["contradiction_count"] == 0
    assert header["unresolved_fact_type_count"] == 0
    assert payload["protocol_version"] == "CARGO_FACT_GRAPH/5"
    assert payload["compilation_policy_version"] == "CARGO_FACT_RECONCILIATION/5"
    assert payload["stored_narrative_policy"] == "DETERMINISTIC_CONTRACT_TEMPLATES"
    assert {item["document_id"] for item in payload["document_reviews"]} == {
        "BL-041",
        "ARRIVAL-041",
    }
    assert all(item["evidence_excerpt"] for item in payload["support_edges"])
    assert all(
        item["note"]
        == "This document supplies at least one support edge for a requested fact."
        for item in payload["document_reviews"]
    )
    assert payload["coverage_note"] == (
        "Every requested fact type has one or more supported nodes."
    )
    assert "authenticity" in payload["scope_disclaimer"].lower()


@pytest.mark.integration
def test_five_validator_result_supports_bounded_pages_and_content_identity(
    deployed_address,
):
    bundle = json.loads((ROOT / "examples" / "reconciliation_bundle.json").read_text("utf-8"))
    bundle["shipment_reference"] = "DEMO-SHIPMENT-2026-042"
    candidate = json.loads((ROOT / "examples" / "leader_candidate.json").read_text("utf-8"))
    context = validator_context(candidate)
    receipt = write(
        deployed_address,
        "create_graph",
        [json.dumps(bundle)],
        context,
    )
    assert tx_execution_succeeded(receipt)
    assert_five_validator_agreement(receipt)

    identity = read(deployed_address, "derive_bundle_identity", [json.dumps(bundle)])
    first_page = json.loads(
        read(deployed_address, "get_fact_nodes_page", [identity["graph_id"], 0, 2])
    )
    second_page = json.loads(
        read(deployed_address, "get_fact_nodes_page", [identity["graph_id"], 2, 25])
    )
    header = read(deployed_address, "get_graph_header", [identity["graph_id"]])
    assert len(first_page) == 2
    assert len(first_page) + len(second_page) == header["fact_node_count"]
    assert header["graph_content_id"].startswith("sha256:")
    assert json.loads(
        read(
            deployed_address,
            "get_contradictions_page",
            [identity["graph_id"], 0, 25],
        )
    ) == []
    arrival_nodes = [
        node
        for node in first_page + second_page
        if node["fact_type"] == "ARRIVAL_DATE"
    ]
    assert {node["context"]["record_status"] for node in arrival_nodes} == {
        "CURRENT",
        "SUPERSEDED",
    }
