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
- signed evidence verification

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

The node exposes an HTTP API for event recording, registry verification, evidence generation, and signed evidence export.

### Actor Registry

File:

rep-actors.json

Maps actors to their public keys.

### Offline Verifiers

Files:

rep-verify-evidence.py  
rep-verify-signed-evidence.py  

These scripts verify exported evidence files independently of the running node.

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

Offline Verification

Verify plain evidence

python3 rep-verify-evidence.py

Verify signed evidence

python3 rep-verify-signed-evidence.py

These verifiers allow exported files to be checked independently from the active node.


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

This allows the registry state to be exported, hashed, signed, and verified offline.


---

Protocol Properties

REP provides a minimal structure for:

append-only recording

deterministic verification

hash-linked event sequencing

actor-bound event generation

portable registry evidence

signed integrity attestations



---

Current Status

REP is an experimental protocol and node prototype.

The repository currently demonstrates:

operational event creation

registry verification

chain checkpoint generation

evidence export

signed evidence export

offline verification of evidence files



---

Author

Manuel Coletta
HERMETICUM B.C.E. S.r.l.

