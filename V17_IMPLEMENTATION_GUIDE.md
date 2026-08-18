# v17 Implementation & Customization Guide

## Architecture decision

v17 deliberately uses static HTML + one CSS file + one browser JavaScript file. The goal is portability and inspectability: the production output does not need a framework server, Node runtime, middleware, or platform-specific API.

The three files to edit most often are:

- `index.html` — content/data/section order.
- `assets/site-v17.css` — typography, spacing, responsive behavior, themes, animation.
- `assets/app-v17.js` — state changes, no-click interactions, deck navigation, table hints, live CISA data.

Run `npm run check && npm run build && npm run postbuild` after meaningful changes.

## HTML edit map

The file is intentionally formatted so line numbers are usable. Major comments:

- Hero / Governance Portfolio: around line 106. Governance stage starts around 232; proof around 349; Signature Operating Model around 431.
- Executive Value: around line 555.
- Architecture: around line 1272. Module rail around 1286. Evidence tables around 1378, 1533 and 1688.
- Selected Systems: around line 2038. Filter rail around 2051; finite deck around 2082.
- Capabilities: around line 2230. Filter rail around 2243; finite deck around 2274.
- Framework Depth: around line 2562; finite deck around 2592.
- Live Public Risk Pulse: around line 2670.
- Direct Conversation: around line 2787.
- Footer / centered Back to Top: around line 2891; button around 3020.

Search for `V17-CUSTOMIZE` instead of relying only on line numbers after future edits.

## CSS edit map

The final v17 override layer begins near the end of `assets/site-v17.css`. The most important selectors are:

- UI font / defensive wrapping: lines ~3415–3465.
- Governance stage + proof separation: ~3469–3555.
- Signature model: ~3558–3610.
- Responsive evidence tables: ~3627–3699.
- AI matrix plot-to-score-card conversion: ~3703–3744.
- Systems/Capabilities/Framework card normalization: ~3748–3769.
- Dynamic Island + icon centering: ~3774–3795.
- Direct Conversation scale: ~3801–3811 plus final override ~3903–3913.
- Live public-risk section: ~3814–3897.
- Reduced-motion guard: ~3899–3901.

Container queries are intentional. They respond to the component’s available width, which is more reliable than assuming that a 1024px viewport always means a 1024px component.

## JavaScript edit map

- Shared geometry helpers: lines ~36–56.
- Theme state: ~58–92.
- Dynamic Island and active section tracking: ~94–147.
- Governance TRACE content and state machine: ~149–290. Edit `TRACE` if stage copy/evidence logic changes.
- Operating model: ~291–348.
- Architecture module switching and adaptive no-click rails: ~349–426.
- Finite decks: ~427–489.
- Risk model / AI matrix behavior: ~490–549.
- Responsive table overflow hints: ~550–564.
- Reveal animation: ~565–593.
- Live CISA KEV data loader: ~594–728.
- Utilities / Back to Top / resize observers: ~729–755.

## Governance Portfolio

The stage cards are one state machine with seven entries: Requirement, Control, Evidence, Exception, Residual Risk, Decision and Monitoring. Pointer movement, stage-number hover/focus, arrows, keyboard and touch all call the same `selectStage()` function. There is no autoplay.

The six-step Signature Operating Model intentionally ends at Decision. When Monitoring is selected, the signature indicator remains on Decision because Monitoring is an additional continuous-governance state rather than a seventh label in the published six-step signature.

To change stage substance, edit the `TRACE` array in `app-v17.js` and the matching card labels in `index.html` together.

## Evidence tables

On roomy containers, the architecture tables render as normal columnar tables. When the table wrapper itself is <=680px, CSS turns each table row into a labeled record card and uses each cell’s `data-label` attribute as the field label. This removes the narrow-screen text collision shown in earlier screenshots.

If a new column is added, add both the `<th>` and the matching `data-label` to each `<td>`.

## AI risk matrix

The desktop/tablet matrix remains a 2D plot with numerical Risk (0–15) and Human Oversight (1–5) values. When the matrix panel is <=760px wide, the same nodes become vertical score cards rather than being squeezed into a small coordinate plane.

Do not fix this with a viewport-only media query; the matrix can live inside a narrow split pane even on a large monitor.

## Finite decks

Selected Systems, Capabilities and Framework Depth are finite; there are no cloned cards, autoplay or wrap-around. Previous/Next buttons call component-local horizontal `scrollTo()`. Scroll/swipe signs are icon-only and appear only when overflow exists.

## Live public-risk pulse

The section reads public CISA KEV data on page load. The first URL is CISA’s official GitHub mirror, which CISA maintains for easier programmatic consumption; the canonical cisa.gov JSON feed is the second source. The section calculates:

- total catalog entries returned by the feed;
- KEV additions in the last 30 days;
- distinct vendors represented in those additions;
- three most recent entries with dates, vendor/product, due date and ransomware-use tag when present.

It then translates each signal into governance actions: confirm exposure/owner, capture remediation evidence, and record exceptions/residual risk when deadlines cannot be met. It does **not** claim that a named prospective employer suffered a breach.

If both live sources fail, values become em dashes and the section states that the live source is unavailable. No stale value is presented as current.

## Theme and typography

Light and dark colors are explicitly guarded near the end of the CSS. Main body/button/table typography uses the local high-quality UI stack (`Avenir Next`, `Aptos`, `Segoe UI Variable Text`, etc.), while major editorial titles keep the serif display stack. There is no remote font dependency.

## Dynamic Island

The closed island stays compact, shows the current section, and exposes eight in-page destinations when opened. It appears only after the visitor has moved beyond the early hero area and suppresses itself near the footer. The `+`/`×` glyph is placed in a fixed 26×26 grid cell so its optical center remains aligned.

## Deployment safety

Cloudflare Pages: Framework preset None, build command `npm run build`, output `out`.

Vercel: repository `vercel.json` sets `framework: null`, `buildCommand: npm run build`, `outputDirectory: out`.

There are no production imports of React, Next.js, D3, Recharts, Lenis or Framer Motion; there is no Node API in the browser runtime.

## Safe-change checklist

1. Edit content/markup, CSS or JS.
2. Preserve `data-*` hooks used by JavaScript unless you update JS at the same time.
3. Keep new card/table text wrapping (`min-width:0`, normal wrapping) rather than fixed widths.
4. Prefer `transform`/`opacity` for animations; do not animate large layout dimensions unless necessary.
5. Preserve `prefers-reduced-motion` behavior.
6. Run preflight/build/postbuild.
7. Re-run browser QA at wide, medium, split-pane and phone widths when layout changes.
8. If the hostname changes, update canonical/OG URL/robots/sitemap together.
