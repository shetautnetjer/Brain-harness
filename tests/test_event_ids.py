from src.brain_harness.events import make_event_id


def test_event_id_uses_uuidv7_shape():
    event_id = make_event_id()
    _, raw = event_id.split("_", maxsplit=1)

    assert event_id.startswith("evt_")
    assert raw[14] == "7"
    assert raw[19] in {"8", "9", "a", "b"}


def test_event_ids_are_unique_across_calls():
    ids = {make_event_id() for _ in range(200)}
    assert len(ids) == 200
