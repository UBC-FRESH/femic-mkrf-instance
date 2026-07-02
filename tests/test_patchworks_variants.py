from __future__ import annotations

from importlib import metadata
from pathlib import Path

from mkrf_femic.patchworks_variants import provider_factory


def test_patchworks_variant_provider_metadata() -> None:
    provider = provider_factory()

    assert provider.provider_id == "mkrf"
    assert provider.registry_base_dir == Path(__file__).resolve().parents[1]

    payload = provider.load_registry_payload()
    assert payload["instances"][0]["instance_id"] == "mkrf"
    variant_ids = {item["variant_id"] for item in payload["variants"]}
    assert variant_ids == {"mkrf.base", "mkrf.poc_base"}
    base = next(
        item for item in payload["variants"] if item["variant_id"] == "mkrf.base"
    )
    assert base["instance_root"] == "."
    assert base["analysis_pin"] == "models/mkrf_patchworks_model/analysis/base.pin"
    assert (
        base["runtime_config"] == "config/patchworks.runtime.mkrf_rebuild.windows.yaml"
    )


def test_package_exposes_patchworks_variant_registry_entry_point() -> None:
    entry_points = metadata.entry_points().select(
        group="femic.patchworks_variant_registries"
    )
    matches = [
        entry_point for entry_point in entry_points if entry_point.name == "mkrf"
    ]
    assert matches
    assert matches[0].value == "mkrf_femic.patchworks_variants:provider_factory"
