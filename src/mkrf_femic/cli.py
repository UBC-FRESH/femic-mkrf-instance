"""Command line interface for MKRF-owned FEMIC workflow implementation."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from mkrf_femic.workflows.mkrf import (
    audit_mkrf_runtime_sanity,
    build_mkrf_bad_curve_audit,
    build_mkrf_all_plots,
    build_mkrf_au_distribution_plot,
    build_mkrf_au_input_bundle,
    build_mkrf_first_growth_input_bundle,
    build_mkrf_managed_au_curves,
    build_mkrf_managed_au_input_bundle,
    build_mkrf_selected_au_input_bundle,
    initialize_mkrf_runtime_package,
    publish_mkrf_runtime_spatial_handoff,
)

console = Console()
app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="MKRF-owned FEMIC workflow commands.",
)
INSTANCE_ROOT_OPTION = typer.Option(
    None,
    "--instance-root",
    help="Path to the MKRF instance root. Defaults to the current directory.",
)


class _InstanceContext:
    def __init__(self, instance_root: Path) -> None:
        self.instance_root = instance_root.resolve()

    def resolve_path(self, path: Path) -> Path:
        if path.is_absolute():
            return path
        return self.instance_root / path


def _resolve_cli_instance_context(*, instance_root: Path | None) -> _InstanceContext:
    return _InstanceContext(instance_root or Path("."))


@app.command("mkrf-build-au-inputs")
def instance_mkrf_build_au_inputs(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb directory.",
    ),
    output_dir: Path = typer.Option(
        Path("data/model_input_bundle"),
        "--output-dir",
        help="Instance-relative output directory for AU input bundle CSVs.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Build MKRF AU and stand-assignment inputs from Resultant.gdb."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_au_input_bundle(
        resultant_gdb=resultant_gdb,
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf au inputs built[/green] "
        f"source_rows={result.source_row_count} aus={result.au_count}"
    )
    console.print(f"au_table: {result.au_table_path}")
    console.print(f"stand_assignment: {result.stand_assignment_path}")


@app.command("mkrf-build-first-growth-curves")
def instance_mkrf_build_first_growth_curves(
    vdyp_yields_csv: Path = typer.Option(
        ...,
        "--vdyp-yields-csv",
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF VDYP_Yields.csv file.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb used for lexmatch fallback.",
    ),
    output_dir: Path = typer.Option(
        Path("data/model_input_bundle"),
        "--output-dir",
        help="Instance-relative output directory for AU-wise first-growth CSVs.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Build MKRF AU-wise first-growth curves from VDYP stand evidence."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_first_growth_input_bundle(
        vdyp_yields_csv=vdyp_yields_csv,
        assignment_csv=context.resolve_path(assignment_csv),
        resultant_gdb=resultant_gdb,
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf first-growth curves built[/green] "
        f"aus={result.au_count} assigned_stands={result.assigned_stand_count} "
        f"raw_unmatched_source_stands={result.raw_unmatched_source_stand_count} "
        f"residual_unmatched_source_stands={result.residual_unmatched_source_stand_count} "
        f"lexmatch_assigned_stands={result.lexmatch_assigned_stand_count}"
    )
    console.print(f"curves: {result.curves_path}")
    console.print(f"diagnostics: {result.diagnostics_path}")


@app.command("mkrf-plot-au-distribution")
def instance_mkrf_plot_au_distribution(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb source surface.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    selected_au_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--selected-au-csv",
        help="Instance-relative selected-AU table CSV used to filter the plotted subset.",
    ),
    output_dir: Path = typer.Option(
        Path("plots"),
        "--output-dir",
        help="Instance-relative output directory for AU distribution plots.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Build the MKRF AU abundance/site-index distribution plot."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_au_distribution_plot(
        resultant_gdb=resultant_gdb,
        assignment_csv=context.resolve_path(assignment_csv),
        selected_au_csv=context.resolve_path(selected_au_csv),
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf au distribution plot built[/green] "
        f"aus={result.au_count} site_index_points={result.point_count}"
    )
    console.print(f"png: {result.png_path}")
    console.print(f"pdf: {result.pdf_path}")


@app.command("mkrf-select-aus")
def instance_mkrf_select_aus(
    au_table_csv: Path = typer.Option(
        Path("data/model_input_bundle/au_table.csv"),
        "--au-table-csv",
        help="Instance-relative canonical AU table CSV.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    output_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--output-csv",
        help="Instance-relative output CSV for the selected top-N AU subset.",
    ),
    target_coverage: float = typer.Option(
        0.95,
        "--target-coverage",
        min=0.0,
        max=1.0,
        help="Cumulative covered-area share cutoff for the selected AU subset.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Publish the canonical top-N AU subset by cumulative covered-area share."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_selected_au_input_bundle(
        au_table_csv=context.resolve_path(au_table_csv),
        assignment_csv=context.resolve_path(assignment_csv),
        output_path=context.resolve_path(output_csv),
        target_coverage=target_coverage,
    )
    console.print(
        "[green]mkrf selected au table built[/green] "
        f"selected_aus={result.selected_au_count} total_aus={result.total_au_count} "
        f"target_coverage={result.target_coverage:.3f} "
        f"realized_coverage={result.realized_coverage:.6f}"
    )
    console.print(f"selected_au_table: {result.output_path}")


@app.command("mkrf-recompile-plots")
def instance_mkrf_recompile_plots(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb source surface.",
    ),
    vdyp_yields_csv: Path = typer.Option(
        ...,
        "--vdyp-yields-csv",
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF VDYP_Yields.csv file.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    selected_au_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--selected-au-csv",
        help="Instance-relative selected-AU table CSV.",
    ),
    first_growth_curves_csv: Path = typer.Option(
        Path("data/model_input_bundle/first_growth_au_curves.csv"),
        "--first-growth-curves-csv",
        help="Instance-relative AU-wise first-growth curves CSV.",
    ),
    managed_curves_csv: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_curves.csv"),
        "--managed-curves-csv",
        help="Instance-relative AU-wise managed curves CSV.",
    ),
    output_dir: Path = typer.Option(
        Path("plots"),
        "--output-dir",
        help="Instance-relative output directory for regenerated plots.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Rebuild the MKRF AU strata, VDYP diagnostics, and TIPSY comparison plots."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_all_plots(
        resultant_gdb=resultant_gdb,
        assignment_csv=context.resolve_path(assignment_csv),
        selected_au_csv=context.resolve_path(selected_au_csv),
        first_growth_curves_csv=context.resolve_path(first_growth_curves_csv),
        managed_curves_csv=context.resolve_path(managed_curves_csv),
        vdyp_yields_csv=vdyp_yields_csv,
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf plots rebuilt[/green] "
        f"lmh={result.lmh_plot_count} "
        f"fitdiag={result.fitdiag_plot_count} "
        f"tipsy_vdyp={result.tipsy_vdyp_plot_count}"
    )
    console.print(f"strata_png: {result.strata_png}")
    console.print(f"strata_pdf: {result.strata_pdf}")


@app.command("mkrf-audit-bad-curves")
def instance_mkrf_audit_bad_curves(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb source surface.",
    ),
    vdyp_yields_csv: Path = typer.Option(
        ...,
        "--vdyp-yields-csv",
        exists=True,
        dir_okay=False,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF VDYP_Yields.csv file.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    selected_au_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--selected-au-csv",
        help="Instance-relative selected-AU table CSV.",
    ),
    first_growth_curves_csv: Path = typer.Option(
        Path("data/model_input_bundle/first_growth_au_curves.csv"),
        "--first-growth-curves-csv",
        help="Instance-relative AU-wise first-growth curves CSV.",
    ),
    output_dir: Path = typer.Option(
        Path("data/model_input_bundle"),
        "--output-dir",
        help="Instance-relative output directory for bad-curve audit CSVs.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Audit suspicious MKRF first-growth curve cases against source-stand evidence."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_bad_curve_audit(
        resultant_gdb=resultant_gdb,
        assignment_csv=context.resolve_path(assignment_csv),
        selected_au_csv=context.resolve_path(selected_au_csv),
        first_growth_curves_csv=context.resolve_path(first_growth_curves_csv),
        vdyp_yields_csv=vdyp_yields_csv,
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf bad-curve audit built[/green] "
        f"flagged_aus={result.flagged_au_count} "
        f"selected_aus={result.total_selected_au_count}"
    )
    console.print(f"summary_csv: {result.summary_path}")
    console.print(f"detail_csv: {result.detail_path}")


@app.command("mkrf-build-managed-au-inputs")
def instance_mkrf_build_managed_au_inputs(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb source surface.",
    ),
    tipsy_rules_yaml: Path = typer.Option(
        Path("config/tipsy/tsamkrf.yaml"),
        "--tipsy-rules-yaml",
        help="Instance-relative managed-rule YAML used for expert planting specs.",
    ),
    selected_au_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--selected-au-csv",
        help="Instance-relative selected-AU table CSV.",
    ),
    assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--assignment-csv",
        help="Instance-relative stand-to-AU assignment CSV.",
    ),
    output_dir: Path = typer.Option(
        Path("data/model_input_bundle"),
        "--output-dir",
        help="Instance-relative output directory for managed AU bundle artifacts.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Build the expert-rule managed AU bootstrap and BTC MSYT surfaces."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_managed_au_input_bundle(
        resultant_gdb=resultant_gdb,
        selected_au_csv=context.resolve_path(selected_au_csv),
        assignment_csv=context.resolve_path(assignment_csv),
        tipsy_rules_yaml=context.resolve_path(tipsy_rules_yaml),
        output_dir=context.resolve_path(output_dir),
    )
    console.print(
        "[green]mkrf managed au inputs built[/green] "
        f"selected_aus={result.selected_au_count} "
        f"included_aus={result.included_au_count} "
        f"unmatched_aus={result.unmatched_au_count} "
        f"logging_origin_si={result.logging_origin_si_au_count} "
        f"all_stands_fallback={result.all_stands_si_fallback_au_count}"
    )
    console.print(f"stand_origin_assignment: {result.stand_origin_assignment_path}")
    console.print(f"bootstrap_table: {result.bootstrap_table_path}")
    console.print(f"managed_au_msyt: {result.msyt_path}")


@app.command("mkrf-build-managed-au-curves")
def instance_mkrf_build_managed_au_curves(
    bootstrap_csv: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_bootstrap_table.csv"),
        "--bootstrap-csv",
        help="Instance-relative managed AU bootstrap table CSV.",
    ),
    msyt_csv: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_msyt.csv"),
        "--msyt-csv",
        help="Instance-relative managed AU BTC MSYT.csv input.",
    ),
    output_dir: Path = typer.Option(
        Path("data/model_input_bundle"),
        "--output-dir",
        help="Instance-relative output directory for managed AU BTC artifacts.",
    ),
    log_dir: Path = typer.Option(
        Path("runtime/logs/managed_au_btc"),
        "--log-dir",
        help="Instance-relative output directory for BTC runtime logs.",
    ),
    run_id: str = typer.Option(
        "mkrf_managed_au_curves",
        "--run-id",
        help="Run identifier for the managed AU BTC attempt.",
    ),
    btc_executable: Path | None = typer.Option(
        None,
        "--btc-executable",
        exists=False,
        resolve_path=True,
        help="Optional explicit TIPSYbtc.exe path override.",
        show_default=False,
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Attempt a BTC compile for the provisional managed AU lane."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = build_mkrf_managed_au_curves(
        bootstrap_csv=context.resolve_path(bootstrap_csv),
        msyt_csv=context.resolve_path(msyt_csv),
        output_dir=context.resolve_path(output_dir),
        log_dir=context.resolve_path(log_dir),
        run_id=run_id,
        executable_path=btc_executable,
    )
    color = "green" if result.status == "completed" else "yellow"
    console.print(
        f"[{color}]mkrf managed au btc attempt {result.status}[/{color}] "
        f"included_aus={result.included_au_count} curve_aus={result.curve_au_count}"
    )
    console.print(f"manifest: {result.manifest_path}")
    if result.curves_path is not None:
        console.print(f"managed_au_curves: {result.curves_path}")


@app.command("mkrf-init-runtime-package")
def instance_mkrf_init_runtime_package(
    package_root: Path = typer.Option(
        Path("models/mkrf_patchworks_model"),
        "--package-root",
        help="Instance-relative canonical MKRF runtime-package root.",
    ),
    selected_au_csv: Path = typer.Option(
        Path("data/model_input_bundle/selected_au_table.csv"),
        "--selected-au-csv",
        help="Instance-relative selected-AU table CSV.",
    ),
    stand_origin_assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_origin_assignment.csv"),
        "--stand-origin-assignment-csv",
        help="Instance-relative stand-to-rebuild-AU assignment CSV.",
    ),
    stand_au_assignment_csv: Path = typer.Option(
        Path("data/model_input_bundle/stand_au_assignment.csv"),
        "--stand-au-assignment-csv",
        help="Instance-relative stand-to-AU/species-share assignment CSV.",
    ),
    managed_bootstrap_csv: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_bootstrap_table.csv"),
        "--managed-bootstrap-csv",
        help="Instance-relative managed AU bootstrap/species-composition CSV.",
    ),
    first_growth_curves_csv: Path = typer.Option(
        Path("data/model_input_bundle/first_growth_au_curves.csv"),
        "--first-growth-curves-csv",
        help="Instance-relative AU-wise first-growth curves CSV.",
    ),
    first_growth_diagnostics_csv: Path = typer.Option(
        Path("data/model_input_bundle/first_growth_au_fit_diagnostics.csv"),
        "--first-growth-diagnostics-csv",
        help="Instance-relative AU-wise first-growth diagnostics CSV.",
    ),
    managed_curves_csv: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_curves.csv"),
        "--managed-curves-csv",
        help="Instance-relative managed AU curves CSV.",
    ),
    managed_run_manifest_json: Path = typer.Option(
        Path("data/model_input_bundle/managed_au_run_manifest.json"),
        "--managed-run-manifest-json",
        help="Instance-relative managed AU run manifest JSON.",
    ),
    bad_curve_audit_summary_csv: Path = typer.Option(
        Path("data/model_input_bundle/bad_curve_audit_summary.csv"),
        "--bad-curve-audit-summary-csv",
        help="Instance-relative bad-curve audit summary CSV.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Initialize the canonical MKRF runtime-package root and lineage manifest."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = initialize_mkrf_runtime_package(
        package_root=context.resolve_path(package_root),
        selected_au_csv=context.resolve_path(selected_au_csv),
        stand_origin_assignment_csv=context.resolve_path(stand_origin_assignment_csv),
        stand_au_assignment_csv=context.resolve_path(stand_au_assignment_csv),
        managed_bootstrap_csv=context.resolve_path(managed_bootstrap_csv),
        first_growth_curves_csv=context.resolve_path(first_growth_curves_csv),
        first_growth_diagnostics_csv=context.resolve_path(first_growth_diagnostics_csv),
        managed_curves_csv=context.resolve_path(managed_curves_csv),
        managed_run_manifest_json=context.resolve_path(managed_run_manifest_json),
        bad_curve_audit_summary_csv=context.resolve_path(bad_curve_audit_summary_csv),
    )
    console.print(
        "[green]mkrf runtime package initialized[/green] "
        f"selected_aus={result.selected_au_count} "
        f"first_growth_aus={result.first_growth_curve_au_count} "
        f"managed_curve_aus={result.managed_curve_au_count} "
        f"first_growth_missing_aus={result.first_growth_missing_au_count}"
    )
    console.print(f"package_root: {result.package_root}")
    console.print(f"manifest: {result.manifest_path}")
    console.print(f"curve_status_csv: {result.curve_status_path}")
    console.print(
        f"analysis_au_runtime_status_csv: {result.analysis_au_runtime_status_path}"
    )
    console.print(f"analysis_au_curve_refs_csv: {result.analysis_au_curve_refs_path}")
    console.print(f"runtime_species_share_audit_csv: {result.species_share_audit_path}")
    console.print(f"analysis_pin: {result.analysis_pin_path}")
    console.print(f"headless_runtime_common_bsh: {result.headless_runtime_common_path}")
    console.print(f"flow_targets_bsh: {result.flow_targets_script_path}")
    console.print(f"xml_contract: {result.xml_contract_path}")
    console.print(f"xml_curve_bank: {result.xml_curve_bank_path}")
    console.print(f"forestmodel_xml: {result.forestmodel_xml_path}")


@app.command("mkrf-audit-runtime-sanity")
def instance_mkrf_audit_runtime_sanity(
    package_root: Path = typer.Option(
        Path("models/mkrf_patchworks_model"),
        "--package-root",
        help="Instance-relative canonical MKRF runtime-package root.",
    ),
    stage_dir: Path = typer.Option(
        ...,
        "--stage-dir",
        exists=True,
        dir_okay=True,
        file_okay=False,
        resolve_path=True,
        help="Absolute or repo-relative saved headless stage directory to audit.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Audit canonical MKRF runtime signal against published species-share sources."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = audit_mkrf_runtime_sanity(
        package_root=context.resolve_path(package_root),
        stage_dir=stage_dir.resolve(),
    )
    color = "green" if result.failure_count == 0 else "yellow"
    console.print(
        f"[{color}]mkrf runtime sanity audit complete[/{color}] "
        f"rows={result.row_count} failures={result.failure_count}"
    )
    console.print(f"stage_dir: {result.stage_dir}")
    console.print(f"audit_csv: {result.audit_csv_path}")
    console.print(f"summary_json: {result.summary_json_path}")


@app.command("mkrf-publish-runtime-spatial")
def instance_mkrf_publish_runtime_spatial(
    resultant_gdb: Path = typer.Option(
        ...,
        "--resultant-gdb",
        exists=True,
        dir_okay=True,
        file_okay=True,
        resolve_path=True,
        help="Path to the upstream MKRF Resultant.gdb source surface.",
    ),
    package_root: Path = typer.Option(
        Path("models/mkrf_patchworks_model"),
        "--package-root",
        help="Instance-relative canonical MKRF runtime-package root.",
    ),
    instance_root: Path | None = INSTANCE_ROOT_OPTION,
) -> None:
    """Publish canonical MKRF runtime fragments from Resultant.gdb."""
    context = _resolve_cli_instance_context(instance_root=instance_root)
    result = publish_mkrf_runtime_spatial_handoff(
        resultant_gdb=resultant_gdb,
        package_root=context.resolve_path(package_root),
    )
    console.print(
        "[green]mkrf runtime spatial published[/green] "
        f"source_features={result.source_feature_count} "
        f"published_features={result.published_feature_count} "
        f"excluded_features={result.excluded_feature_count}"
    )
    console.print(f"fragments: {result.fragments_path}")
    console.print(f"manifest: {result.manifest_path}")
