# XML Output Staging

`P57.3` / `P57.4` emit the FEMIC-managed MKRF runtime XML at
`XML/baseMKRF.xml`.

Included now:

- `baseMKRF.xml` with the recovered Input Variables contract;
- legacy stratification defines and live scalar constants;
- Curve Library curves plus inlined generated `Yield_*` curves from
  `CSV/CURVE_TABLE.csv`;
- the two Netdown retention rules;
- the unmanaged catch-track;
- default Treat succession; and
- `CC` / `CT` treatment track definitions; and
- the five deferred Attrib compatibility-passthrough `<select>` blocks copied
  from reconciled legacy `baseMKRF.xml`.

Current boundary:

- the Attrib formula-heavy blocks remain compatibility passthrough, not native
  FEMIC attribute-builder output;
- this XML now feeds a successful matrix-build plus launch-proof runtime lane
  when paired with the accepted compiled spatial inputs; and
- this XML alone still does not claim raw-source reconstruction or exact
  legacy-equivalent behavior.
