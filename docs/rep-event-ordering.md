# REP Event Ordering

The Reconstructible Event Protocol (REP) assumes that operational events
occur within a temporal sequence.

Maintaining the correct ordering of events is necessary to reconstruct
the operational history of a system.

## Chronological Sequence

REP Event Units should be recorded in chronological order based on
their temporal exposure.

Each event includes:

time_start  
time_end  

These timestamps allow events to be placed within an operational timeline.

## Ordering Principle

Event ordering allows reconstruction of the operational chain:

Decision → Cost → Trace → Time

Multiple events may form longer sequences that describe the evolution
of a system through time.

## Registry Role

Registries implementing REP should preserve event ordering.

Append-only registries naturally support chronological recording of
events without retroactive modification.

## Reconstruction

When reconstructing operational history, verification systems evaluate
events according to their recorded temporal sequence.

Preserving event order ensures that the operational chain remains
coherent and verifiable.
