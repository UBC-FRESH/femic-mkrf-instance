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
- no runtime `Tracks/*.csv` outputs are generated here yet; and
- this XML alone is not yet a runnable FEMIC/Patchworks rebuild claim.
