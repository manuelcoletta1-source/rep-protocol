# REP Limitations

The Reconstructible Event Protocol (REP) defines a minimal structure for
reconstructible operational events. As a minimal protocol, REP intentionally
does not address all aspects of operational systems.

## Interpretation

REP does not interpret events.

The protocol only provides the structural conditions required to reconstruct
an operational sequence. Interpretation of the meaning or intention of an
event remains outside the protocol scope.

## Storage Technology

REP does not prescribe any specific storage technology.

Event Units may be recorded using different infrastructures, including:

- append-only logs
- distributed registries
- cryptographic ledgers
- infrastructure audit systems

The protocol only assumes that historical records remain reconstructible.

## Identity Systems

REP does not mandate a specific identity infrastructure.

Identity attribution may be implemented using external identity systems
when operational accountability requires it.

## Enforcement

REP does not enforce system behavior.

The protocol describes how events can be structured and verified but does
not control how systems execute decisions.

## Scope

REP remains a structural protocol describing reconstructible operational
events rather than a full governance or infrastructure framework.
