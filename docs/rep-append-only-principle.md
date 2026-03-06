# REP Append-Only Principle

The Reconstructible Event Protocol (REP) assumes that operational events are
recorded in structures that preserve historical integrity.

For this reason, REP-compatible registries should follow an append-only model.

## Principle

Once an event has been recorded, the record must not be modified or deleted.

New events are added sequentially while previous entries remain unchanged.

This ensures that the operational history remains reconstructible.

## Event Sequence

Append-only registries allow deterministic reconstruction of operational
history through ordered events.

Each event contributes to the reconstruction chain:

Decision → Cost → Trace → Time

By preserving the chronological sequence of events, the registry maintains
the structural integrity of operational history.

## Tamper Evidence

Append-only structures reduce the risk of retroactive modification.

If tampering occurs, inconsistencies in the event sequence or trace
integrity become observable.

## Compatibility

Append-only registries can be implemented using different infrastructures,
including:

- immutable logs
- cryptographic ledgers
- distributed registries
- infrastructure audit logs

REP does not mandate a specific storage technology but assumes that the
event sequence remains historically preserved.
