import json
import hashlib
import datetime
import os
import base64

REGISTRY_FILE = "rep-registry.json"
ACTOR_FILE = "rep-actors.json"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def utc_now():
    return datetime.datetime.utcnow().isoformat() + "Z"


def load_json(path, default):
    if not os.path.exists(path):
        return default

    with open(path) as f:
        try:
            return json.load(f)
        except:
            return default


def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def canonical_payload(event):
    payload = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "actor_ipr": event["actor_ipr"],
        "decision": event["decision"],
        "cost": event["cost"],
        "trace": event["trace"],
        "time_start": event["time_start"],
        "time_end": event["time_end"],
        "prev_hash": event["prev_hash"],
    }

    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def sign(event_hash, public_key):
    raw = f"{public_key}:{event_hash}"
    return base64.b64encode(raw.encode()).decode()


def verify_signature(event_hash, public_key, signature):
    return sign(event_hash, public_key) == signature


def create_genesis():
    event = {
        "event_id": "EVT-0000",
        "event_type": "genesis",
        "actor_ipr": "SYSTEM",
        "decision": "initialize registry",
        "cost": "none",
        "trace": sha256_hex("genesis"),
        "time_start": utc_now(),
        "time_end": utc_now(),
        "prev_hash": "NONE",
        "public_key": "SYSTEM"
    }

    event["event_hash"] = sha256_hex(canonical_payload(event))
    event["signature"] = "GENESIS"

    return event


def create_event(actor_ipr, decision, cost, trace_input):
    registry = load_json(REGISTRY_FILE, [])
    actors = load_json(ACTOR_FILE, {})

    if actor_ipr not in actors:
        raise Exception("Unknown actor")

    public_key = actors[actor_ipr]["public_key"]
    prev_hash = registry[-1]["event_hash"]

    event = {
        "event_id": f"EVT-{len(registry):04d}",
        "event_type": "operation",
        "actor_ipr": actor_ipr,
        "decision": decision,
        "cost": cost,
        "trace": sha256_hex(trace_input),
        "time_start": utc_now(),
        "time_end": utc_now(),
        "prev_hash": prev_hash,
        "public_key": public_key
    }

    event["event_hash"] = sha256_hex(canonical_payload(event))
    event["signature"] = sign(event["event_hash"], public_key)

    return event


def verify_event(event, expected_prev):
    required = [
        "event_id",
        "event_type",
        "actor_ipr",
        "decision",
        "cost",
        "trace",
        "time_start",
        "time_end",
        "prev_hash",
        "event_hash",
        "public_key",
        "signature"
    ]

    for r in required:
        if r not in event:
            return "FAIL"

    if event["prev_hash"] != expected_prev:
        return "FAIL"

    if sha256_hex(canonical_payload(event)) != event["event_hash"]:
        return "FAIL"

    if event["event_type"] != "genesis":
        if not verify_signature(event["event_hash"], event["public_key"], event["signature"]):
            return "FAIL"

    return "PASS"


def verify_registry():
    registry = load_json(REGISTRY_FILE, [])
    prev = "NONE"

    for event in registry:
        result = verify_event(event, prev)

        if result != "PASS":
            return "FAIL"

        prev = event["event_hash"]

    return "PASS"


def ensure_genesis():
    registry = load_json(REGISTRY_FILE, [])

    if len(registry) == 0:
        genesis = create_genesis()
        registry.append(genesis)
        save_json(REGISTRY_FILE, registry)


def main():
    ensure_genesis()

    event = create_event(
        "IPR-3",
        "deploy configuration update",
        "compute resources",
        "deployment log example"
    )

    registry = load_json(REGISTRY_FILE, [])
    registry.append(event)
    save_json(REGISTRY_FILE, registry)

    print("Event created")
    print(json.dumps(event, indent=2))
    print("\nRegistry verification:", verify_registry())


if __name__ == "__main__":
    main()
