Rebuild and QA
==============

Current Rebuild Meaning
-----------------------

For the PoC lane, rebuild/QA means:

- regenerate the runtime XML from the reviewed contract surfaces;
- rebuild the runtime track package through Patchworks Matrix Builder;
- prove the runtime package launches; and
- compare benchmark summary reports against the accepted legacy benchmark lane.

Core Validation Surfaces
------------------------

- ``femic instance validate-spec --spec config/rebuild.spec.yaml``
- runtime XML under ``models/mkrf_patchworks_model_poc/XML/``
- runtime tracks under ``models/mkrf_patchworks_model_poc/Tracks/``
- benchmark comparison reports described in :doc:`benchmark-results`

Current Quality Bar
-------------------

The current quality bar is:

- operator-facing PoC benchmark confidence

It is not:

- exact long-horizon parity
- full legacy helper recovery
- source-faithful from-scratch rebuild acceptance
