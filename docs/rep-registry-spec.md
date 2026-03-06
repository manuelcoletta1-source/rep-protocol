# REP Registry Specification

The REP registry is an append-only event chain.

Each event is linked to the previous event through a hash reference.
This creates a deterministic and verifiable event sequence.

The registry is stored as a JSON array.

## Event Structure

Each event MUST contain the following fields.

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

## Field Definitions

event_id

Unique identifier of the event.

Example:

EVT-0001


event_type

Type of event.

Possible values include:

genesis  
operation  
system


actor_ipr

Identity of the actor responsible for the event.

Example:

IPR-3  
AI-JOKER-C2


decision

Human-readable description of the action performed.


cost

Operational cost description.

Examples:

compute resources  
compute cycle  
network resources


trace

SHA-256 hash derived from the original trace input.


time_start

UTC timestamp indicating when the event started.


time_end

UTC timestamp indicating when the event completed.


prev_hash

Hash reference to the previous event in the chain.

The genesis event uses:

NONE


public_key

Identifier of the actor public key used for signing.


event_hash

SHA-256 hash of the canonical event payload.


signature

Base64 encoded signature derived from:

public_key + event_hash


## Canonical Payload

The event hash is calculated from a canonical JSON structure containing:

event_id  
event_type  
actor_ipr  
decision  
cost  
trace  
time_start  
time_end  
prev_hash  


## Registry Verification

The registry verification process MUST validate:

1. presence of all required fields
2. hash integrity
3. correct prev_hash linkage
4. valid signature for non-genesis events

If any validation step fails, the registry status MUST be:

FAIL


## Registry Properties

A valid REP registry has the following properties:

append-only  
hash-linked  
deterministically verifiable  
actor-bound  
signature-backed


## Genesis Event

The first event initializes the registry.

event_type: genesis  
actor_ipr: SYSTEM  
prev_hash: NONE  
signature: GENESIS


## Verification Result

The registry verification endpoint returns:

PASS  
FAIL

PASS indicates that the event chain is valid and unbroken.
