# Reconstructible Event Protocol (REP)

Experimental protocol and reference node for reconstructible operational events.

REP defines a minimal event model based on four conditions:

Decision  
Cost  
Trace  
Time  

An event is considered operationally valid only when these conditions remain reconstructible.

---

## Repository Purpose

This repository contains:

- the REP protocol draft
- the REP reference node
- protocol documentation
- evidence export and verification utilities

The goal is to provide a minimal but functional framework for:

- append-only event recording
- deterministic registry verification
- chain checkpoint generation
- portable evidence export
- signed evidence export
- offline and remote evidence validation

---

## Core Event Model

A REP event is represented as an Event Unit containing:

event_id  
event_type  
actor_ipr  
decision  
cost  
trace  
time_start  
time_end  
prev_hash  
public_key  
event_hash  
signature  

Each event is linked to the previous one through `prev_hash`, creating a verifiable event chain.

---

## Available Components

### REP Node

Main file:

rep-node.py

The node exposes an HTTP API for event recording, registry verification, evidence generation, signed evidence export, and registry checkpoint calculation.

### Actor Registry

File:

rep-actors.json

Maps actors to their public keys.

### Offline Verifiers

Files:

rep-verify-evidence.py  
rep-verify-signed-evidence.py  

These scripts verify exported evidence files independently of the running node.

### Remote Verifier

File:

rep-remote-verifier.py

This script retrieves signed evidence directly from a running REP node and verifies it remotely.

---

## API Endpoints

The REP node exposes the following endpoints:

GET /registry  
GET /verify  
GET /evidence  
GET /export-evidence  
GET /export-evidence-signed  
GET /chain-hash  
POST /event  

### Endpoint Roles

**GET /registry**  
Returns the current append-only event registry.

**GET /verify**  
Returns the deterministic verification result of the registry.

**GET /evidence**  
Returns an evidence snapshot of the current registry state.

**GET /export-evidence**  
Exports an evidence snapshot to `rep-evidence.json`.

**GET /export-evidence-signed**  
Exports a signed evidence snapshot to `rep-evidence-signed.json`.

**GET /chain-hash**  
Returns the cumulative hash checkpoint of the full event chain.

**POST /event**  
Creates and appends a new event to the registry.

---

## Runtime Files

The node generates runtime files that are intentionally excluded from version control:

rep-registry.json  
rep-evidence.json  
rep-evidence-signed.json  

These files represent operational state, not source code.

---

## Start the Node

From Linux:

