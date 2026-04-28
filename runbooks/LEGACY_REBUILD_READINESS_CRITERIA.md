# Legacy Rebuild Readiness Criteria

This note records the P56.6 rebuild-readiness criteria for the MKRF legacy
rebuild lane.

## Decision

Metadata recovery through Phase 56: **complete**.

Runnable FEMIC/Patchworks rebuild candidate: **no-go**.

P56.6 publishes the criteria required before a future task can claim runnable
rebuild readiness. It does not activate builders, generate XML, regenerate
fragments, run Patchworks matrix build, or ingest source payloads.

## Required Gates

A runnable rebuild candidate requires all of the following gates to pass:

- legacy evidence gate;
- source-input publication gate;
- builder activation gate;
- FEMIC-generated XML gate;
- Patchworks matrix-build gate;
- output comparison gate; and
- identity gate.

The legacy evidence gate is sufficient for metadata recovery. It is not
sufficient for runnable rebuild readiness.

## Current No-Go Reasons

The runnable rebuild claim remains blocked because:

- the fragments payload publication still requires DataLad/git-annex
  availability;
- the current MKRF run profile is still a template and does not publish a real
  boundary path or source checkpoint;
- the curve, retention/netdown, attribute, and stratum builders are not active;
- no FEMIC-generated MKRF ForestModel XML exists yet;
- no Patchworks matrix build has been run from FEMIC-generated XML;
- no FEMIC-generated track outputs exist for comparison; and
- the generated XML literal description `Base TFL26` does not match the
  accepted MKRF case identity.

## Future Claim Boundary

A future runnable claim must show both:

- FEMIC-generated XML plus Patchworks matrix-build outputs; and
- direct comparison of those outputs against the legacy evidence reviewed in
  Phase 56.

Archival legacy controls, generated XML, compiled tracks, and spatial runtime
files remain comparison evidence. They must not be relabeled as
FEMIC-regenerated outputs.
