Adjacency and Greenup
======================

Purpose
-------

This page documents the optional greenup/adjacency surface in the canonical
MKRF runtime package. It is disabled by default and is configured under the
``greenup`` block in ``config/silviculture.mkrf.yaml``.

.. warning::

   Patchworks patch targets are soft weighted objectives, not hard adjacency
   constraints. This feature is an approximation of a greenup constraint. Use
   ws4 when the model must enforce true adjacency/greenup rules.

Configuration
-------------

.. code-block:: yaml

   greenup:
     enabled: false
     greenup_years: 5
     adjacency_distance_m: 100
     intermediate_min_ha: 40
     max_patch_size_ha: 50
     intermediate_max_size_percent: 5
     intermediate_weight: 10
     large_patch_weight: 1000

The parameters mean:

- ``greenup_years``: age window used by the patch membership criterion. A block
  joins a recent-harvest patch while its area is inside this seral window.
- ``adjacency_distance_m``: proximal distance used to build the separation-block
  topology and to group neighbouring blocks into one patch.
- ``intermediate_min_ha`` / ``max_patch_size_ha``: bounds of the intermediate
  patch-size class. The generated classes are ``0_40``, ``40_50`` and
  ``50plus`` by default.
- ``intermediate_max_size_percent`` / ``intermediate_weight``: soft maximum and
  scheduler weight for the intermediate class.
- ``large_patch_weight``: scheduler weight for the ``50plus`` class, whose soft
  maximum is zero.

Generated runtime artifacts
---------------------------

When ``greenup.enabled`` is true, ``mkrf-init-runtime-package`` produces:

- ``models/mkrf_patchworks_model/spatial/topo_frag<distance>.csv``: proximal
  topology generated from the current runtime fragments using the
  ``BLOCK1,BLOCK2,DISTANCE,LENGTH`` contract;
- ``models/mkrf_patchworks_model/scripts/targets/patchtargets.bsh``: BeanShell
  target setup for the active patch-size classes;
- ``analysis/runtime_greenup_provenance.json``: configuration and topology
  provenance; and
- an ``le<greenup_years>`` seral curve plus
  ``%f.area.%m.seral.le<greenup_years>`` feature in ``xml/forestmodel.xml``.

``analysis/base.pin`` is also updated to:

- set ``usePatches = true``;
- load the topology and define the three patch targets on
  ``feature.area.managed.seral.le<greenup_years>``; and
- source and call ``setupGreenupPatchTargets``.

Rebuild order
-------------

1. Publish the current runtime fragments.
2. Run ``mkrf-femic mkrf-init-runtime-package ...`` with ``greenup.enabled``
   set in ``config/silviculture.mkrf.yaml``.
3. Run the Patchworks matrix build so ``tracks/accounts.csv`` is regenerated
   with the new seral account before loading ``analysis/base.pin``.

The matrix build is required because the patch target criteria account must
exist in ``tracks/accounts.csv``. A pin that references the new criterion
against a stale track package will fail at load time.

Deferred work
-------------

A second implementation using soft patch-size distribution targets is planned
but not parameterized yet. The current greenup block already exposes the
intermediate-class percentage and scheduler weights that such a surface would
reuse. The detailed distribution targets remain TBD.
