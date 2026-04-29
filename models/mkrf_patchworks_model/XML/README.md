# XML Output Staging

`P57.3` through `P58.2` emit the FEMIC-managed MKRF runtime XML at
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
- the native Attrib feature/product `<select>` blocks rebuilt from the
  reviewed workbook extracts.

Current boundary:

- this XML now feeds a successful matrix-build plus launch-proof runtime lane
  when paired with the accepted compiled spatial inputs; and
- this XML alone still does not claim raw-source reconstruction or exact
  legacy-equivalent behavior.