```bash
cd /home/manuelcoletta1/rep-protocol && python3 rep-node.py

Expected banner:

REP node API running on http://0.0.0.0:8080
GET  /registry
GET  /verify
GET  /evidence
GET  /export-evidence
GET  /export-evidence-signed
GET  /chain-hash
POST /event


---

Minimal Operational Flow

1. Verify registry

curl http://127.0.0.1:8080/verify

2. Read chain checkpoint

curl http://127.0.0.1:8080/chain-hash

3. Create an event

curl -X POST http://127.0.0.1:8080/event -H "Content-Type: application/json" -d '{"actor_ipr":"IPR-3","decision":"deploy configuration update","cost":"compute resources","trace_input":"deployment log example","event_type":"operation"}'

4. Export evidence

curl http://127.0.0.1:8080/export-evidence

5. Export signed evidence

curl http://127.0.0.1:8080/export-evidence-signed


---

Verified Example Flow

The following sequence demonstrates the expected REP behavior.

Initial registry state

The node starts with a genesis event:

EVT-0000

Initial verification:

curl http://127.0.0.1:8080/verify

Example result:

{
  "registry_verification": "PASS"
}

Initial chain checkpoint:

curl http://127.0.0.1:8080/chain-hash

Example result:

{
  "status": "PASS",
  "event_count": 1,
  "chain_hash": "ad01602f41c19670589321b041eae1982a6622123f8de1fff351d9f51a29367b",
  "generated_at": "2026-03-06T15:21:16.497821Z"
}

Append a new event

curl -X POST http://127.0.0.1:8080/event -H "Content-Type: application/json" -d '{"actor_ipr":"IPR-3","decision":"deploy configuration update","cost":"compute resources","trace_input":"deployment log example","event_type":"operation"}'

Example result:

{
  "status": "PASS",
  "event": {
    "event_id": "EVT-0001",
    "event_type": "operation",
    "actor_ipr": "IPR-3",
    "decision": "deploy configuration update",
    "cost": "compute resources",
    "trace": "47c6e4230d491d6880e3e28eabdf85ac807481adf43677b7dfe38bbd352c33c6",
    "time_start": "2026-03-06T16:10:21.545011Z",
    "time_end": "2026-03-06T16:10:21.545026Z",
    "prev_hash": "f64ca38f2d021ef9c822c19ab29ac4ff2f9773a8ec14685aca425eedc37a6a40",
    "public_key": "HBCE-PUBKEY-IPR-3",
    "event_hash": "b79490d99c57248416a753c78a13c359b318494051086ef93596f71cf510ca3a",
    "signature": "SEJDRS1QVUJLRVktSVBSLTM6Yjc5NDkwZDk5YzU3MjQ4NDE2YTc1M2M3OGExM2MzNTliMzE4NDk0MDUxMDg2ZWY5MzU5NmY3MWNmNTEwY2EzYQ=="
  }
}

Registry state after append

curl http://127.0.0.1:8080/chain-hash

Example result:

{
  "status": "PASS",
  "event_count": 2,
  "chain_hash": "35697a0b3dac5d936cb097d4255984d04fb6b4870fe91817859e802c9d0c341b",
  "generated_at": "2026-03-06T16:10:47.888103Z"
}

This demonstrates the expected REP property:

appending an event increases event_count

appending an event changes chain_hash

registry verification remains PASS


Export signed evidence

curl http://127.0.0.1:8080/export-evidence-signed

Example result:

{
  "status": "EXPORTED",
  "file": "rep-evidence-signed.json",
  "signed_evidence": {
    "evidence": {
      "status": "PASS",
      "event_count": 1,
      "last_event_id": "EVT-0000",
      "last_event_hash": "f64ca38f2d021ef9c822c19ab29ac4ff2f9773a8ec14685aca425eedc37a6a40",
      "final_registry_hash": "ad01602f41c19670589321b041eae1982a6622123f8de1fff351d9f51a29367b",
      "generated_at": "2026-03-06T15:35:39.628828Z"
    },
    "evidence_hash": "7e3d2c7bb4379a012d2bcbed9250dcdc00072bd5a1c0d3bd3bf67985a69ae9df",
    "public_key": "HBCE-EVIDENCE-PUBKEY",
    "signature": "SEJDRS1FVklERU5DRS1QVUJLRVk6N2UzZDJjN2JiNDM3OWEwMTJkMmJjYmVkOTI1MGRjZGMwMDA3MmJkNWExYzBkM2JkM2JmNjc5ODVhNjlhZTlkZg=="
  }
}


---

Offline Verification

Verify plain evidence

python3 rep-verify-evidence.py

Verify signed evidence

python3 rep-verify-signed-evidence.py

These verifiers allow exported files to be checked independently from the active node.


---

Remote Verification

The remote verifier requests signed evidence from a running REP node and validates it independently.

Run:

python3 rep-remote-verifier.py

Expected result:

PASS: remote signed evidence is valid

This verifies:

remote payload structure

evidence hash correctness

deterministic signature correctness



---

Evidence Model

A REP evidence object contains:

status
event_count
last_event_id
last_event_hash
final_registry_hash
generated_at

A signed evidence object contains:

evidence
evidence_hash
public_key
signature

This allows the registry state to be exported, hashed, signed, and verified offline or remotely.


---

Protocol Properties

REP provides a minimal structure for:

append-only recording

deterministic verification

hash-linked event sequencing

actor-bound event generation

cumulative registry checkpointing

portable registry evidence

signed integrity attestations

offline verification

remote signed evidence verification



---

Current Status

REP is an experimental protocol and node prototype.

The repository currently demonstrates:

operational event creation

genesis event initialization

append-only registry persistence

registry verification

chain hash calculation

evidence export

signed evidence export

offline verification tools

remote signed evidence verification



---

Author

Manuel Coletta
HERMETICUM B.C.E. S.r.l.


