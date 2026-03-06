---
title: Reconstructible Event Protocol (REP)
abbrev: REP
docname: draft-coletta-rep-00
category: exp
submissiontype: IETF
author:
- name: Manuel Coletta
  org: HERMETICUM B.C.E. S.r.l.
  email: manuelcoletta1@gmail.com
---

# Abstract

This document specifies the Reconstructible Event Protocol (REP), a minimal
protocol for representing reconstructible operational events and verifying
their integrity through deterministic registry methods.

REP defines an append-only event model in which each event is linked to the
previous event through a hash reference and attributed to an operational
actor through a public-key-bound signature model.

The protocol also defines registry-level verification, cumulative chain
checkpoints, portable evidence export, signed evidence export, and offline
or remote evidence validation.

---

# Status of This Memo

This Internet-Draft is submitted in full conformance with the provisions of
BCP 78 and BCP 79.

Internet-Drafts are working documents of the Internet Engineering Task Force
(IETF). They may be updated, replaced, or obsoleted at any time.

---

# 1. Introduction

Modern infrastructures increasingly depend on autonomous systems,
distributed services, and operational processes whose actions must remain
reconstructible through time.

Existing systems often provide logging, authentication, and transport
mechanisms, but do not guarantee that operational events remain
deterministically reconstructible, hash-linked, and independently
verifiable.

REP addresses this gap by defining a minimal protocol for operational
events with the following properties:

- append-only recording
- deterministic verification
- hash-linked event sequencing
- actor-bound event generation
- registry checkpoint generation
- portable evidence export
- signed evidence export
- offline and remote verification of exported evidence

REP treats operational events as bounded units whose effects remain
reconstructible across time.

---

# 2. Core Event Model

REP defines four minimal conditions for an operational event:

Decision  
Cost  
Trace  
Time

An event is considered operationally valid only when these four conditions
remain reconstructible.

To make such reconstruction operationally verifiable, REP represents each
event as an Event Unit with a deterministic structure and a hash-link to
the previous event in the registry.

---

# 3. Event Unit Structure

A REP Event Unit contains the following fields:

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

## 3.1 Field Definitions

### event_id

A unique event identifier.

Example:

EVT-0001

### event_type

The type of event.

Example values include:

genesis  
operation  
system

### actor_ipr

The identity anchor of the operational actor responsible for the event.

Example values:

IPR-3  
AI-JOKER-C2

### decision

A human-readable description of the action that generated the event.

### cost

A human-readable description of the localized operational cost.

### trace

A SHA-256 hash derived from the original trace input associated with the
event.

### time_start

UTC timestamp indicating when the event became operational.

### time_end

UTC timestamp indicating when the event completed or became evaluable.

### prev_hash

Hash reference to the previous event in the registry.

For the genesis event:

NONE

### public_key

The public-key identifier associated with the actor.

### event_hash

The SHA-256 hash of the canonical event payload.

### signature

A deterministic signature derived from:

public_key + event_hash

---

# 4. Canonical Event Payload

REP computes the `event_hash` from a canonical JSON payload containing:

event_id  
event_type  
actor_ipr  
decision  
cost  
trace  
time_start  
time_end  
prev_hash

The fields `public_key`, `event_hash`, and `signature` are not included in
the canonical payload.

This ensures stable and reproducible event hashing.

---

# 5. Genesis Event

A REP registry begins with a required genesis event.

The genesis event initializes the registry and defines the first trust
anchor of the event chain.

Example genesis structure:

event_id: EVT-0000  
event_type: genesis  
actor_ipr: SYSTEM  
decision: initialize registry  
cost: none  
prev_hash: NONE  
public_key: SYSTEM  
signature: GENESIS  

The genesis event establishes the first `event_hash` from which subsequent
events derive their `prev_hash`.

---

# 6. Registry Model

REP uses an append-only registry.

Events are appended sequentially and each event references the previous
event through `prev_hash`.

This creates a hash-linked event chain.

The registry is stored as a JSON array.

Registry properties include:

- append-only structure
- deterministic ordering
- hash-linked history
- actor-bound attribution
- signature-backed integrity

---

# 7. Registry Verification

REP defines deterministic registry verification.

Verification begins from:

prev = NONE

Each event is verified in sequence.

For every event the verifier MUST check:

1. `prev_hash` matches the previous event hash
2. the canonical payload hashes to the stored `event_hash`
3. non-genesis events have a valid signature derived from
   `public_key + event_hash`

If any event fails verification, the registry verification result MUST be:

FAIL

If the full chain is coherent, the registry verification result MUST be:

PASS

---

# 8. Chain Hash Checkpoint

REP defines a cumulative chain checkpoint called `chain_hash`.

The chain hash is computed as:

SHA-256( event_hash₀ + event_hash₁ + event_hash₂ + ... )

This produces a single fingerprint representing the current registry state.

Properties of the chain hash:

- changes if any event changes
- depends on event ordering
- provides a compact registry checkpoint
- may be exported independently of the full registry

REP nodes may expose this checkpoint through a dedicated endpoint.

