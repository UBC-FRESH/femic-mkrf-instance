MKRF User Guide
===============

This documentation site is the standalone operator guide for the
``femic-mkrf-instance`` repository.

**Runtime lane:** ``ws4`` is the primary MKRF/NICC runtime. The Patchworks
model packages are reference/interchange-only. Start with :doc:`ws4-pilot` for
the active lane.

The canonical FEMIC input/interchange package lives under
``models/mkrf_patchworks_model/``.

The retained PoC benchmark/reference package remains under
``models/mkrf_patchworks_model_poc/``.

.. toctree::
   :maxdepth: 2
   :caption: Guide

   getting-started
   model-anatomy
   legacy-archive-reference
   treatments-and-state-logic
   adjacency-and-greenup
   ws4-pilot
   analysis-units-and-yield-curves
   data-package-crosswalk
   benchmark-results
   yield-curve-comparisons
   figure-appendix
   evidence-and-boundaries
   caveats-and-deferred-seams
   metadata-and-lineage
   operator-runbook
   docs-ownership-and-release
   rebuild-and-qa
   troubleshooting
