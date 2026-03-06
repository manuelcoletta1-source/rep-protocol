import json
import hashlib
import datetime
import os
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

REGISTRY_FILE = "rep-registry.json"
ACTOR_FILE = "rep-actors.json"
EVIDENCE_FILE = "rep-evidence.json"
SIGNED_EVIDENCE_FILE = "rep-evidence-signed.json"
HOST = "0.0.0.0"
PORT = 8080


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode()).hexdigest()


def utc_now():
    return datetime.datetime.utcnow().isoformat() + "Z"


def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)


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
        "prev_hash": event["prev_hash"]
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def canonical_evidence_payload(evidence):
    payload = {
        "status": evidence["status"],
        "event_count": evidence["event_count"],
        "last_event_id": evidence["last_event_id"],
        "last_event_hash": evidence["last_event_hash"],
        "final_registry_hash": evidence["final_registry_hash"],
        "generated_at": evidence["generated_at"]
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))


def sign(data_hash, public_key):
    raw = f"{public_key}:{data_hash}"
    return base64.b64encode(raw.encode()).decode()


def verify_signature(data_hash, public_key, signature):
    return sign(data_hash, public_key) == signature


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


def ensure_genesis():
    registry = load_json(REGISTRY_FILE, [])

    if len(registry) == 0:
        registry.append(create_genesis())
        save_json(REGISTRY_FILE, registry)


def next_event_id(registry):
    return f"EVT-{len(registry):04d}"


def create_event(actor_ipr, decision, cost, trace_input, event_type="operation"):
    registry = load_json(REGISTRY_FILE, [])
    actors = load_json(ACTOR_FILE, {})

    if actor_ipr not in actors:
        raise ValueError("Unknown actor")

    public_key = actors[actor_ipr]["public_key"]
    prev_hash = registry[-1]["event_hash"]

    event = {
        "event_id": next_event_id(registry),
        "event_type": event_type,
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
        if verify_event(event, prev) != "PASS":
            return "FAIL"
        prev = event["event_hash"]

    return "PASS"


def append_event(event):
    registry = load_json(REGISTRY_FILE, [])
    registry.append(event)
    save_json(REGISTRY_FILE, registry)


def chain_hash():
    registry = load_json(REGISTRY_FILE, [])

    return sha256_hex(
        "".join(event["event_hash"] for event in registry)
    )


def build_evidence():
    registry = load_json(REGISTRY_FILE, [])
    verification = verify_registry()

    if registry:
        last_event = registry[-1]
        last_event_hash = last_event["event_hash"]
        last_event_id = last_event["event_id"]
    else:
        last_event_hash = None
        last_event_id = None

    return {
        "status": verification,
        "event_count": len(registry),
        "last_event_id": last_event_id,
        "last_event_hash": last_event_hash,
        "final_registry_hash": chain_hash(),
        "generated_at": utc_now()
    }


def build_signed_evidence():
    evidence = build_evidence()
    evidence_hash = sha256_hex(canonical_evidence_payload(evidence))
    public_key = "HBCE-EVIDENCE-PUBKEY"
    signature = sign(evidence_hash, public_key)

    return {
        "evidence": evidence,
        "evidence_hash": evidence_hash,
        "public_key": public_key,
        "signature": signature
    }


class REPHandler(BaseHTTPRequestHandler):

    def _send(self, code, payload):
        body = json.dumps(payload, indent=2).encode()

        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):

        if self.path == "/registry":
            self._send(200, load_json(REGISTRY_FILE, []))
            return

        if self.path == "/verify":
            self._send(200, {"registry_verification": verify_registry()})
            return

        if self.path == "/evidence":
            self._send(200, build_evidence())
            return

        if self.path == "/export-evidence":
            evidence = build_evidence()
            save_json(EVIDENCE_FILE, evidence)

            self._send(200, {
                "status": "EXPORTED",
                "file": EVIDENCE_FILE,
                "evidence": evidence
            })
            return

        if self.path == "/export-evidence-signed":
            signed_evidence = build_signed_evidence()
            save_json(SIGNED_EVIDENCE_FILE, signed_evidence)

            self._send(200, {
                "status": "EXPORTED",
                "file": SIGNED_EVIDENCE_FILE,
                "signed_evidence": signed_evidence
            })
            return

        if self.path == "/chain-hash":
            self._send(200, {
                "status": verify_registry(),
                "event_count": len(load_json(REGISTRY_FILE, [])),
                "chain_hash": chain_hash(),
                "generated_at": utc_now()
            })
            return

        self._send(404, {"error": "Not found"})

    def do_POST(self):

        if self.path != "/event":
            self._send(404, {"error": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(content_length)

        data = json.loads(raw)

        event = create_event(
            actor_ipr=data["actor_ipr"],
            decision=data["decision"],
            cost=data["cost"],
            trace_input=data["trace_input"],
            event_type=data.get("event_type", "operation")
        )

        append_event(event)

        self._send(201, {
            "status": "PASS",
            "event": event
        })

    def log_message(self, format, *args):
        return


def main():
    ensure_genesis()

    server = HTTPServer((HOST, PORT), REPHandler)

    print(f"REP node API running on http://{HOST}:{PORT}")
    print("GET  /registry")
    print("GET  /verify")
    print("GET  /evidence")
    print("GET  /export-evidence")
    print("GET  /export-evidence-signed")
    print("GET  /chain-hash")
    print("POST /event")

    server.serve_forever()


if __name__ == "__main__":
    main()
