# REP Event Examples

This document provides illustrative examples of Event Units in the
Reconstructible Event Protocol (REP).

These examples demonstrate how operational events can be represented
using the REP event structure.

## Example 1 — Infrastructure Change

event_id: EVT-0001

decision: Deploy updated service configuration  
cost: Resource allocation and service restart  
trace: Configuration change log and deployment record  
time_start: 2026-03-06T10:15:00Z  
time_end: 2026-03-06T10:18:00Z

This event represents an operational infrastructure change recorded
through observable traces and bounded in time.

## Example 2 — Autonomous System Action

event_id: EVT-0002

decision: Autonomous system adjusts operational parameter  
cost: Computational resource usage and state modification  
trace: System telemetry and configuration update record  
time_start: 2026-03-06T11:02:10Z  
time_end: 2026-03-06T11:02:15Z

The event records the operational decision executed by an automated
system and the traces produced during the action.

## Example 3 — Administrative Decision

event_id: EVT-0003

decision: Administrative approval of operational change  
cost: Organizational resource allocation  
trace: Decision record and authorization log  
time_start: 2026-03-06T12:30:00Z  
time_end: 2026-03-06T12:45:00Z

This event demonstrates how governance or administrative decisions
can be represented using the REP event structure.

## Reconstruction

In each example, verification reconstructs the event sequence:

Decision → Cost → Trace → Time
