from pathlib import Path

import yaml


def test_contracts_are_machine_readable_yaml():
    for path in Path("contracts").glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict)
