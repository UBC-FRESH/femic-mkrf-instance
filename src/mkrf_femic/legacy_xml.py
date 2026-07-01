"""MKRF-owned legacy ForestModel XML builder."""

from __future__ import annotations

import copy
import math
from pathlib import Path
import re
from typing import Any, Iterable
import xml.etree.ElementTree as et

import pandas as pd
import yaml

from femic.fmg.core import CurvePoint
from femic.fmg.patchworks import (
    DEFAULT_FORESTMODEL_DESCRIPTION,
    DEFAULT_HORIZON_YEARS,
    DEFAULT_START_YEAR,
    _as_quoted_literal,
    _build_live_legacy_input_attribute_contract,
    _format_legacy_define_constant_value,
    _format_xml_x,
    _format_xml_y,
    _legacy_expression_is_area_ha,
    _legacy_input_variables_staged_mapping,
    _load_legacy_input_variables_config,
    _normalize_legacy_constant_literal,
    _normalize_optional_expression,
    validate_forestmodel_xml_tree,
    write_forestmodel_xml,
)


DEFAULT_LEGACY_MKRF_ATTRIB_REVIEW_EXTRACT = Path(
    "metadata/mkrf_xlsm_review/ranges/attrib_attributes.review.csv"
)
DEFAULT_LEGACY_MKRF_SPP_COMP_REVIEW_EXTRACT = Path(
    "metadata/mkrf_xlsm_review/ranges/lookups_spp_comp.review.csv"
)
DEFAULT_LEGACY_MKRF_OUTPUT_ATTRIBUTES = {
    "messages": "messages.csv",
    "blocks": "blocks.csv",
    "features": "features.csv",
    "products": "products.csv",
    "treatments": "treatments.csv",
    "curves": "curves.csv",
    "tracknames": "tracknames.csv",
}
DEFAULT_LEGACY_MKRF_REQUIRED_DEFINE_FIELDS = (
    "status",
    "au",
    "auf",
    "oper",
    "ct",
    "aux",
    "treatment",
)
DEFAULT_LEGACY_MKRF_SUCCESSION_BREAKUP = "999"
DEFAULT_LEGACY_MKRF_SUCCESSION_RENEW = "0"
_MKRF_INSTANCE_ROOT = Path(__file__).resolve().parents[2]
_LEGACY_MKRF_REVIEW_FORMULA_PATTERN = re.compile(r'^="(?P<expression>.*)"$')
_LEGACY_MKRF_LOOKUP_FACTOR_PATTERN = re.compile(
    r'^="(?P<prefix>.*)"&CONCATENATE\("Number\(",'
    r'LookupTable\(Lookups!SPP_COMP,"au","(?P<species>[^"]+)"\),'
    r'"\)/100"\)$'
)
_LEGACY_MKRF_LOOKUP_REF_PATTERN = re.compile(r"^=[A-Z]+(?P<row>\d+)$")
_LEGACY_MKRF_THN_AU_PATTERN = re.compile(r'^="thn_"&N(?P<row>\d+)$')


def _load_legacy_mkrf_yaml_contract(
    *,
    path: Path,
    contract_label: str,
) -> dict[str, Any]:
    resolved = path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"{contract_label} not found: {resolved}")
    payload = yaml.safe_load(resolved.read_text(encoding="utf-8"))
    if payload is None:
        raise ValueError(f"{contract_label} must not be empty: {resolved}")
    if not isinstance(payload, dict):
        raise ValueError(
            f"{contract_label} must contain a top-level mapping/object "
            f"(found {type(payload).__name__})"
        )
    return payload


def _load_legacy_mkrf_curve_table(
    *,
    curve_table_csv_path: Path,
) -> dict[str, tuple[CurvePoint, ...]]:
    resolved = curve_table_csv_path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"legacy MKRF curve table not found: {resolved}")
    curve_table = pd.read_csv(resolved)
    required_columns = {"Curve_ID", "Age", "Value"}
    missing_columns = sorted(required_columns.difference(curve_table.columns))
    if missing_columns:
        raise ValueError(
            "legacy MKRF curve table missing required columns: "
            + ", ".join(missing_columns)
        )
    grouped: dict[str, list[CurvePoint]] = {}
    for row in curve_table.itertuples(index=False):
        curve_id = str(getattr(row, "Curve_ID", "")).strip()
        if not curve_id:
            raise ValueError("legacy MKRF curve table contains blank Curve_ID value")
        age_value = pd.to_numeric([getattr(row, "Age", None)], errors="coerce")[0]
        curve_value = pd.to_numeric([getattr(row, "Value", None)], errors="coerce")[0]
        if pd.isna(age_value) or pd.isna(curve_value):
            raise ValueError(
                f"legacy MKRF curve table contains non-numeric point for {curve_id!r}"
            )
        grouped.setdefault(curve_id, []).append(
            CurvePoint(x=float(age_value), y=float(curve_value))
        )
    return {
        curve_id: tuple(sorted(points, key=lambda point: float(point.x)))
        for curve_id, points in sorted(grouped.items())
    }


