# v17 Validation Report

## Release scope

This release focuses on adaptive layout under constrained widths, text collision removal, component-local scrolling, smooth/no-click interactions, visual hierarchy, current public-risk data and static-host portability.

## Browser regression

Representative Chromium checks were run at 1440, 1024, 768, 620, 540, 430, 390, 360 and 320 CSS pixels. The production HTML/CSS/JS was inlined for deterministic layout testing and the CISA feed was replaced with a mock payload so network availability could not affect UI measurements.

Measured results at every tested width:

- document horizontal overflow: **0 px**;
- Governance number-hover moved to `03 / 07 · Inspectable proof` without click;
- Architecture pointer-hover activated Third-Party Risk;
- Selected Systems pointer-hover activated AI Governance;
- Capabilities pointer-hover activated Automation;
- focus governance card vs proof overlap: **0 px²**;
- focus governance card vs stage controls overlap: **0 px²**;
- AI heat-node overlap: **0 px²**;
- responsive table sibling-cell overlap: **0 px²**;
- Dynamic Island plus/cross vertical-center deviation: **0 px**;
- unexpected vertical scroll movement after settling: **0 px**;
- removed visible instruction/disclaimer strings: absent;
- browser page errors: none.

Direct Conversation title measured about 63.4px at 1440px and 35.1px at 390px after the final scale correction.

The full machine-readable results are in `validation/browser-v17-final.json`.

## Visual QA

Final screenshots under `validation/` confirm:

- clean Governance stage at 390px with no background text layer collision;
- Architecture tables rendered as labeled record cards at 390px;
- AI risk nodes rendered as non-overlapping vertical score cards at narrow width;
- Live Risk Pulse cards and metrics fit a 390px viewport;
- desktop sections remain full data-rich layouts.

## Static checks

Release gate includes:

- `node --check assets/app-v17.js`;
- balanced CSS braces;
- valid JSON package/config files;
- duplicate ID and broken in-page anchor checks;
- broken local asset reference check;
- one production CSS + one production JS runtime;
- no `scrollIntoView()` in component runtime;
- no `setInterval` recurring timer;
- expected counts for governance, modules, tables, decks and Dynamic Island destinations;
- live-risk feed signatures;
- build output verification.

## Deployment model

`npm run build` creates `out/`, a directory of static files. No server-side runtime is required. Cloudflare Pages and Vercel can both publish the generated output using the included settings.

## Limits

No finite test matrix can prove identical behavior on every existing or future browser/device. v17 is designed defensively around fluid layout, container queries, standard pointer/touch/keyboard input, reduced-motion preferences and feature fallbacks, and it was validated across representative narrow-to-wide widths rather than only one laptop/phone size.
