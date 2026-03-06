import json
import hashlib
import datetime

REGISTRY_FILE = "rep-registry.json"


def hash_trace(data):
    return hashlib.sha256(data.encode()).hexdigest()


def create_event(event_id, decision, cost, trace):
    time_start = datetime.datetime.utcnow().isoformat() + "Z"
    time_end = time_start

    event = {
        "event_id": event_id,
        "decision": decision,
        "cost": cost,
        "trace": hash_trace(trace),
        "time_start": time_start,
        "time_end": time_end
    }

    return event


def append_event(event):
    try:
        with open(REGISTRY_FILE, "r") as f:
            registry = json.load(f)
    except:
        registry = []

    registry.append(event)

    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def verify_event(event):
    required = ["decision", "cost", "trace", "time_start", "time_end"]

    for r in required:
        if r not in event or not event[r]:
            return "FAIL"

    return "PASS"


def main():
    event = create_event(
        "EVT-0001",
        "deploy configuration update",
        "compute resources",
        "deployment log example"
    )

    append_event(event)

    result = verify_event(event)

    print("Verification:", result)
    print(json.dumps(event, indent=2))


if __name__ == "__main__":
    main()
