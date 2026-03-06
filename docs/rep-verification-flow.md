# REP Verification Flow

The Reconstructible Event Protocol (REP) verifies operational events by
reconstructing the minimal conditions that define an Event Unit.

Verification evaluates whether the event remains reconstructible through
observable evidence.

## Verification Inputs

A verification system receives an Event Unit containing:

event_id  
decision  
cost  
trace  
time_start  
time_end  

These fields provide the structural information required to reconstruct
the operational event.

## Verification Sequence

REP verification reconstructs the event using the following order:

Decision → Cost → Trace → Time

Each stage must remain observable for the event to remain valid.

### Step 1 — Decision

The system evaluates whether the operational decision can be identified
or attributed.

### Step 2 — Cost

The system verifies whether the decision produced a localized cost.

### Step 3 — Trace

The system evaluates whether observable evidence of the event exists.

### Step 4 — Time

The system evaluates the temporal interval in which the event occurred.

## Verification Result

Verification produces a deterministic outcome:

PASS  
FAIL  

PASS indicates that all reconstructibility conditions are satisfied.

FAIL indicates that one or more conditions cannot be reconstructed.

## Fail-Closed Behavior

REP verification systems should return FAIL whenever reconstruction
cannot be completed.
