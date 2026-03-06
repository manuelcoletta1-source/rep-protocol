import json
import hashlib
import base64
import sys
import urllib.request
import urllib.error

DEFAULT_URL = "http://127.0.0.1:8080/export-evidence-signed"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def canonical_evidence_payload(evidence: dict) -> str:
    payload = {
        "status": evidence["status"],
        "event_count": evidence["event_count"],
        "last_event_id": evidence["last_event_id"],
        "last_event_hash": evidence["last_event_hash"],
        "final_registry_hash": evidence["final_registry_hash"],
        "generated_at": evidence["generated_at"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def sign(data_hash: str, public_key: str) -> str:
    raw = f"{public_key}:{data_hash}"
    return base64.b64encode(raw.encode()).decode()


def fetch_json(url: str) -> dict:
    try:
        with urllib.request.urlopen(url) as response:
            if response.status != 200:
                raise Exception(f"unexpected HTTP status {response.status}")
            body = response.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.URLError as e:
        raise Exception(f"network error: {e.reason}")
    except json.JSONDecodeError:
        raise Exception("invalid JSON response")


def validate_exported_payload(data: dict) -> dict:
    required_top = ["status", "file", "signed_evidence"]
    for field in required_top:
        if field not in data:
            raise Exception(f"missing top-level field: {field}")

    if data["status"] != "EXPORTED":
        raise Exception("remote node did not return EXPORTED status")

    signed = data["signed_evidence"]

    required_signed = ["evidence", "evidence_hash", "public_key", "signature"]
    for field in required_signed:
        if field not in signed:
            raise Exception(f"missing signed evidence field: {field}")

    evidence = signed["evidence"]

    required_evidence = [
        "status",
        "event_count",
        "last_event_id",
        "last_event_hash",
        "final_registry_hash",
        "generated_at",
    ]

    for field in required_evidence:
        if field not in evidence:
            raise Exception(f"missing evidence field: {field}")

    if evidence["status"] not in ["PASS", "FAIL"]:
        raise Exception("invalid evidence status")

    if not isinstance(evidence["event_count"], int):
        raise Exception("event_count must be integer")

    return signed


def verify_signed_evidence(signed: dict) -> None:
    evidence = signed["evidence"]
    evidence_hash = signed["evidence_hash"]
    public_key = signed["public_key"]
    signature = signed["signature"]

    recomputed_hash = sha256_hex(canonical_evidence_payload(evidence))
    if recomputed_hash != evidence_hash:
        raise Exception("evidence_hash mismatch")

    expected_signature = sign(evidence_hash, public_key)
    if expected_signature != signature:
        raise Exception("signature mismatch")


def main() -> None:
    url = DEFAULT_URL

    if len(sys.argv) > 1:
        url = sys.argv[1]

    data = fetch_json(url)
    signed = validate_exported_payload(data)
    verify_signed_evidence(signed)

    print("PASS: remote signed evidence is valid")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
