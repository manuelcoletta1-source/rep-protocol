# REP Event Granularity

The Reconstructible Event Protocol (REP) does not impose a fixed
granularity for operational events.

Instead, REP assumes that systems define Event Units at a level
sufficient to preserve reconstructibility.

## Granularity Principle

An event should be defined at the smallest level where the four
reconstructible conditions remain observable:

Decision  
Cost  
Trace  
Time  

If an event is defined too broadly, reconstruction may become ambiguous.

If an event is defined too narrowly, the event structure may become
fragmented without improving reconstructibility.

## Practical Balance

Implementations should choose an event granularity that preserves
clear operational meaning.

Each Event Unit should represent a distinct operational action
that introduces observable consequences.

## Event Chains

Complex operations may be represented as sequences of events.

Each event in the chain preserves its own reconstructible structure.

These sequences allow systems to reconstruct larger operational
processes through ordered Event Units.
