# REP Event Integrity

The Reconstructible Event Protocol (REP) assumes that the integrity of
event records is essential for reconstructibility.

If event records can be silently modified, deleted, or replaced,
reconstruction of operational sequences becomes unreliable.

## Integrity Principle

REP-compatible systems should ensure that recorded events preserve their
original structure and content.

The Event Unit fields should remain intact:

event_id  
decision  
cost  
trace  
time_start  
time_end  

Integrity mechanisms protect the reliability of these fields.

## Integrity Mechanisms

Typical mechanisms used to preserve event integrity include:

- cryptographic hashing
- tamper-evident logs
- append-only registries
- verifiable timestamps

These mechanisms allow later verification that event records have not
been altered.

## Verification Role

During verification, the system evaluates whether traces and event data
remain consistent with the recorded event structure.

If integrity cannot be confirmed, the event cannot be considered
reconstructible.

## Operational Consequence

Integrity failures should cause verification to return:

FAIL

This prevents corrupted or manipulated records from producing false
verification outcomes.
