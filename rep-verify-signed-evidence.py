import json
import os
import sys
import hashlib
import base64

REQUIRED_EVIDENCE_FIELDS = [
    "status",
    "event_count",
    "last_event_id",
    "last_event_hash",
    "final_registry_hash",
    "generated_at",
]

REQUIRED_SIGNED_FIELDS = [
    "evidence",
    "evidence_hash",
    "public_key",
    "signature",
]


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def canonical_evidence_payload(evidence):
    payload = {
        "status": evidence["status"],
        "event_count": evidence["event_count"],
        "last_event_id": evidence["last_event_id"],
        "last_event_hash": evidence["last_event_hash"],
        "final_registry_hash": evidence["final_registry_hash"],
        "generated_at": evidence["generated_at"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def sign(data_hash, public_key):
    raw = f"{public_key}:{data_hash}"
    return base64.b64encode(raw.encode()).decode()


def load_signed_evidence(path):

    if not os.path.exists(path):
        print("FAIL: signed evidence file not found")
        sys.exit(1)

    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            print("FAIL: invalid JSON")
            sys.exit(1)


def validate_signed_structure(data):

    for field in REQUIRED_SIGNED_FIELDS:
        if field not in data:
            print(f"FAIL: missing field {field}")
            sys.exit(1)

    evidence = data["evidence"]

    if not isinstance(evidence, dict):
        print("FAIL: evidence must be an object")
        sys.exit(1)

    for field in REQUIRED_EVIDENCE_FIELDS:
        if field not in evidence:
            print(f"FAIL: missing evidence field {field}")
            sys.exit(1)

    if evidence["status"] not in ["PASS", "FAIL"]:
        print("FAIL: invalid evidence status")
        sys.exit(1)

    if not isinstance(evidence["event_count"], int):
        print("FAIL: event_count must be integer")
        sys.exit(1)


def verify_evidence_hash(data):

    evidence = data["evidence"]
    expected_hash = sha256_hex(canonical_evidence_payload(evidence))

    if expected_hash != data["evidence_hash"]:
        print("FAIL: evidence_hash mismatch")
        sys.exit(1)


def verify_signature(data):

    expected_signature = sign(data["evidence_hash"], data["public_key"])

    if expected_signature != data["signature"]:
        print("FAIL: signature mismatch")
        sys.exit(1)


def main():

    filename = "rep-evidence-signed.json"

    if len(sys.argv) > 1:
        filename = sys.argv[1]

    data = load_signed_evidence(filename)

    validate_signed_structure(data)
    verify_evidence_hash(data)
    verify_signature(data)

    print("PASS: signed evidence is valid")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
