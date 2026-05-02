Metadata and Lineage
====================

Primary Machine-Readable Ledgers
--------------------------------

Key instance lineage surfaces include:

- ``metadata/lineage_registry.yaml``
- ``metadata/legacy_runtime_xml_emission.yaml``
- ``metadata/legacy_runtime_track_reconciliation.yaml``
- ``metadata/legacy_source_input_publication_boundary.yaml``
- ``metadata/legacy_source_reproducibility_boundary.yaml``

Those files are not redundant bookkeeping. Together they answer three different
questions:

- what source or archival surface exists;
- what claim that surface supports; and
- what still belongs outside the canonical rebuild claim boundary.

Primary Human-Readable Runbooks
-------------------------------

- ``runbooks/LEGACY_COMPILED_PACKAGE_REFERENCE.md``
- ``runbooks/LEGACY_XML_BUILDER_AUTHORITY_REVIEW.md``
- ``runbooks/LEGACY_GENERATED_XML_RECONCILIATION.md``
- ``runbooks/LEGACY_REBUILD_READINESS_CRITERIA.md``
- ``runbooks/LEGACY_RUNTIME_XML_EMISSION.md``
- ``runbooks/LEGACY_RUNTIME_TRACK_RECONCILIATION.md``

The runbooks are the readable companion layer for the machine-readable ledgers.
Operators should use them first when they need narrative context, and then use
the YAML ledgers when they need exact artifact/claim/status details.

Lineage Summary
---------------

The current canonical MKRF package was assembled from:

- workbook-reviewed builder contracts;
- source-faithful runtime spatial publication from upstream mapping-analysis
  inputs;
- FEMIC-native runtime XML/package emission; and
- Patchworks matrix-build regeneration of the canonical runtime track package.

This lineage is sufficient for the canonical runtime/package rebuild claim.

The retained PoC package remains a separate benchmark/reference lineage surface
under ``models/mkrf_patchworks_model_poc/``.

Claim Ladder
------------

The current lineage surfaces support the following claim ladder:

1. archival legacy package evidence exists and is inventoried;
2. workbook/builder authority was reviewed and translated into explicit FEMIC
   contract surfaces;
3. FEMIC emits a canonical runtime/package surface and rebuilds the Patchworks
   track package from that surface;
4. the resulting canonical package launches/builds cleanly and supports
   runtime-surface comparison against the accepted PoC package; and
5. therefore the current instance qualifies as a source-faithful canonical
   runtime/package rebuild with explicit retained benchmark/reference evidence.

The lineage surfaces explicitly do **not** support the stronger claim that the
current instance has already rebuilt the legacy control/entrypoint helper lane.
Accepted legacy-only seams such as ``THLB4070(...)``, ``UWR(...)``, and
``InitialTargets/00_Target_Descriptions.bsh`` remain outside that claim
boundary.

How To Read `lineage_registry.yaml`
-----------------------------------

The registry is the top-level inventory of published instance artifacts and what
class of thing each artifact is:

- reference metadata;
- translated config;
- archival reference;
- generated runtime surface; or
- benchmark/reconciliation evidence.

That is the quickest way to distinguish:

- what is authoritative for the current canonical rebuild lane;
- what is benchmark/reference evidence from the retained PoC lane;
- what is only historical evidence; and
- what still remains outside the canonical rebuild claim boundary.

Runtime AU and species-share audit surfaces
-------------------------------------------

The most important current technical lookup surfaces for the canonical runtime
are:

- ``data/model_input_bundle/selected_au_table.csv``
- ``data/model_input_bundle/stand_origin_assignment.csv``
- ``data/model_input_bundle/stand_au_assignment.csv``
- ``models/mkrf_patchworks_model/analysis/runtime_au_remap_audit.csv``
- ``models/mkrf_patchworks_model/analysis/runtime_species_share_audit.csv``

Use them for different questions:

- ``selected_au_table.csv``:
  what canonical top-N AU subset was retained for runtime publication?
- ``stand_au_assignment.csv``:
  what raw AU did the underlying stand evidence support?
- ``stand_origin_assignment.csv``:
  what origin class did that stand receive under the current runtime rule?
- ``runtime_au_remap_audit.csv``:
  what canonical selected AU did runtime actually use after non-top-N AU
  normalization/remap?
- ``runtime_species_share_audit.csv``:
  what species-share surface was published for that canonical AU/origin lane?

This is the main technical evidence behind the concise operator explanation in
:doc:`analysis-units-and-yield-curves`.
