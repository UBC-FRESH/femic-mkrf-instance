# XML Output Staging

`P57.3` emits the first FEMIC-managed MKRF runtime XML at
`XML/baseMKRF.xml`.

Included now:

- `baseMKRF.xml` with the recovered Input Variables contract;
- legacy stratification defines and live scalar constants;
- Curve Library curves plus inlined generated `Yield_*` curves from
  `CSV/CURVE_TABLE.csv`;
- the two Netdown retention rules;
- the unmanaged catch-track;
- default Treat succession; and
- `CC` / `CT` treatment track definitions.

Current boundary:

- no Attrib compatibility-passthrough blocks are materialized here yet;
- no runtime `Tracks/*.csv` outputs are generated here yet; and
- this XML alone is not yet a runnable FEMIC/Patchworks rebuild claim.
