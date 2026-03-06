# REP Compliance

A system is considered REP-compliant if it satisfies the structural
requirements of the Reconstructible Event Protocol.

## Compliance Requirements

A REP-compliant system must:

1. represent events using the REP Event Unit structure
2. record the four reconstructible conditions
3. preserve event integrity
4. allow deterministic verification

## Event Requirements

Each recorded event must contain:

decision  
cost  
trace  
time_start  
time_end  

These fields allow reconstruction of the operational chain:

Decision → Cost → Trace → Time

## Verification

REP-compliant systems must support deterministic verification outcomes:

PASS  
FAIL

If reconstruction cannot be completed, the system must return FAIL.
