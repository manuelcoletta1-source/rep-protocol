# REP Fail-Closed Model

The Reconstructible Event Protocol (REP) adopts a fail-closed verification principle.

When reconstruction of an event cannot be completed, the system must return a
negative result rather than attempting interpretation.

## Principle

Verification outcomes are limited to two possible states:

PASS  
FAIL  

PASS indicates that the event satisfies all reconstructibility conditions.

FAIL indicates that at least one of the required operational conditions
cannot be reconstructed.

## Reconstruction Conditions

Verification evaluates the presence of the four REP conditions:

Decision  
Cost  
Trace  
Time  

If any condition cannot be verified, the event must be considered
non-reconstructible.

## Deterministic Verification

REP systems should avoid probabilistic interpretation.

Verification must rely on observable and reconstructible evidence.

## Operational Consequence

The fail-closed model ensures that incomplete or corrupted event records
do not produce misleading verification outcomes.

When uncertainty exists, the system must return FAIL.
