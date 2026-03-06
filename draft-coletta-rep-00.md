---
title: Reconstructible Event Protocol (REP)
abbrev: REP
docname: draft-coletta-rep-00
category: exp
submissiontype: IETF
author:
- name: Manuel Coletta
  org: HERMETICUM B.C.E. S.r.l.
  email: manuelcoletta1@gmail.com
---

# Abstract

REP defines a minimal protocol for reconstructible operational events
based on append-only registries, hash-linked sequencing, and
independent verification of exported evidence.

# Introduction

This document describes the Reconstructible Event Protocol (REP) and
its reference operational model.

# Event Model

A REP event contains:

- decision
- cost
- trace
- time

Events are serialized into a deterministic structure and linked through
hash references.

# Registry Model

REP uses an append-only registry where each event references the
previous event hash.

# Verification

A registry is valid when:

1. event hashes match canonical payloads
2. prev_hash references are correct
3. signatures are valid

# Evidence Model

Nodes may export evidence objects summarizing the registry state.

Evidence objects include:

- event_count
- last_event_hash
- final_registry_hash
- generated_at

# Signed Evidence

Evidence may be exported with a deterministic signature for independent
verification.

# Security Considerations

REP depends on canonical serialization, deterministic hashing, and
stable actor identity anchors.

# Author

Manuel Coletta  
HERMETICUM B.C.E. S.r.l.
