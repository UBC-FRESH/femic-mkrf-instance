from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as et

from femic.fmg.core import CurvePoint
from femic.fmg.patchworks import validate_forestmodel_xml_tree
from mkrf_femic.legacy_xml import (
    build_legacy_mkrf_forestmodel_xml_tree,
    emit_legacy_mkrf_forestmodel_xml,
)
import pytest
import yaml


def test_build_legacy_mkrf_forestmodel_xml_tree_emits_recovered_contract_sections() -> (
    None
):
    instance_root = Path(".")
    input_variables_path = (
        instance_root / "config/legacy_xml_builder/input_variables.mkrf.yaml"
    )
    curve_library_path = (
        instance_root / "config/legacy_xml_builder/curve_library.mkrf.yaml"
    )
    netdown_path = instance_root / "config/legacy_xml_builder/netdown.mkrf.yaml"
    treat_path = instance_root / "config/legacy_xml_builder/strata/treat.mkrf.yaml"
    curve_table_path = (
        instance_root / "data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv"
    )
    if not all(
        path.exists()
        for path in (
            input_variables_path,
            curve_library_path,
            netdown_path,
            treat_path,
            curve_table_path,
        )
    ):
        pytest.skip("MKRF instance contracts are not materialized")

    root = build_legacy_mkrf_forestmodel_xml_tree(
        legacy_input_variables_config=yaml.safe_load(
            input_variables_path.read_text(encoding="utf-8")
        ),
        legacy_curve_library_config=yaml.safe_load(
            curve_library_path.read_text(encoding="utf-8")
        ),
        legacy_netdown_config=yaml.safe_load(netdown_path.read_text(encoding="utf-8")),
        legacy_treat_config=yaml.safe_load(treat_path.read_text(encoding="utf-8")),
        generated_curve_table_by_id={
            curve_id: tuple(points)
            for curve_id, points in {
                "Yield_1": (
                    CurvePoint(x=0.0, y=27.9345),
                    CurvePoint(x=10.0, y=27.9345),
                ),
                "Yield_2": (
                    CurvePoint(x=0.0, y=30.0),
                    CurvePoint(x=10.0, y=31.5),
                ),
            }.items()
        },
    )

    assert root.attrib == {
        "description": "Base TFL26",
        "horizon": "300",
        "year": "2020",
        "maxage": "350",
        "match": "multi",
    }
    input_node = root.find("./input")
    assert input_node is not None
    assert input_node.attrib == {
        "block": "Int(RES_KEY)",
        "area": "Shape_Area/10000",
        "age": "Int(AGE_2020)",
        "exclude": "CONTCLAS eq 'X'",
    }
    root_tags = [child.tag for child in list(root)]
    first_define_index = root_tags.index("define")
    first_input_index = root_tags.index("input")
    first_output_index = root_tags.index("output")
    assert all(tag == "curve" for tag in root_tags[:first_define_index])
    assert all(
        tag == "define" for tag in root_tags[first_define_index:first_input_index]
    )
    assert root_tags[first_input_index : first_output_index + 1] == ["input", "output"]
    output_node = root.find("./output")
    assert output_node is not None
    assert output_node.attrib["features"] == "features.csv"
    define_fields = [node.attrib["field"] for node in root.findall("./define")]
    assert define_fields == [
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
    ]
    assert root.find("./define[@field='frd']") is None
    assert root.find("./curve[@id='one']") is not None
    assert root.find("./curve[@id='zero']") is not None
    assert root.find("./curve[@id='Yield_1']") is not None
    assert root.find("./curve[@id='Yield_2']") is not None
    retention_selects = root.findall("./select[retention]")
    assert [node.attrib["statement"] for node in retention_selects] == [
        "status in managed and oper in operable",
        "status in managed and oper in lowoper",
    ]
    unmanaged_select = root.find("./select[@statement='status in unmanaged']")
    assert unmanaged_select is not None
    assert unmanaged_select.find("./track") is not None
    succession = root.find("./select/succession")
    assert succession is not None
    assert succession.attrib == {"breakup": "999", "renew": "0"}
    cc_treatment = root.find("./select[@statement='status in managed']/track/treatment")
    assert cc_treatment is not None
    assert cc_treatment.attrib == {
        "label": "CC",
        "minage": "if(oper in operable, 60, 150)",
    }
    ct_treatment = root.find(
        "./select[@statement=\"status in managed and oper in operable and ct eq 'Y' "
        "and not startswith(au,'t')\"]/track/treatment"
    )
    assert ct_treatment is not None
    assert ct_treatment.attrib == {
        "label": "CT",
        "minage": "40",
        "maxage": "150",
        "retain": "20",
    }


