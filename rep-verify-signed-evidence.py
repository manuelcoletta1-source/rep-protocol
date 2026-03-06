import json
import hashlib
import base64
import os


EVIDENCE_FILE = "rep-evidence-signed.json"


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def canonical_json(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))


def sign(event_hash, public_key):
    raw = f"{public_key}:{event_hash}"
    return base64.b64encode(raw.encode()).decode()


def verify_signature(event_hash, public_key, signature):
    return sign(event_hash, public_key) == signature


def load_signed_evidence():

    if not os.path.exists(EVIDENCE_FILE):
        raise Exception("rep-evidence-signed.json not found")

    with open(EVIDENCE_FILE, "r") as f:
        return json.load(f)


def verify_signed_evidence():

    data = load_signed_evidence()

    evidence = data["evidence"]
    evidence_hash = data["evidence_hash"]
    public_key = data["public_key"]
    signature = data["signature"]

    recomputed_hash = sha256_hex(canonical_json(evidence))

    if recomputed_hash != evidence_hash:
        print("FAIL: evidence hash mismatch")
        return False

    if not verify_signature(evidence_hash, public_key, signature):
        print("FAIL: signature invalid")
        return False

    print("PASS: signed evidence is valid")
    print(json.dumps(data, indent=2))

    return True


def main():

    verify_signed_evidence()


if __name__ == "__main__":
    main()