---

# 9. Evidence Model

REP defines a portable evidence object summarizing the current registry
state.

A REP evidence object contains:

status  
event_count  
last_event_id  
last_event_hash  
final_registry_hash  
generated_at  

## 9.1 Field Definitions

### status

Registry verification result.

Possible values:

PASS  
FAIL

### event_count

Number of events in the registry.

### last_event_id

Identifier of the most recent event.

### last_event_hash

Hash of the most recent event.

### final_registry_hash

Cumulative hash checkpoint of the registry.

### generated_at

UTC timestamp at which the evidence object was generated.

The evidence object provides a compact integrity summary of the registry.

---

# 10. Signed Evidence Model

REP defines a signed evidence export model.

A signed evidence object contains:

evidence  
evidence_hash  
public_key  
signature  

## 10.1 Evidence Hash

The `evidence_hash` is computed from a canonical JSON serialization of the
evidence object fields:

status  
event_count  
last_event_id  
last_event_hash  
final_registry_hash  
generated_at

## 10.2 Signature

The evidence signature is derived from:

public_key + evidence_hash

This allows the evidence snapshot to be exported as a portable attestation
object.

---

# 11. Actor Registry

REP assumes an actor registry mapping operational actors to public-key
identifiers.

A minimal actor registry MAY be represented as JSON.

Example:

IPR-3  
AI-JOKER-C2

mapped to public-key identifiers.

REP does not standardize a specific external identity infrastructure, but
it requires that events be attributable to a stable actor anchor and
corresponding key identifier.

---

# 12. HTTP Reference Node

A REP reference node MAY expose the following HTTP API:

GET /registry  
GET /verify  
GET /evidence  
GET /export-evidence  
GET /export-evidence-signed  
GET /chain-hash  
POST /event  

## 12.1 Endpoint Roles

### GET /registry

Returns the append-only registry.

### GET /verify

Returns the deterministic verification result of the registry.

### GET /evidence

Returns the current evidence object.

### GET /export-evidence

Exports the evidence object to a runtime file and returns the exported
payload.

### GET /export-evidence-signed

Exports a signed evidence object to a runtime file and returns the signed
payload.

### GET /chain-hash

Returns the cumulative registry checkpoint.

### POST /event

Creates and appends a new event to the registry.

---

# 13. Runtime Artifacts

REP reference implementations may generate runtime files that represent
operational state rather than source code.

Example runtime artifacts include:

rep-registry.json  
rep-evidence.json  
rep-evidence-signed.json  

These files SHOULD be treated as runtime state and not as normative source
artifacts of the protocol implementation.

---

# 14. Offline Verification

REP supports offline verification of exported evidence.

Two minimal verification modes are defined.

## 14.1 Plain Evidence Verification

A plain evidence verifier checks:

- required field presence
- valid status field
- correct field types

## 14.2 Signed Evidence Verification

A signed evidence verifier checks:

- signed evidence structure
- canonical evidence hash
- deterministic signature validity

This allows exported evidence files to be verified independently from the
active node.

---

# 15. Remote Verification

REP supports remote verification of signed evidence through an external
verifier that queries a REP node endpoint.

A remote verifier retrieves:

GET /export-evidence-signed

and validates:

- top-level exported payload
- signed evidence structure
- evidence hash
- signature integrity

This permits independent verification without direct trust in the local
runtime environment of the node.

---

# 16. Security Considerations

REP depends on the integrity of:

- registry ordering
- canonical hashing
- actor public-key mapping
- deterministic signature derivation
- exported evidence serialization

If event ordering changes, if event payloads are altered, or if evidence
serialization is modified, verification results will fail.

REP does not presently define:

- transport-layer security
- cryptographic key distribution
- key revocation
- adversarial network consensus

These remain implementation concerns outside the current minimal protocol
scope.

---

# 17. Protocol Properties

The current REP model provides:

- append-only registry recording
- deterministic event verification
- hash-linked operational history
- cumulative registry checkpointing
- portable evidence export
- signed evidence export
- offline evidence verification
- remote signed evidence verification

These properties make REP suitable as an experimental protocol for
verifiable operational audit flows.

---

# 18. Current Implementation Scope

The current reference implementation demonstrates:

- event creation
- genesis event initialization
- append-only registry persistence
- registry verification
- chain hash calculation
- evidence export
- signed evidence export
- offline verification tools
- remote signed evidence verification

The implementation is minimal and experimental.

It should be interpreted as a protocol prototype rather than a final
production-grade standard.

---

# 19. Conclusion

REP defines a minimal protocol for reconstructible operational events and
their deterministic verification through append-only registry methods.

It combines:

Decision  
Cost  
Trace  
Time

with:

- actor attribution
- hash-linked sequencing
- registry verification
- checkpoint hashing
- portable evidence export
- signed evidence attestation
- independent verification

In this form REP is not merely a document model. It is a working protocol
prototype capable of generating, exporting, and validating operational
integrity evidence.

---

# Author

Manuel Coletta  
HERMETICUM B.C.E. S.r.l.
