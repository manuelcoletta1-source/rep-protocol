# REP Minimal Core

The Reconstructible Event Protocol (REP) is designed around a minimal core model.

The goal of REP is to define the smallest possible structure required
to represent reconstructible operational events.

## Core Conditions

The protocol relies on four conditions:

Decision  
Cost  
Trace  
Time  

These four elements form the minimal core required for reconstructible events.

## Minimal Event Unit

The minimal structure of a REP Event Unit is:

event_id  
decision  
cost  
trace  
time_start  
time_end  

This structure allows deterministic reconstruction of the event.

## Minimal Philosophy

REP intentionally avoids introducing unnecessary complexity.

The protocol focuses only on the structural conditions required for
reconstructibility and does not prescribe specific technologies,
infrastructures, or governance models.

## Structural Sufficiency

If Decision, Cost, Trace, and Time remain reconstructible,
the event can be verified.

If one of these conditions cannot be reconstructed,
the event becomes non-reconstructible within the REP model.
