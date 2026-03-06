# REP Evidence Example

This document shows how to obtain a registry evidence snapshot
from a running REP node.

## Step 1 — Start the node

python3 rep-node.py

The server will expose:

GET /registry  
GET /verify  
GET /evidence  
POST /event

## Step 2 — Generate events

Example:

curl -X POST http://127.0.0.1:8080/event \
-H "Content-Type: application/json" \
-d '{"actor_ipr":"IPR-3","decision":"deploy configuration update","cost":"compute resources","trace_input":"deployment log example"}'

## Step 3 — Verify registry

curl http://127.0.0.1:8080/verify

Expected result:

{
  "registry_verification": "PASS"
}

## Step 4 — Obtain evidence snapshot

curl http://127.0.0.1:8080/evidence

Example result:

{
  "status": "PASS",
  "event_count": 3,
  "last_event_id": "EVT-0002",
  "last_event_hash": "...",
  "final_registry_hash": "...",
  "generated_at": "2026-03-06T12:30:00Z"
}

## Interpretation

The evidence object represents a deterministic integrity summary
of the registry state.

If the registry verification fails, the evidence status will return:

FAIL
