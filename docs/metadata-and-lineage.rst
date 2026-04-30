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
- what still belongs to a later rebuild lane rather than the current PoC lane.

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

The current MKRF PoC package was assembled from:

- workbook-reviewed builder contracts;
- accepted archival compiled runtime evidence;
- FEMIC-native runtime XML emission; and
- Patchworks matrix-build regeneration of the runtime track package.

This lineage is sufficient for a PoC benchmark/intermediate claim. It is not
yet the later source-faithful from-scratch rebuild contract.

Claim Ladder
------------

The current lineage surfaces support the following claim ladder:

1. archival legacy package evidence exists and is inventoried;
2. workbook/builder authority was reviewed and translated into explicit FEMIC
   contract surfaces;
3. FEMIC emits a runtime XML package and rebuilds the Patchworks track package;
4. the resulting runtime package launches and supports benchmark comparison;
5. therefore the current instance qualifies as a PoC benchmark/intermediate.

The lineage surfaces explicitly do **not** support the stronger claim that the
current package is already a source-faithful rebuild from raw
``03_MappingAnalysisData/*`` inputs.

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

- what is authoritative for the current PoC lane;
- what is only historical evidence; and
- what still needs replacement in the later canonical rebuild.
