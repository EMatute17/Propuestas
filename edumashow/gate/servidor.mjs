// Servidor estatico minimo para probar sitios generados, parecido a un hosting real:
// compresion brotli/gzip para texto, tipos MIME correctos y cabeceras de cache por ruta.
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import zlib from 'node:zlib';

const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8', '.txt': 'text/plain; charset=utf-8', '.svg': 'image/svg+xml',
  '.avif': 'image/avif', '.webp': 'image/webp', '.jpg': 'image/jpeg', '.png': 'image/png', '.woff2': 'font/woff2',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.ico': 'image/x-icon',
};
const COMPRIMIBLE = new Set(['.html', '.css', '.js', '.json', '.txt', '.svg']);

export function servir(carpeta, { puerto = 0, comprimir = true, registro = null } = {}) {
  const raiz = path.resolve(carpeta);
  const cache = new Map();
  const srv = http.createServer((req, res) => {
    const limpia = decodeURIComponent((req.url || '/').split('?')[0]);
    let rel = path.normalize(limpia).replace(/^(\.\.[/\\])+/, '');
    if (rel.endsWith(path.sep) || rel === '.' || rel === '') rel = path.join(rel, 'index.html');
    const ruta = path.join(raiz, rel);
    if (!ruta.startsWith(raiz)) { res.writeHead(403); res.end(); return; }
    fs.readFile(ruta, (err, data) => {
      if (err) { res.writeHead(404, { 'content-type': 'text/plain' }); res.end('no encontrado'); if (registro) registro.push({ url: req.url, estado: 404 }); return; }
      const ext = path.extname(ruta).toLowerCase();
      const cab = { 'content-type': MIME[ext] || 'application/octet-stream', 'x-content-type-options': 'nosniff' };
      if (rel.split(path.sep).includes('assets')) cab['cache-control'] = 'public, max-age=31536000, immutable';
      else cab['cache-control'] = 'public, max-age=0, must-revalidate';
      let cuerpo = data;
      const ae = String(req.headers['accept-encoding'] || '');
      if (comprimir && COMPRIMIBLE.has(ext)) {
        const clave = ruta + (ae.includes('br') ? '#br' : ae.includes('gzip') ? '#gz' : '');
        if (ae.includes('br') || ae.includes('gzip')) {
          if (!cache.has(clave)) cache.set(clave, ae.includes('br') ? zlib.brotliCompressSync(data, { params: { [zlib.constants.BROTLI_PARAM_QUALITY]: 9 } }) : zlib.gzipSync(data, { level: 9 }));
          cuerpo = cache.get(clave); cab['content-encoding'] = ae.includes('br') ? 'br' : 'gzip'; cab['vary'] = 'Accept-Encoding';
        }
      }
      cab['content-length'] = cuerpo.length;
      res.writeHead(200, cab); res.end(cuerpo);
      if (registro) registro.push({ url: req.url, estado: 200, bytes: cuerpo.length, tipo: ext });
    });
  });
  return new Promise((ok) => {
    srv.listen(puerto, '127.0.0.1', () => {
      const p = srv.address().port;
      ok({ url: `http://127.0.0.1:${p}/`, puerto: p, cerrar: () => new Promise((r) => srv.close(r)) });
    });
  });
}

// uso directo: node servidor.mjs <carpeta> [puerto]
if (import.meta.url === `file://${process.argv[1]}`) {
  const s = await servir(process.argv[2] || '.', { puerto: Number(process.argv[3] || 8080) });
  console.log('Sirviendo en', s.url);
}
