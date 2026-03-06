# REP Event Model

The Reconstructible Event Protocol (REP) defines a minimal operational model
for representing reconstructible events.

An event is considered operationally valid only when four conditions remain
reconstructible:

Decision  
Cost  
Trace  
Time  

These four conditions define the minimal structure required to reconstruct
an operational action.

## Event Unit

REP represents events as a minimal operational unit:

event_id  
decision  
cost  
trace  
time_start  
time_end  

This structure allows deterministic reconstruction of the operational sequence.

## Operational Principle

REP assumes that any real operational event introduces:

- a decision that selects an action
- a cost localized in resources or state
- a trace that remains observable
- exposure to time enabling verification

If one of these conditions disappears, the event becomes non-reconstructible
within the REP domain.
