// Capturas rapidas de un sitio en varios tamanos, para revision visual.
// uso: node capturas.mjs <carpeta_sitio> <carpeta_salida> [ancho x alto [dpr [completa]]]...
import { chromium } from 'playwright';
import path from 'node:path';
import fs from 'node:fs';
import { servir } from './servidor.mjs';

const [carpeta, salida, ...pedidos] = process.argv.slice(2);
fs.mkdirSync(salida, { recursive: true });
const tamanos = (pedidos.length ? pedidos : ['390x844:2', '1440x900:1']).map((p) => {
  const [dim, resto] = p.split(':');
  const [w, h] = dim.split('x').map(Number);
  const [dpr, completa] = (resto || '1').split(',');
  return { w, h, dpr: Number(dpr), completa: completa === 'completa' };
});

const srv = await servir(carpeta);
const nav = await chromium.launch({ args: ['--no-sandbox'] });
for (const t of tamanos) {
  const movil = t.w < 900;
  const ctx = await nav.newContext({ viewport: { width: t.w, height: t.h }, deviceScaleFactor: t.dpr, isMobile: movil, hasTouch: movil });
  const pag = await ctx.newPage();
  const errores = [];
  pag.on('console', (m) => { if (m.type() === 'error') errores.push(m.text()); });
  pag.on('pageerror', (e) => errores.push('pageerror: ' + e.message));
  await pag.goto(srv.url, { waitUntil: 'load' });
  await pag.waitForTimeout(2600);
  const nombre = `${t.w}x${t.h}`;
  await pag.screenshot({ path: path.join(salida, `${nombre}_arriba.png`) });
  if (t.completa) {
    // recorre la pagina para activar los reveals y hace una captura completa
    const alto = await pag.evaluate(() => document.documentElement.scrollHeight);
    for (let y = 0; y < alto; y += Math.round(t.h * 0.8)) { await pag.evaluate((yy) => window.scrollTo(0, yy), y); await pag.waitForTimeout(260); }
    await pag.evaluate(() => window.scrollTo(0, 0)); await pag.waitForTimeout(500);
    await pag.screenshot({ path: path.join(salida, `${nombre}_completa.png`), fullPage: true });
  }
  console.log(nombre, JSON.stringify({ errores }));
  await ctx.close();
}
await nav.close(); await srv.cerrar();
