# REP Terminology

This document defines the core terminology used by the Reconstructible Event Protocol (REP).

## Event

An operational occurrence that can be reconstructed through time using
deterministic evidence.

In REP, an event must satisfy four reconstructible conditions:

Decision  
Cost  
Trace  
Time  

## Event Unit

The minimal structure used to represent an operational event.

An Event Unit contains the following elements:

event_id  
decision  
cost  
trace  
time_start  
time_end  

This structure allows deterministic reconstruction of the operational sequence.

## Decision

The act that selects an operational action.

A decision introduces irreversibility into the operational sequence.

## Cost

The localized loss associated with the execution of a decision.

Cost may include resource consumption, economic expenditure,
computational load, or physical effects.

## Trace

Observable evidence produced by the event.

A trace must remain reconstructible independently of the system that
recorded it.

## Time

The interval during which the event remains observable and subject to
verification.

Time allows evaluation of persistence and decay of operational states.

## Reconstructibility

The property that allows an event to be deterministically reconstructed
through available evidence.

An event is reconstructible only if the four required conditions remain
verifiable.