def test_emit_legacy_mkrf_forestmodel_xml_writes_runtime_base_xml(
    tmp_path: Path,
) -> None:
    instance_root = Path(".")
    input_variables_path = (
        instance_root / "config/legacy_xml_builder/input_variables.mkrf.yaml"
    )
    curve_library_path = (
        instance_root / "config/legacy_xml_builder/curve_library.mkrf.yaml"
    )
    netdown_path = instance_root / "config/legacy_xml_builder/netdown.mkrf.yaml"
    treat_path = instance_root / "config/legacy_xml_builder/strata/treat.mkrf.yaml"
    curve_table_path = (
        instance_root / "data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv"
    )
    if not all(
        path.exists()
        for path in (
            input_variables_path,
            curve_library_path,
            netdown_path,
            treat_path,
            curve_table_path,
        )
    ):
        pytest.skip("MKRF instance contracts are not materialized")

    output_path = tmp_path / "XML" / "baseMKRF.xml"
    emitted = emit_legacy_mkrf_forestmodel_xml(
        legacy_input_variables_config_path=input_variables_path,
        legacy_curve_library_config_path=curve_library_path,
        legacy_netdown_config_path=netdown_path,
        legacy_treat_config_path=treat_path,
        generated_curve_table_csv_path=curve_table_path,
        output_path=output_path,
    )

    assert emitted == output_path
    assert emitted.exists()
    root = et.parse(emitted).getroot()
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
    assert root.find("./curve[@id='Yield_1']") is not None


def test_emit_legacy_mkrf_forestmodel_xml_emits_native_attrib_blocks(
    tmp_path: Path,
) -> None:
    instance_root = Path(".")
    input_variables_path = (
        instance_root / "config/legacy_xml_builder/input_variables.mkrf.yaml"
    )
    curve_library_path = (
        instance_root / "config/legacy_xml_builder/curve_library.mkrf.yaml"
    )
    netdown_path = instance_root / "config/legacy_xml_builder/netdown.mkrf.yaml"
    treat_path = instance_root / "config/legacy_xml_builder/strata/treat.mkrf.yaml"
    attributes_path = instance_root / "config/legacy_xml_builder/attributes.mkrf.yaml"
    curve_table_path = (
        instance_root / "data/legacy_mkrf/generated_xml/CSV/CURVE_TABLE.csv"
    )
    if not all(
        path.exists()
        for path in (
            input_variables_path,
            curve_library_path,
            netdown_path,
            treat_path,
            attributes_path,
            curve_table_path,
        )
    ):
        pytest.skip("MKRF instance contracts are not materialized")

    output_path = tmp_path / "XML" / "baseMKRF.xml"
    emitted = emit_legacy_mkrf_forestmodel_xml(
        legacy_input_variables_config_path=input_variables_path,
        legacy_curve_library_config_path=curve_library_path,
        legacy_netdown_config_path=netdown_path,
        legacy_treat_config_path=treat_path,
        generated_curve_table_csv_path=curve_table_path,
        output_path=output_path,
        legacy_attributes_config_path=attributes_path,
    )

    assert emitted == output_path
    root = et.parse(emitted).getroot()
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
    assert len(root.findall("./select")) == 11
    assert root.find("./define[@field='frd']") is not None
    assert root.find(".//features/attribute[@label='%f.area.%m.total']") is not None
    assert (
        root.find(".//features/attribute[@label='%f.yield.%m.merch.total']") is not None
    )
    assert (
        root.find(".//features/attribute[@label='%f.area.%m.seral.le10']") is not None
    )
    ba_species = root.find(".//features/attribute[@label='%f.yield.%m.indsp.Ba']")
    assert ba_species is not None
    assert "Number(lookupTable(au,'" in ba_species.attrib["factor"]
