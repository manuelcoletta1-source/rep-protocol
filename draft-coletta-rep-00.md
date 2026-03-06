---
title: Reconstructible Event Protocol (REP)
abbrev: REP
docname: draft-coletta-rep-00
category: exp
submissiontype: IETF
ipr: trust200902
area: General
workgroup: Independent Submission
keyword:
 - reconstructibility
 - audit
 - registry
 - evidence
author:
 -
   ins: M. Coletta
   name: Manuel Coletta
   org: HERMETICUM B.C.E. S.r.l.
   email: manuelcoletta1@gmail.com
normative:
  RFC2119:
  RFC8174:
informative:
  RFC3552:
pi:
  toc: yes
  sortrefs: yes
  symrefs: yes
---

--- abstract

REP defines a minimal protocol for reconstructible operational events
based on append-only registries, hash-linked sequencing, and
independent verification of exported evidence.

REP supports deterministic event verification, cumulative chain
checkpoints, portable evidence export, signed evidence export,
offline evidence validation, and remote verification of signed evidence.

--- middle

# Introduction

Modern infrastructures increasingly depend on distributed services,
autonomous systems, and operational actions whose effects must remain
reconstructible through time.

REP defines a minimal protocol for representing such events in an
append-only registry, linking them through hash references, and
supporting exportable integrity evidence.

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and
"OPTIONAL" in this document are to be interpreted as described in RFC 2119
and RFC 8174 when, and only when, they appear in all capitals.

# Core Event Model

REP defines four minimal operational conditions:

* Decision
* Cost
* Trace
* Time

A REP event is considered operationally valid only when these conditions
remain reconstructible.

REP represents each event as an Event Unit with deterministic fields and a
hash-link to the previous event.

# Event Unit Structure

A REP Event Unit contains the following fields:

* event_id
* event_type
* actor_ipr
* decision
* cost
* trace
* time_start
* time_end
* prev_hash
* public_key
* event_hash
* signature

## Field Summary

`event_id`
: Unique identifier of the event.

`event_type`
: Type of event, such as `genesis`, `operation`, or `system`.

`actor_ipr`
: Identity anchor of the actor responsible for the event.

`decision`
: Human-readable description of the action.

`cost`
: Human-readable description of the operational cost.

`trace`
: SHA-256 hash derived from the original trace input.

`time_start`
: UTC timestamp indicating when the event became operational.

`time_end`
: UTC timestamp indicating when the event completed or became evaluable.

`prev_hash`
: Hash reference to the previous event in the registry.

`public_key`
: Public-key identifier associated with the actor.

`event_hash`
: SHA-256 hash of the canonical event payload.

`signature`
: Deterministic signature derived from `public_key + event_hash`.

# Canonical Event Payload

REP computes `event_hash` from a canonical JSON payload containing:

* event_id
* event_type
* actor_ipr
* decision
* cost
* trace
* time_start
* time_end
* prev_hash

The fields `public_key`, `event_hash`, and `signature` are not included in
the canonical payload.

# Genesis Event

A REP registry begins with a required genesis event.

A minimal genesis event uses:

* event_id: EVT-0000
* event_type: genesis
* actor_ipr: SYSTEM
* decision: initialize registry
* cost: none
* prev_hash: NONE
* public_key: SYSTEM
* signature: GENESIS

# Registry Model

REP uses an append-only JSON registry.

Each event references the previous event through `prev_hash`, producing a
hash-linked sequence.

Registry properties include:

* append-only structure
* deterministic ordering
* hash-linked history
* actor-bound attribution
* signature-backed integrity

# Registry Verification

Verification begins from:

* prev = NONE

For each event, the verifier checks:

1. `prev_hash` matches the previous event hash
2. the canonical payload hashes to the stored `event_hash`
3. non-genesis events contain a valid signature

If any verification step fails, the result MUST be `FAIL`.

If the chain is coherent, the result MUST be `PASS`.

# Chain Hash Checkpoint

REP defines a cumulative checkpoint called `chain_hash`.

The chain hash is computed as:

* SHA-256(event_hash_0 + event_hash_1 + event_hash_2 + ...)

The chain hash acts as a compact fingerprint of the full registry state.

# Evidence Model

REP defines a portable evidence object containing:

* status
* event_count
* last_event_id
* last_event_hash
* final_registry_hash
* generated_at

The evidence object summarizes the current integrity state of the registry.

# Signed Evidence Model

REP defines a signed evidence object containing:

* evidence
* evidence_hash
* public_key
* signature

The `evidence_hash` is computed from a canonical serialization of the
evidence fields.

The signature is derived from:

* public_key + evidence_hash

This allows evidence to be exported as a portable attestation object.

# HTTP Reference Node

A REP reference node MAY expose the following HTTP endpoints:

* GET /registry
* GET /verify
* GET /evidence
* GET /export-evidence
* GET /export-evidence-signed
* GET /chain-hash
* POST /event

# Runtime Artifacts

REP reference implementations may generate runtime files such as:

* rep-registry.json
* rep-evidence.json
* rep-evidence-signed.json

These files represent runtime state rather than normative source artifacts.

# Offline Verification

REP supports offline verification of exported evidence.

A plain evidence verifier checks:

* required field presence
* valid status field
* expected field types

A signed evidence verifier checks:

* signed evidence structure
* evidence hash correctness
* signature validity

# Remote Verification

REP supports remote verification of signed evidence through an external
verifier querying a REP node endpoint.

A remote verifier retrieves exported signed evidence and validates:

* top-level payload
* signed evidence structure
* evidence hash
* signature integrity

# Security Considerations

REP depends on the integrity of:

* registry ordering
* canonical hashing
* actor public-key mapping
* deterministic signature derivation
* exported evidence serialization

REP does not currently define transport security, key distribution, or
adversarial network consensus. These remain outside the present scope.
See RFC 3552 for general guidance on security considerations in protocol
design.

# Conclusion

REP defines a minimal protocol for reconstructible operational events and
their deterministic verification through append-only registry methods.

REP combines:

* event reconstruction
* actor attribution
* hash-linked sequencing
* registry verification
* checkpoint hashing
* portable evidence export
* signed evidence attestation
* independent verification

In this form, REP is both a protocol specification and a working protocol
prototype.

--- back

# References

## Normative References

[RFC2119]
: Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels",
  BCP 14, RFC 2119, DOI 10.17487/RFC2119, March 1997.

[RFC8174]
: Leiba, B., "Ambiguity of Uppercase vs Lowercase in RFC 2119 Key Words",
  BCP 14, RFC 8174, DOI 10.17487/RFC8174, May 2017.

## Informative References

[RFC3552]
: Rescorla, E. and B. Korver, "Guidelines for Writing RFC Text on Security
  Considerations", BCP 72, RFC 3552, DOI 10.17487/RFC3552, July 2003.