def _load_legacy_mkrf_base_xml_root(*, legacy_base_xml_path: Path) -> et.Element:
    resolved = legacy_base_xml_path.expanduser().resolve()
    if not resolved.exists():
        raise FileNotFoundError(f"legacy MKRF base XML not found: {resolved}")
    text = resolved.read_text(encoding="latin-1")
    text = re.sub(r"<!DOCTYPE.*?\]>\s*", "", text, flags=re.DOTALL)
    text = re.sub(r"&[A-Za-z_][A-Za-z0-9_]*;", "", text)
    return et.fromstring(text)


def _build_legacy_mkrf_define_column_contract(
    *,
    legacy_input_variables_config: dict[str, Any] | None,
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    staged = _legacy_input_variables_staged_mapping(legacy_input_variables_config)
    raw_columns = staged.get("additional_stratification_columns")
    if not isinstance(raw_columns, list):
        return (), ()
    live_columns: list[tuple[str, str]] = []
    required_fields: list[str] = []
    for item in raw_columns:
        if not isinstance(item, dict):
            continue
        key = str(item.get("key", "")).strip()
        source_expression = _normalize_optional_expression(
            item.get("source_expression")
        )
        if not key or source_expression is None:
            continue
        if (
            key not in required_fields
            and key in DEFAULT_LEGACY_MKRF_REQUIRED_DEFINE_FIELDS
        ):
            required_fields.append(key)
        live_columns.append((key, source_expression))
    return tuple(live_columns), tuple(required_fields)


def _build_legacy_mkrf_define_constants_contract(
    *,
    legacy_input_variables_config: dict[str, Any] | None,
    compatibility_required_constant_keys: Iterable[str] = (),
) -> tuple[tuple[tuple[str, str], ...], tuple[str, ...]]:
    staged = _legacy_input_variables_staged_mapping(legacy_input_variables_config)
    raw_constants = staged.get("constants")
    if not isinstance(raw_constants, dict):
        return (), ()
    raw_constant_contract = staged.get("constant_contract")
    constant_order: list[str] = []
    if isinstance(raw_constant_contract, list):
        for item in raw_constant_contract:
            if not isinstance(item, dict):
                continue
            key = str(item.get("key", "")).strip()
            status = str(item.get("status", "")).strip()
            if not key or status not in {"live_export", "live_build_input"}:
                continue
            constant_order.append(key)
    else:
        constant_order = [str(key).strip() for key in raw_constants if str(key).strip()]
    for key in compatibility_required_constant_keys:
        normalized_key = str(key).strip()
        if normalized_key and normalized_key not in constant_order:
            constant_order.append(normalized_key)
    entries: list[tuple[str, str]] = []
    required_fields: list[str] = []
    for key in constant_order:
        if key not in raw_constants:
            continue
        normalized_value = _normalize_legacy_constant_literal(raw_constants.get(key))
        value = _format_legacy_define_constant_value(normalized_value)
        if value is None:
            continue
        entries.append((key, value))
        required_fields.append(key)
    return tuple(entries), tuple(required_fields)


def _append_legacy_mkrf_curve_node(
    *,
    root: et.Element,
    curve_id: str,
    points: tuple[CurvePoint, ...],
) -> None:
    curve_node = et.SubElement(root, "curve", {"id": curve_id})
    for point in points:
        et.SubElement(
            curve_node,
            "point",
            {
                "x": _format_xml_x(float(point.x)),
                "y": _format_xml_y(curve_id, float(point.y)),
            },
        )


def _append_legacy_mkrf_curves(
    *,
    root: et.Element,
    curves_by_id: dict[str, tuple[CurvePoint, ...]],
) -> None:
    for curve_id, points in curves_by_id.items():
        _append_legacy_mkrf_curve_node(root=root, curve_id=curve_id, points=points)


def _load_legacy_mkrf_attribute_review_table(
    *,
    legacy_attributes_config: dict[str, Any],
) -> pd.DataFrame:
    source = legacy_attributes_config.get("source", {})
    review_extract = (source.get("parent_review_extracts", {}) or {}).get(
        "range_extract"
    ) or str(DEFAULT_LEGACY_MKRF_ATTRIB_REVIEW_EXTRACT)
    review_path = _MKRF_INSTANCE_ROOT / str(review_extract)
    if not review_path.exists():
        raise ValueError(
            f"legacy MKRF Attrib review extract is missing: {review_path.as_posix()}"
        )
    return pd.read_csv(review_path, dtype=str).fillna("")


def _resolve_legacy_mkrf_review_formula(value: str | None) -> str | None:
    normalized = _normalize_optional_expression(value)
    if normalized is None:
        return None
    match = _LEGACY_MKRF_REVIEW_FORMULA_PATTERN.match(normalized)
    if match is not None:
        return match.group("expression")
    return normalized


def _load_legacy_mkrf_species_lookup_contract() -> dict[str, tuple[str, str]]:
    review_path = _MKRF_INSTANCE_ROOT / DEFAULT_LEGACY_MKRF_SPP_COMP_REVIEW_EXTRACT
    if not review_path.exists():
        raise ValueError(
            f"legacy MKRF SPP_COMP review extract is missing: {review_path.as_posix()}"
        )
    table = pd.read_csv(review_path, dtype=str).fillna("")
    value_columns = [column for column in table.columns if column != "au"]
    resolved_rows: list[dict[str, str]] = []
    for _, row in table.iterrows():
        raw_au = str(row["au"]).strip()
        thn_match = _LEGACY_MKRF_THN_AU_PATTERN.match(raw_au)
        if thn_match is not None:
            source_index = int(thn_match.group("row")) - 7
            source_row = resolved_rows[source_index]
            resolved_au = f"thn_{source_row['au']}"
        else:
            resolved_au = raw_au

        resolved_row = {"au": resolved_au}
        for column in value_columns:
            raw_value = str(row[column]).strip()
            ref_match = _LEGACY_MKRF_LOOKUP_REF_PATTERN.match(raw_value)
            if ref_match is not None:
                source_index = int(ref_match.group("row")) - 7
                resolved_row[column] = resolved_rows[source_index][column]
            else:
                resolved_row[column] = raw_value
        resolved_rows.append(resolved_row)

    species_lookup: dict[str, tuple[str, str]] = {}
    au_values = ",".join(row["au"] for row in resolved_rows)
    for column in value_columns:
        species_lookup[column] = (
            au_values,
            ",".join(row[column] for row in resolved_rows),
        )
    return species_lookup


def _resolve_legacy_mkrf_factor_expression(
    *,
    raw_factor: str | None,
    species_lookup_contract: dict[str, tuple[str, str]],
) -> str | None:
    normalized = _normalize_optional_expression(raw_factor)
    if normalized is None:
        return None
    lookup_match = _LEGACY_MKRF_LOOKUP_FACTOR_PATTERN.match(normalized)
    if lookup_match is not None:
        species = lookup_match.group("species")
        if species not in species_lookup_contract:
            raise ValueError(
                "legacy MKRF Attrib species lookup is missing review values for "
                f"{species!r}"
            )
        au_values, species_values = species_lookup_contract[species]
        return (
            f"{lookup_match.group('prefix')}"
            f"Number(lookupTable(au,'{au_values}','{species_values}'))/100"
        )
    return _resolve_legacy_mkrf_review_formula(normalized)


def _append_legacy_mkrf_native_attribute(
    *,
    parent: et.Element,
    label: str,
    curve_or_expression: str,
    factor_expression: str | None,
) -> None:
    attribute_attrs = {"label": label}
    normalized_factor = _normalize_optional_expression(factor_expression)
    if normalized_factor is not None and normalized_factor != "1":
        attribute_attrs["factor"] = normalized_factor
    attribute_node = et.SubElement(parent, "attribute", attribute_attrs)
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", curve_or_expression):
        et.SubElement(attribute_node, "curve", {"idref": curve_or_expression})
        return
    et.SubElement(
        attribute_node,
        "expression",
        {
            "statement": curve_or_expression,
            "by": "1",
            "ignoreMissingAttributes": "false",
        },
    )


def _build_legacy_mkrf_native_attribute_selects(
    *,
    legacy_attributes_config: dict[str, Any],
) -> tuple[et.Element, ...]:
    review_table = _load_legacy_mkrf_attribute_review_table(
        legacy_attributes_config=legacy_attributes_config
    )
    species_lookup_contract = _load_legacy_mkrf_species_lookup_contract()
    configured_rows = {
        int(entry["row_offset"]): entry
        for entry in legacy_attributes_config.get("attribute_rows", []) or []
        if isinstance(entry, dict) and entry.get("row_offset") is not None
    }
    review_rows: dict[int, dict[str, str]] = {}
    for row_offset, row_config in configured_rows.items():
        if row_offset <= 0 or row_offset > len(review_table.index):
            raise ValueError(
                "legacy MKRF Attrib contract row_offset is outside the review "
                f"extract: {row_offset}"
            )
        row = review_table.iloc[row_offset - 1]
        review_rows[row_offset] = {
            "applies_to": _normalize_optional_expression(row.get("Applies to"))
            or str(row_config.get("applies_to", "")).strip(),
            "curve_or_expression": _resolve_legacy_mkrf_review_formula(
                row.get("Curve or Expression")
            )
            or _normalize_optional_expression(row_config.get("curve_or_expression")),
            "attribute_name": _normalize_optional_expression(row.get("Attribute Name"))
            or _normalize_optional_expression(row_config.get("attribute_name")),
            "factor_expression": _resolve_legacy_mkrf_factor_expression(
                raw_factor=row.get("Factor"),
                species_lookup_contract=species_lookup_contract,
            )
            or _normalize_optional_expression(row_config.get("factor_expression")),
            "selection_expression": _normalize_optional_expression(
                row.get("Unnamed: 9")
            )
            or _normalize_optional_expression(row_config.get("selection_expression"))
            or "",
        }

    block_specs = (
        ("", "features", (1, 2, 5, 6)),
        ("status in managed", "features", (9,)),
        ("", "features", (11, 12, 13, 14, 15, 16, 17, 18)),
        ("status ne 'X'", "features", (21,)),
        ("", "products", (1, 2, 3, 5, 6, 7, 11, 12, 13, 14, 15, 16, 17, 18)),
    )
    select_nodes: list[et.Element] = []
    for statement, container_tag, row_offsets in block_specs:
        select_node = et.Element("select", {"statement": statement})
        container = et.SubElement(select_node, container_tag)
        for row_offset in row_offsets:
            row = review_rows[row_offset]
            applies_to = row["applies_to"]
            if container_tag == "features" and applies_to not in {"both", "feature"}:
                continue
            if container_tag == "products" and applies_to not in {"both", "product"}:
                continue
            curve_or_expression = row["curve_or_expression"]
            label = row["attribute_name"]
            if curve_or_expression is None or label is None:
                raise ValueError(
                    "legacy MKRF Attrib row is missing curve/expression or label: "
                    f"{row_offset}"
                )
            _append_legacy_mkrf_native_attribute(
                parent=container,
                label=label,
                curve_or_expression=curve_or_expression,
                factor_expression=row["factor_expression"],
            )
        select_nodes.append(select_node)
    return tuple(select_nodes)


def _validate_legacy_mkrf_native_attributes(
    *,
    emitted_root: et.Element,
    selects: tuple[et.Element, ...],
    legacy_attributes_config: dict[str, Any],
) -> None:
    required_define_fields = {"status", "au", "aux", "treatment", "frd", "managed"}
    define_fields = {
        str(node.get("field")).strip()
        for node in emitted_root.findall("./define")
        if node.get("field")
    }
    missing_define_fields = sorted(required_define_fields.difference(define_fields))
    if missing_define_fields:
        raise ValueError(
            "native MKRF Attrib builder missing required define fields: "
            + ", ".join(missing_define_fields)
        )

    curve_ids = {
        str(node.get("id")).strip()
        for node in emitted_root.findall("./curve")
        if node.get("id")
    }
    missing_curve_ids = sorted({"one", "le10"}.difference(curve_ids))
    if missing_curve_ids:
        raise ValueError(
            "native MKRF Attrib builder missing required curves: "
            + ", ".join(missing_curve_ids)
        )
    if not any(curve_id.startswith("Yield_") for curve_id in curve_ids):
        raise ValueError("native MKRF Attrib builder requires emitted `Yield_*` curves")

    validation_contract = legacy_attributes_config.get("validation_contract", {})
    expected_attribute_names = {
        _normalize_passthrough_label(value)
        for value in validation_contract.get("required_attribute_names", []) or []
        if _normalize_passthrough_label(value)
    }
    emitted_attribute_names = {
        _normalize_passthrough_label(attribute.get("label"))
        for select in selects
        for attribute in select.findall(".//attribute")
        if _normalize_passthrough_label(attribute.get("label"))
    }
    missing_attribute_names = sorted(
        expected_attribute_names.difference(emitted_attribute_names)
    )
    if missing_attribute_names:
        raise ValueError(
            "native MKRF Attrib builder missing expected attribute labels: "
            + ", ".join(missing_attribute_names)
        )


def _normalize_passthrough_label(value: str | None) -> str:
    return str(value or "").strip()


def _extract_legacy_mkrf_attribute_passthrough_selects(
    *,
    legacy_base_xml_path: Path,
    legacy_attributes_config: dict[str, Any],
) -> tuple[et.Element, ...]:
    legacy_root = _load_legacy_mkrf_base_xml_root(
        legacy_base_xml_path=legacy_base_xml_path
    )
    validation_contract = legacy_attributes_config.get("validation_contract", {})
    required_attribute_names = {
        _normalize_passthrough_label(value)
        for value in validation_contract.get("required_attribute_names", []) or []
        if _normalize_passthrough_label(value)
    }
    passthrough_selects: list[et.Element] = []
    for select in legacy_root.findall("./select"):
        labels = [
            _normalize_passthrough_label(attribute.get("label"))
            for attribute in select.findall(".//attribute")
        ]
        expressions = [
            _normalize_passthrough_label(expression.get("statement"))
            for expression in select.findall(".//expression")
        ]
        if (
            any(label in required_attribute_names for label in labels)
            or any("%f." in label for label in labels)
            or any("curveId('Yield_" in expression for expression in expressions)
            or any(
                "attribute('feature.yield.%m.total')" in expression
                for expression in expressions
            )
        ):
            passthrough_selects.append(copy.deepcopy(select))
    if len(passthrough_selects) != 5:
        raise ValueError(
            "legacy MKRF Attrib passthrough extraction expected 5 select blocks "
            f"but found {len(passthrough_selects)}"
        )
    return tuple(passthrough_selects)


def _validate_legacy_mkrf_attribute_passthrough(
    *,
    emitted_root: et.Element,
    passthrough_selects: tuple[et.Element, ...],
    legacy_attributes_config: dict[str, Any],
    require_generated_yield_curves: bool = True,
) -> None:
    define_fields = {
        str(node.get("field")).strip()
        for node in emitted_root.findall("./define")
        if node.get("field")
    }
    required_define_fields = {"status", "au", "aux", "treatment", "frd", "managed"}
    missing_define_fields = sorted(required_define_fields.difference(define_fields))
    if missing_define_fields:
        raise ValueError(
            "legacy MKRF Attrib passthrough missing required define fields in "
            "emitted XML: " + ", ".join(missing_define_fields)
        )

    curve_ids = {
        str(node.get("id")).strip()
        for node in emitted_root.findall("./curve")
        if node.get("id")
    }
    missing_static_curves = sorted({"one", "le10"}.difference(curve_ids))
    if missing_static_curves:
        raise ValueError(
            "legacy MKRF Attrib passthrough missing required emitted curves: "
            + ", ".join(missing_static_curves)
        )
    generated_yield_curve_count = sum(
        1 for curve_id in curve_ids if curve_id.startswith("Yield_")
    )
    if require_generated_yield_curves and generated_yield_curve_count <= 0:
        raise ValueError(
            "legacy MKRF Attrib passthrough requires emitted `Yield_*` curves"
        )

    validation_contract = legacy_attributes_config.get("validation_contract", {})
    expected_attribute_names = {
        _normalize_passthrough_label(value)
        for value in validation_contract.get("required_attribute_names", []) or []
        if _normalize_passthrough_label(value)
    }
    passthrough_attribute_names = {
        _normalize_passthrough_label(attribute.get("label"))
        for select in passthrough_selects
        for attribute in select.findall(".//attribute")
        if _normalize_passthrough_label(attribute.get("label"))
    }
    missing_attribute_names = sorted(
        expected_attribute_names.difference(passthrough_attribute_names)
    )
    if missing_attribute_names:
        raise ValueError(
            "legacy MKRF Attrib passthrough missing expected attribute labels: "
            + ", ".join(missing_attribute_names)
        )


def _append_legacy_mkrf_attribute_passthrough(
    *,
    root: et.Element,
    legacy_base_xml_path: Path,
    legacy_attributes_config: dict[str, Any],
    require_generated_yield_curves: bool = True,
) -> tuple[et.Element, ...]:
    passthrough_selects = _extract_legacy_mkrf_attribute_passthrough_selects(
        legacy_base_xml_path=legacy_base_xml_path,
        legacy_attributes_config=legacy_attributes_config,
    )
    _validate_legacy_mkrf_attribute_passthrough(
        emitted_root=root,
        passthrough_selects=passthrough_selects,
        legacy_attributes_config=legacy_attributes_config,
        require_generated_yield_curves=require_generated_yield_curves,
    )
    for select in passthrough_selects:
        root.append(copy.deepcopy(select))
    return passthrough_selects


def _legacy_mkrf_track_statement_from_selection(selection: dict[str, Any]) -> str:
    parts: list[str] = []
    status_key = _normalize_optional_expression(selection.get("status"))
    if status_key is not None:
        parts.append(f"status in {status_key}")
    for expression in selection.get("additional_expressions", []) or []:
        normalized = _normalize_optional_expression(expression)
        if normalized is not None:
            parts.append(normalized)
    return " and ".join(parts)


def _normalize_legacy_mkrf_runtime_input_attributes(
    input_attributes: dict[str, str],
) -> dict[str, str]:
    normalized = dict(input_attributes)
    area_expression = _normalize_optional_expression(normalized.get("area"))
    if area_expression is not None and _legacy_expression_is_area_ha(area_expression):
        normalized["area"] = "Shape_Area/10000"
    return normalized


def _reorder_legacy_mkrf_root_children(*, root: et.Element) -> None:
    tag_order = {
        "curve": 0,
        "define": 1,
        "input": 2,
        "output": 3,
        "select": 4,
    }
    ordered_children = sorted(
        list(root),
        key=lambda node: tag_order.get(node.tag, 99),
    )
    root[:] = ordered_children


def build_legacy_mkrf_forestmodel_xml_tree(
    *,
    legacy_input_variables_config: dict[str, Any],
    legacy_curve_library_config: dict[str, Any],
    legacy_netdown_config: dict[str, Any],
    legacy_treat_config: dict[str, Any],
    generated_curve_table_by_id: dict[str, tuple[CurvePoint, ...]],
    compatibility_required_constant_keys: Iterable[str] = (),
) -> et.Element:
    """Build the opt-in MKRF ForestModel XML tree from recovered legacy contracts."""
    description = str(
        legacy_input_variables_config.get(
            "description", DEFAULT_FORESTMODEL_DESCRIPTION
        )
    )
    start_year = int(
        legacy_input_variables_config.get("start_year", DEFAULT_START_YEAR)
    )
    horizon_years = int(
        legacy_input_variables_config.get("horizon_years", DEFAULT_HORIZON_YEARS)
    )
    input_attributes, _required_input_columns = (
        _build_live_legacy_input_attribute_contract(
            legacy_input_variables_config=legacy_input_variables_config
        )
    )
    input_attributes = _normalize_legacy_mkrf_runtime_input_attributes(input_attributes)
    define_columns, required_define_fields = _build_legacy_mkrf_define_column_contract(
        legacy_input_variables_config=legacy_input_variables_config
    )
    define_constants, required_constant_fields = (
        _build_legacy_mkrf_define_constants_contract(
            legacy_input_variables_config=legacy_input_variables_config,
            compatibility_required_constant_keys=compatibility_required_constant_keys,
        )
    )

    root = et.Element(
        "ForestModel",
        {
            "description": description,
            "horizon": str(horizon_years),
            "year": str(start_year),
            "maxage": "350",
            "match": "multi",
        },
    )
    et.SubElement(root, "input", dict(input_attributes))
    et.SubElement(root, "output", dict(DEFAULT_LEGACY_MKRF_OUTPUT_ATTRIBUTES))

    for field, column in define_columns:
        et.SubElement(root, "define", {"field": field, "column": column})
    et.SubElement(root, "define", {"field": "treatment"})
    for field, value in define_constants:
        et.SubElement(root, "define", {"field": field, "constant": value})

    _append_legacy_mkrf_curve_node(
        root=root,
        curve_id="one",
        points=(CurvePoint(x=0.0, y=1.0),),
    )
    for curve in legacy_curve_library_config.get("curves", []) or []:
        curve_id = _normalize_optional_expression(curve.get("curve_id"))
        if curve_id is None:
            raise ValueError(
                "legacy MKRF curve-library contract contains blank curve_id"
            )
        raw_points = curve.get("points")
        if not isinstance(raw_points, list) or not raw_points:
            raise ValueError(
                f"legacy MKRF curve-library contract {curve_id!r} must contain points"
            )
        points = tuple(
            CurvePoint(x=float(point["age"]), y=float(point["value"]))
            for point in raw_points
            if isinstance(point, dict)
        )
        _append_legacy_mkrf_curve_node(root=root, curve_id=curve_id, points=points)
    _append_legacy_mkrf_curves(root=root, curves_by_id=generated_curve_table_by_id)

    for rule in legacy_netdown_config.get("rules", []) or []:
        if str(rule.get("status", "")).strip() != "review_to_build_candidate":
            continue
        statement = _normalize_optional_expression(rule.get("selection_expression"))
        if statement is None:
            raise ValueError("legacy MKRF netdown rule is missing selection_expression")
        select_node = et.SubElement(root, "select", {"statement": statement})
        retention_node = et.SubElement(
            select_node,
            "retention",
            {"factor": str(rule["netdown_proportion"])},
        )
        reassignment = rule.get("reassignment")
        if not isinstance(reassignment, dict):
            raise ValueError("legacy MKRF netdown rule missing reassignment mapping")
        assign_field = _normalize_optional_expression(reassignment.get("field"))
        assign_value = _normalize_optional_expression(reassignment.get("value"))
        if assign_field is None or assign_value is None:
            raise ValueError(
                "legacy MKRF netdown reassignment must define field and value"
            )
        et.SubElement(
            retention_node,
            "assign",
            {"field": assign_field, "value": assign_value},
        )
        features_node = et.SubElement(retention_node, "features")
        for feature_assignment in rule.get("feature_assignments", []) or []:
            if not isinstance(feature_assignment, dict):
                continue
            label = _normalize_optional_expression(feature_assignment.get("feature"))
            if label is None:
                continue
            attribute_attrs = {"label": label}
            factor_value = pd.to_numeric(
                [feature_assignment.get("value", None)], errors="coerce"
            )[0]
            if not pd.isna(factor_value) and not math.isclose(
                float(factor_value), 1.0, rel_tol=0.0, abs_tol=1e-12
            ):
                attribute_attrs["factor"] = _format_xml_y(
                    "legacy_mkrf_factor", float(factor_value)
                )
            attribute_node = et.SubElement(features_node, "attribute", attribute_attrs)
            et.SubElement(attribute_node, "curve", {"idref": "one"})

    unmanaged_statement = "status in unmanaged"
    unmanaged_select = et.SubElement(root, "select", {"statement": unmanaged_statement})
    et.SubElement(unmanaged_select, "track")

    succession_select = et.SubElement(root, "select")
    succession = legacy_treat_config.get("stratum", {}).get("succession", {})
    breakup_at = succession.get(
        "breakup_at", int(DEFAULT_LEGACY_MKRF_SUCCESSION_BREAKUP)
    )
    renewal_age = succession.get(
        "renewal_age", int(DEFAULT_LEGACY_MKRF_SUCCESSION_RENEW)
    )
    et.SubElement(
        succession_select,
        "succession",
        {"breakup": str(breakup_at), "renew": str(renewal_age)},
    )

    for treatment in legacy_treat_config.get("treatments", []) or []:
        treatment_id = _normalize_optional_expression(treatment.get("treatment_id"))
        if treatment_id is None:
            raise ValueError("legacy MKRF treat contract contains blank treatment_id")
        if "blocked_by_stratum_builder" not in str(treatment.get("status", "")).strip():
            continue
        selection = treatment.get("selection")
        if not isinstance(selection, dict):
            raise ValueError(
                f"legacy MKRF treatment {treatment_id!r} missing selection mapping"
            )
        statement = _legacy_mkrf_track_statement_from_selection(selection)
        select_node = et.SubElement(root, "select", {"statement": statement})
        track_node = et.SubElement(select_node, "track")
        treatment_attrs = {"label": treatment_id}
        min_age = _normalize_optional_expression(
            treatment.get("minimum_operable_age_expression")
        ) or _normalize_optional_expression(treatment.get("minimum_operable_age"))
        max_age = _normalize_optional_expression(treatment.get("maximum_operable_age"))
        adjust = _normalize_optional_expression(treatment.get("scheduling_method"))
        retain = _normalize_optional_expression(treatment.get("retention"))
        if min_age is not None:
            treatment_attrs["minage"] = min_age
        if max_age is not None and max_age not in {"", "0"}:
            treatment_attrs["maxage"] = max_age
        if adjust is not None:
            treatment_attrs["adjust"] = adjust
        if retain is not None and retain not in {"", "0", "0.0"}:
            treatment_attrs["retain"] = retain
        treatment_node = et.SubElement(track_node, "treatment", treatment_attrs)
        produce_node = et.SubElement(treatment_node, "produce")
        et.SubElement(
            produce_node,
            "assign",
            {"field": "treatment", "value": _as_quoted_literal(treatment_id)},
        )
        renew = treatment.get("renew")
        if not isinstance(renew, dict):
            raise ValueError(
                f"legacy MKRF treatment {treatment_id!r} missing renew mapping"
            )
        renew_au = _normalize_optional_expression(renew.get("au"))
        if renew_au is None:
            raise ValueError(f"legacy MKRF treatment {treatment_id!r} missing renew.au")
        transition_node = et.SubElement(treatment_node, "transition")
        et.SubElement(transition_node, "assign", {"field": "au", "value": renew_au})

    _reorder_legacy_mkrf_root_children(root=root)

    validate_forestmodel_xml_tree(
        root=root,
        required_define_fields=(
            *required_define_fields,
            *required_constant_fields,
            "treatment",
        ),
        required_curve_ids=(
            "one",
            *[
                str(curve["curve_id"])
                for curve in legacy_curve_library_config.get("curves", []) or []
                if isinstance(curve, dict) and curve.get("curve_id")
            ],
        ),
    )
    return root


def emit_legacy_mkrf_forestmodel_xml(
    *,
    legacy_input_variables_config_path: Path,
    legacy_curve_library_config_path: Path,
    legacy_netdown_config_path: Path,
    legacy_treat_config_path: Path,
    generated_curve_table_csv_path: Path,
    output_path: Path,
    legacy_attributes_config_path: Path | None = None,
    legacy_base_xml_path: Path | None = None,
) -> Path:
    """Emit the opt-in MKRF runtime ForestModel XML from recovered contracts."""
    legacy_input_variables_config = _load_legacy_input_variables_config(
        legacy_input_variables_config_path=legacy_input_variables_config_path
    )
    if legacy_input_variables_config is None:
        raise ValueError(
            "legacy MKRF input-variables config is required for XML emission"
        )
    legacy_curve_library_config = _load_legacy_mkrf_yaml_contract(
        path=legacy_curve_library_config_path,
        contract_label="legacy MKRF curve-library contract",
    )
    legacy_netdown_config = _load_legacy_mkrf_yaml_contract(
        path=legacy_netdown_config_path,
        contract_label="legacy MKRF netdown contract",
    )
    legacy_treat_config = _load_legacy_mkrf_yaml_contract(
        path=legacy_treat_config_path,
        contract_label="legacy MKRF treat contract",
    )
    generated_curve_table_by_id = _load_legacy_mkrf_curve_table(
        curve_table_csv_path=generated_curve_table_csv_path
    )
    root = build_legacy_mkrf_forestmodel_xml_tree(
        legacy_input_variables_config=legacy_input_variables_config,
        legacy_curve_library_config=legacy_curve_library_config,
        legacy_netdown_config=legacy_netdown_config,
        legacy_treat_config=legacy_treat_config,
        generated_curve_table_by_id=generated_curve_table_by_id,
        compatibility_required_constant_keys=("frd",)
        if legacy_attributes_config_path is not None
        else (),
    )
    if legacy_attributes_config_path is not None:
        legacy_attributes_config = _load_legacy_mkrf_yaml_contract(
            path=legacy_attributes_config_path,
            contract_label="legacy MKRF attributes contract",
        )
        native_attribute_selects = _build_legacy_mkrf_native_attribute_selects(
            legacy_attributes_config=legacy_attributes_config
        )
        _validate_legacy_mkrf_native_attributes(
            emitted_root=root,
            selects=native_attribute_selects,
            legacy_attributes_config=legacy_attributes_config,
        )
        for select in native_attribute_selects:
            root.append(copy.deepcopy(select))
        validate_forestmodel_xml_tree(
            root=root,
            required_define_fields=(
                "status",
                "au",
                "auf",
                "oper",
                "ct",
                "aux",
                "treatment",
                "managed",
                "unmanaged",
                "operable",
                "lowoper",
                "frd",
            ),
            required_curve_ids=(
                "one",
                "zero",
                "age",
                "le10",
                "lt20",
                "gt60",
                "lt80",
                "gt250",
            ),
        )
    write_forestmodel_xml(root=root, path=output_path)
    return output_path


__all__ = [
    "build_legacy_mkrf_forestmodel_xml_tree",
    "emit_legacy_mkrf_forestmodel_xml",
]
