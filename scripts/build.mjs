import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, 'out');
const copyTargets = ['index.html', 'assets', 'career-assets', 'robots.txt', 'sitemap.xml', '_headers'];

fs.rmSync(out, { recursive: true, force: true });
fs.mkdirSync(out, { recursive: true });

function copy(src, dst) {
  const st = fs.statSync(src);
  if (st.isDirectory()) {
    fs.mkdirSync(dst, { recursive: true });
    for (const name of fs.readdirSync(src)) copy(path.join(src, name), path.join(dst, name));
  } else {
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.copyFileSync(src, dst);
  }
}

for (const rel of copyTargets) {
  const src = path.join(root, rel);
  if (fs.existsSync(src)) {
    copy(src, path.join(out, rel));
  }
}

fs.copyFileSync(path.join(root, 'index.html'), path.join(out, '404.html'));
console.log(`Static build complete: ${out}`);
