# REP Message Format

The Reconstructible Event Protocol (REP) defines a minimal event message
structure used to represent reconstructible operational events.

## Event Unit Format

A REP Event Unit contains the following fields:

event_id  
decision  
cost  
trace  
time_start  
time_end  

## Field Description

event_id  
Unique identifier of the event.

decision  
Description of the operational action that initiated the event.

cost  
Localized loss associated with the decision.

trace  
Observable evidence produced by the event.

time_start  
Timestamp indicating when the event becomes operational.

time_end  
Timestamp indicating when the event becomes evaluable or closed.

## Example

event_id: EVT-0001

decision: Deploy configuration update  
cost: service restart and compute resources  
trace: deployment log and configuration hash  
time_start: 2026-03-06T10:15:00Z  
time_end: 2026-03-06T10:18:00Z
