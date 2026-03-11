from pathlib import Path

import yaml


def test_contracts_are_machine_readable_yaml():
    for path in Path("contracts").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)


def test_ingest_contract_tracks_normalized_model_alignment_targets():
    contract = yaml.safe_load(Path("contracts/ingest_contract.yaml").read_text(encoding="utf-8"))
    tables = contract["ingest"]["normalized_model_alignment"]["supported_contract_tables"]

    assert "document_tags" in tables
    assert "document_aliases" in tables
    assert "document_chunks" in tables
    assert "replay_artifact_links" in tables
