# REP Reference Implementation

This document describes the conceptual structure of a reference
implementation of the Reconstructible Event Protocol (REP).

REP implementations record operational events as Event Units and
allow deterministic reconstruction of operational sequences.

## Basic Components

A minimal REP implementation typically contains:

Event Producer  
Event Registry  
Verification Engine  

## Event Producer

The event producer generates REP Event Units when an operational
decision occurs.

Each event must include:

event_id  
decision  
cost  
trace  
time_start  
time_end  

## Event Registry

The registry stores Event Units in chronological order.

Append-only registries are recommended to preserve event integrity.

## Verification Engine

Verification reconstructs the event sequence:

Decision → Cost → Trace → Time

Verification produces deterministic results:

PASS  
FAIL
