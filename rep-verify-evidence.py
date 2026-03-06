import json
import os
import sys

REQUIRED_FIELDS = [
    "status",
    "event_count",
    "last_event_id",
    "last_event_hash",
    "final_registry_hash",
    "generated_at",
]


def load_evidence(path):

    if not os.path.exists(path):
        print("FAIL: evidence file not found")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            print("FAIL: invalid JSON")
            sys.exit(1)


def validate_structure(evidence):

    for field in REQUIRED_FIELDS:
        if field not in evidence:
            print(f"FAIL: missing field {field}")
            sys.exit(1)

    if evidence["status"] not in ["PASS", "FAIL"]:
        print("FAIL: invalid status")
        sys.exit(1)

    if not isinstance(evidence["event_count"], int):
        print("FAIL: event_count must be integer")
        sys.exit(1)


def main():

    filename = "rep-evidence.json"

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    evidence = load_evidence(filename)

    validate_structure(evidence)

    print("PASS: evidence structure is valid")
    print(json.dumps(evidence, indent=2))


if __name__ == "__main__":
    main()
