# Md. Abdullah Al Owasi — Portfolio v17

Technology Risk · GRC · TPRM · AI Governance

v17 is a static, zero-browser-package-dependency portfolio designed around adaptive containers rather than one fixed viewport. Production loads one stylesheet (`assets/site-v17.css`) and one browser runtime (`assets/app-v17.js`). It can be built into ordinary static files for Cloudflare Pages, Vercel, or another static host.

## What v17 changes

- Converts the Governance Portfolio snapshot into a clean state machine: pointer glide, numbered controls, keyboard and touch all update the same state without auto-rotation.
- Separates the moving governance stage from its evidence trace so card text cannot layer over proof text.
- Animates the six-step Signature Operating Model marker from Requirement through Decision without adding autoplay.
- Uses container queries to switch architecture evidence tables from columns to labeled record cards when their *actual container* becomes narrow.
- Uses the same container-aware strategy for the AI risk matrix: full 2D risk/oversight plot where space exists, stacked score cards when it does not.
- Keeps Selected Systems, Capabilities and Framework Depth as finite horizontal decks with explicit previous/next controls and no infinite cloning.
- Keeps no-click pointer switching for Architecture, Selected Systems and Capabilities while retaining click/focus/keyboard fallbacks.
- Removes visible instructional prose such as “swipe”, “glide”, “scroll table”, and “grouped swipe deck”; compact directional signs appear only when useful.
- Tightens UI typography, card hierarchy, button geometry and Direct Conversation title scale.
- Adds a live public-risk pulse using CISA’s Known Exploited Vulnerabilities data. The browser tries CISA’s official GitHub mirror first for programmatic reliability and the canonical CISA JSON feed second. If both fail, the section says so and never fabricates current values.
- Keeps strict light/dark theme separation and reduced-motion handling.
- Keeps production free of `scrollIntoView()` and recurring timers to avoid component-driven page jumps and idle animation work.

## Production structure

- `index.html` — semantic content and component markup, with `V17-CUSTOMIZE ...` comments at major edit points.
- `assets/site-v17.css` — complete responsive/theme/animation cascade with maintenance comments.
- `assets/app-v17.js` — interaction runtime and live-risk loader with implementation comments.
- `career-assets/` — resume, cover letter, portfolio, presentation, and the current website code guide.
- `artifacts/` — governance evidence workbooks.
- `scripts/` — preflight, copy build, production-output verification, local static server.
- `validation/` — representative browser QA output and screenshots.
- `out/` — generated production output after `npm run build`.
- `V17_IMPLEMENTATION_GUIDE.md` — edit map and component architecture.
- `V17_VALIDATION_REPORT.md` — measured release checks.
- `AAO_v17_Code_Customization_Guide.docx` — visual line/selector/function guide for future edits.

## Local validation

```bash
npm run check
npm run build
npm run postbuild
npm start
```

The production output directory is `out/`.
