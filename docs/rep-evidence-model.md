# REP Evidence Model

The Reconstructible Event Protocol (REP) supports the generation of an evidence snapshot
describing the current integrity state of the registry.

An evidence object summarizes the verifiable status of the event chain at a specific time.

## Purpose

The REP evidence model provides a compact and portable integrity summary for:

- registry status verification
- audit snapshots
- external evidence export
- reproducible state reporting

## Evidence Fields

A REP evidence object contains:

status  
event_count  
last_event_id  
last_event_hash  
final_registry_hash  
generated_at  

## Field Description

status  
Verification result of the full registry.

Possible values:

PASS  
FAIL  

event_count  
Total number of events currently stored in the registry.

last_event_id  
Identifier of the most recent event in the chain.

last_event_hash  
Hash of the most recent event.

final_registry_hash  
Deterministic hash summarizing the full registry state.

generated_at  
UTC timestamp indicating when the evidence object was generated.

## Example

status: PASS  
event_count: 3  
last_event_id: EVT-0002  
last_event_hash: 366b0778b0489049cdebcee1a7963638ee88d1a5608d2e91c3e0a2b14ac5bfae  
final_registry_hash: 9e5f5c0b5f3e0f6d4d8b0c1a2e9f7b6a5d4c3b2a190817161514131211100f0e  
generated_at: 2026-03-06T12:30:00Z  

## Operational Role

The evidence snapshot does not replace the registry.

It provides a compact integrity summary that can be exported, stored, compared,
or attached to audit and verification workflows.

## Verification Logic

The evidence object is valid only if it is derived from a registry whose chain
verification returns:

PASS

If the registry verification fails, the evidence status must be:

FAIL
