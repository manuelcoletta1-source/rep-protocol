# REP Registry Model

The Reconstructible Event Protocol (REP) allows Event Units to be stored in append-only registries.

A registry records the sequence of operational events in a way that preserves
their reconstructibility through time.

## Registry Properties

A REP-compatible registry SHOULD provide:

- chronological ordering of events
- cryptographic integrity of records
- deterministic verification
- tamper-evident history

These properties ensure that the operational sequence of events can be
reconstructed independently of the system that originally generated them.

## Append-Only Principle

Registries implementing REP SHOULD follow an append-only model.

Events are recorded sequentially and previous records must not be modified.

This approach preserves the integrity of the event sequence and prevents
retroactive alteration of operational history.

## Reconstruction

By preserving event order and trace integrity, the registry allows
deterministic reconstruction of the sequence:

Decision → Cost → Trace → Time
