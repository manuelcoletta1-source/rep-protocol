import json
import hashlib
import datetime
import os

REGISTRY_FILE = "rep-registry.json"
DEFAULT_ACTOR_IPR = "IPR-3"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def utc_now() -> str:
    return datetime.datetime.utcnow().isoformat() + "Z"


def load_registry() -> list:
    if not os.path.exists(REGISTRY_FILE):
        return []

    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []


def save_registry(registry: list) -> None:
    with open(REGISTRY_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2)


def canonical_event_payload(event: dict) -> str:
    payload = {
        "event_id": event["event_id"],
        "actor_ipr": event["actor_ipr"],
        "decision": event["decision"],
        "cost": event["cost"],
        "trace": event["trace"],
        "time_start": event["time_start"],
        "time_end": event["time_end"],
        "prev_hash": event["prev_hash"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def create_event(
    event_id: str,
    actor_ipr: str,
    decision: str,
    cost: str,
    trace_input: str,
    prev_hash: str,
) -> dict:
    time_start = utc_now()
    time_end = time_start

    event = {
        "event_id": event_id,
        "actor_ipr": actor_ipr,
        "decision": decision,
        "cost": cost,
        "trace": sha256_hex(trace_input),
        "time_start": time_start,
        "time_end": time_end,
        "prev_hash": prev_hash,
    }

    event["event_hash"] = sha256_hex(canonical_event_payload(event))
    return event


def append_event(event: dict) -> None:
    registry = load_registry()
    registry.append(event)
    save_registry(registry)


def verify_event(event: dict, expected_prev_hash: str) -> str:
    required = [
        "event_id",
        "actor_ipr",
        "decision",
        "cost",
        "trace",
        "time_start",
        "time_end",
        "prev_hash",
        "event_hash",
    ]

    for field in required:
        if field not in event or not event[field]:
            return "FAIL"

    if event["prev_hash"] != expected_prev_hash:
        return "FAIL"

    recalculated_hash = sha256_hex(canonical_event_payload(event))
    if event["event_hash"] != recalculated_hash:
        return "FAIL"

    return "PASS"


def verify_registry(registry: list) -> str:
    expected_prev_hash = "GENESIS"

    for event in registry:
        result = verify_event(event, expected_prev_hash)
        if result != "PASS":
            return "FAIL"
        expected_prev_hash = event["event_hash"]

    return "PASS"


def next_event_id(registry: list) -> str:
    return f"EVT-{len(registry) + 1:04d}"


def main() -> None:
    registry = load_registry()
    prev_hash = registry[-1]["event_hash"] if registry else "GENESIS"

    event = create_event(
        event_id=next_event_id(registry),
        actor_ipr=DEFAULT_ACTOR_IPR,
        decision="deploy configuration update",
        cost="compute resources",
        trace_input="deployment log example",
        prev_hash=prev_hash,
    )

    event_result = verify_event(event, prev_hash)
    if event_result != "PASS":
        print("Event verification:", event_result)
        print(json.dumps(event, indent=2))
        return

    append_event(event)

    updated_registry = load_registry()
    registry_result = verify_registry(updated_registry)

    print("Event verification:", event_result)
    print("Registry verification:", registry_result)
    print(json.dumps(event, indent=2))


if __name__ == "__main__":
    main()
