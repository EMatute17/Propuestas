// Rendimiento con Lighthouse (movil lento simulado y escritorio), mediana de varias pasadas,
// sobre un servidor que comprime como un hosting real.
// uso: node rendimiento.mjs <carpeta_sitio> <salida.json> [pasadas]
import fs from 'node:fs';
import lighthouse from 'lighthouse';
import desktopConfig from 'lighthouse/core/config/desktop-config.js';
import * as chromeLauncher from 'chrome-launcher';
import { servir } from './servidor.mjs';

const [carpeta, salida, pasadasArg] = process.argv.slice(2);
const PASADAS = Number(pasadasArg || 3);
const srv = await servir(carpeta, { comprimir: true });
const chrome = await chromeLauncher.launch({
  chromePath: process.env.CHROME_PATH || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  chromeFlags: ['--headless=new', '--no-sandbox', '--disable-gpu'],
});
const mediana = (a) => { const s = [...a].sort((x, y) => x - y); return s[Math.floor(s.length / 2)]; };
const CATS = ['performance', 'accessibility', 'best-practices', 'seo'];
const out = { pasadas: PASADAS, servidor: 'local con brotli, sin CDN', perfiles: {} };

for (const [nombre, config] of [['movil', undefined], ['escritorio', desktopConfig]]) {
  const runs = [];
  for (let i = 0; i < PASADAS; i++) {
    const r = await lighthouse(srv.url, { port: chrome.port, output: 'json', logLevel: 'error', onlyCategories: CATS }, config);
    runs.push(r.lhr);
  }
  const num = (id) => mediana(runs.map((l) => l.audits[id]?.numericValue ?? 0));
  const ultimo = runs[runs.length - 1];
  out.perfiles[nombre] = {
    puntuaciones: Object.fromEntries(CATS.map((c) => [c, mediana(runs.map((l) => Math.round(l.categories[c].score * 100)))])),
    fcp_ms: Math.round(num('first-contentful-paint')), lcp_ms: Math.round(num('largest-contentful-paint')),
    cls: Number(num('cumulative-layout-shift').toFixed(3)), tbt_ms: Math.round(num('total-blocking-time')),
    speed_index_ms: Math.round(num('speed-index')), peso_KB: Math.round(num('total-byte-weight') / 1024),
    fallos: Object.values(ultimo.audits).filter((a) => a.score !== null && a.score < 0.9 && !['notApplicable', 'informative', 'manual'].includes(a.scoreDisplayMode)).map((a) => `${a.id} (${Math.round(a.score * 100)})`),
  };
  console.log(nombre, JSON.stringify(out.perfiles[nombre].puntuaciones), 'LCP', out.perfiles[nombre].lcp_ms, 'ms');
}
fs.writeFileSync(salida, JSON.stringify(out, null, 1));
await chrome.kill(); await srv.cerrar();
