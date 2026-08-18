import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = (rel) => fs.readFileSync(path.join(root, rel), 'utf8');
const required = [
  'index.html',
  'assets/site-v17.css', 'assets/app-v17.js',
  'career-assets/Md_Abdullah_Al_Owasi_Resume.docx', 'career-assets/Md_Abdullah_Al_Owasi_Cover_Letter.docx',
  'career-assets/Md_Abdullah_Al_Owasi_Portfolio.docx', 'career-assets/Md_Abdullah_Al_Owasi_Executive_Portfolio.pdf',
  'career-assets/Md_Abdullah_Al_Owasi_Presentation.pptx',
  'artifacts/Governance_Evidence_Matrix.xlsx', 'artifacts/Governance_Evidence_Workbook.xlsx',
  'robots.txt', 'sitemap.xml', '_headers', 'vercel.json', 'DEPLOYMENT.md',
  'V17_IMPLEMENTATION_GUIDE.md', 'V17_VALIDATION_REPORT.md', 'AAO_v17_Code_Customization_Guide.docx'
];

const errors = [];
for (const rel of required) if (!fs.existsSync(path.join(root, rel))) errors.push(`Missing: ${rel}`);

const html = read('index.html');
const css = read('assets/site-v17.css');
const js = read('assets/app-v17.js');
for (const token of ['next/','motion/react','recharts','d3','lenis']) {
  if (html.includes(token) || js.includes(token)) errors.push(`Runtime dependency token found: ${token}`);
}
if (/<script[^>]+src=["']https?:/i.test(html) || /<link[^>]+href=["']https?:[^>]+stylesheet/i.test(html)) errors.push('External runtime CSS/JS dependency detected.');
if ((css.match(/{/g)||[]).length !== (css.match(/}/g)||[]).length) errors.push('CSS braces are unbalanced.');
try { new Function(js); } catch (error) { errors.push(`app-v17.js syntax error: ${error.message}`); }
for (const rel of ['package.json','package-lock.json','vercel.json']) {
  try { JSON.parse(read(rel)); } catch (error) { errors.push(`Invalid JSON: ${rel} (${error.message})`); }
}
const localRefs = [...html.matchAll(/(?:href|src)=["']\/(?!\/)([^"'#?]+)["']/g)].map((m) => m[1]);
for (const rel of localRefs) if (!rel.endsWith('/') && !fs.existsSync(path.join(root, rel))) errors.push(`Broken local reference: /${rel}`);
const idList = [...html.matchAll(/\sid=["']([^"']+)["']/g)].map((m) => m[1]);
const ids = new Set(idList);
for (const id of ids) if (idList.filter((value) => value === id).length > 1) errors.push(`Duplicate id: #${id}`);
for (const match of html.matchAll(/href=["']#([^"']+)["']/g)) if (!ids.has(match[1])) errors.push(`Broken anchor: #${match[1]}`);
const count = (re) => (html.match(re) || []).length;
if (count(/data-flow-index=/g) !== 6) errors.push('Operating model must have 6 stages.');
if (count(/class="heat-node/g) !== 7) errors.push('AI matrix must have 7 use cases.');
if (count(/data-governance-index=/g) !== 7 || count(/data-stage-goto=/g) !== 7) errors.push('Hero governance controls incomplete.');
if (count(/data-island-link/g) !== 8) errors.push('Dynamic Island must contain 8 destinations.');
if (count(/data-responsive-table=/g) !== 3 || count(/data-overflow-note=/g) !== 3) errors.push('Architecture table overflow instrumentation incomplete.');
if (count(/data-deck-track=/g) !== 3 || count(/data-deck-prev=/g) !== 3 || count(/data-deck-next=/g) !== 3) errors.push('Finite deck controls incomplete.');
if (count(/data-auto-rail=/g) !== 3) errors.push('Architecture, Systems and Capabilities must expose adaptive no-click rails.');
if (count(/class="module-lattice/g) !== 3) errors.push('Each architecture module must expose a 3-step decision lattice.');
if (count(/data-risk=/g) < 7 || count(/data-oversight=/g) < 7) errors.push('AI matrix numerical values missing.');
for (const visibleInstruction of [
  'Move across categories · swipe on touch · click remains optional',
  'Glide on desktop · scroll on touch · the centered stage updates automatically',
  'Integrated modules · move across on desktop · swipe on touch',
  'Capabilities · grouped swipe deck · Scroll / Swipe →',
  'Example only — demonstrates the decision lineage; it is not presented as production operating data.'
]) if (html.includes(visibleInstruction)) errors.push(`Removed instruction/disclaimer still present: ${visibleInstruction}`);
if (!html.includes('theme-bound-contact')) errors.push('Theme-bound Direct Conversation marker missing.');
if (!html.includes('/assets/site-v17.css') || !html.includes('/assets/app-v17.js')) errors.push('v17 consolidated CSS/JS is not linked.');
if (/src=["']\/assets\/(?:app\.js|app-v16\.js|premium-v1[23456]\.js)/.test(html)) errors.push('Historical JS runtime is still linked; v17 must have a single runtime.');
if (js.includes('scrollIntoView(')) errors.push('Component runtime must not use scrollIntoView(); it can cause document jumps.');
if (js.includes('setInterval')) errors.push('Recurring timer detected; production runtime must remain idle when the user is idle.');
if (!html.includes('data-governance-proof') || !html.includes('risk-compression-panel') || !html.includes('matrix-summary')) errors.push('Precision visuals are incomplete.');
if (!html.includes('governance-proof-v17') || !html.includes('signature-model-v17')) errors.push('v17 governance proof/signature model is incomplete.');
if (!html.includes('data-live-risk') || !html.includes('live-risk-pulse') || !js.includes('cisagov/kev-data')) errors.push('Live public-risk pulse is incomplete.');
if (count(/data-top/g) !== 1 || !html.includes('footer-backtop')) errors.push('Back-to-top must exist exactly once in the footer center container.');
const canonical = html.match(/<link href="([^"]+)" rel="canonical"/i)?.[1] || html.match(/<link rel="canonical" href="([^"]+)"/i)?.[1];
if (!canonical) errors.push('Canonical URL missing.');
else {
  const origin = canonical.replace(/\/$/, '');
  if (!read('robots.txt').includes(origin)) errors.push('robots.txt canonical mismatch.');
  if (!read('sitemap.xml').includes(origin)) errors.push('sitemap canonical mismatch.');
}
if (errors.length) {
  console.error('Preflight failed');
  for (const error of [...new Set(errors)]) console.error(` - ${error}`);
  process.exit(1);
}
console.log(`Preflight passed: ${required.length} required assets, v17 single CSS/JS runtime, 3 adaptive no-click rails, 3 finite decks, 3 responsive tables, 7-stage governance selector, live CISA KEV pulse, no recurring timers, and zero external runtime dependencies.`);
