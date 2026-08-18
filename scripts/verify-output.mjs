import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'out');
const required = [
  'index.html','404.html','assets/site-v17.css','assets/app-v17.js',
  'career-assets/Md_Abdullah_Al_Owasi_Resume.docx','career-assets/Md_Abdullah_Al_Owasi_Portfolio.docx',
  'career-assets/Website_Code_Guide.docx','artifacts/Governance_Evidence_Workbook.xlsx','robots.txt','sitemap.xml','_headers'
];
const missing = required.filter((rel) => !fs.existsSync(path.join(out, rel)));
if (missing.length) { console.error('Output verification failed:', missing); process.exit(1); }
const html = fs.readFileSync(path.join(out,'index.html'),'utf8');
for (const sig of [
  'site-v17.css','app-v17.js','data-auto-rail="architecture"','data-auto-rail="systems"','data-auto-rail="capabilities"',
  'data-deck-track="systems"','data-deck-track="capabilities"','data-deck-track="frameworks"','data-responsive-table="1"',
  'theme-bound-contact','data-governance-proof','governance-proof-v17','signature-model-v17','risk-compression-panel','matrix-summary','module-lattice','data-live-risk'
]) if (!html.includes(sig)) { console.error(`Output HTML signature missing: ${sig}`); process.exit(1); }
if (/src=["']\/assets\/(?:app\.js|app-v16\.js|premium-v1[23456]\.js)/.test(html)) { console.error('Historical runtime script is still linked.'); process.exit(1); }
const js = fs.readFileSync(path.join(out,'assets/app-v17.js'),'utf8');
if (js.includes('scrollIntoView(')) { console.error('Unsafe scrollIntoView() present in production runtime.'); process.exit(1); }
if (js.includes('setInterval')) { console.error('Recurring timer present in production runtime.'); process.exit(1); }
if (!js.includes('cisagov/kev-data')) { console.error('CISA official GitHub mirror fallback missing.'); process.exit(1); }
console.log(`Output verified: ${required.length} critical files present, v17 CSS/JS runtime linked, responsive governance/table/matrix structures present, live-risk feed configured, no recurring timers, and scroll-jump guard passed.`);
