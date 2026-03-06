# REP Identity Attribution

The Reconstructible Event Protocol (REP) allows operational events to be
associated with identifiable actors or systems.

REP itself does not mandate a specific identity infrastructure. However,
events SHOULD be linked to persistent identity anchors when possible.

## Purpose

Identity attribution allows reconstruction of responsibility associated
with operational decisions.

By linking events to identifiable entities, REP enables verifiable
accountability within distributed infrastructures.

## Identity Anchors

An identity anchor represents a persistent identifier capable of linking
operational events to actors.

Examples include:

- cryptographic identities
- infrastructure node identifiers
- institutional operational identifiers
- persistent identity records

## Attribution

When an event is recorded, the identity anchor SHOULD be associated with
the decision that generated the event.

This allows later reconstruction of:

Decision → Actor → Operational consequences

Identity attribution strengthens the reconstructibility of operational
events and improves accountability across distributed systems.
