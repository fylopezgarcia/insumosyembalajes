#!/usr/bin/env python3
"""
Build script — "hornea" (inlines) partials/header.html y partials/footer.html
directamente en cada página HTML, generando una copia 100% estática en dist/.

Por qué existe: la mayoría de los rastreadores de IA (GPTBot, ClaudeBot,
PerplexityBot, CCBot) NO ejecutan JavaScript — solo leen el HTML tal cual llega
del servidor. Con <div data-include="header"></div> + fetch() en el navegador,
esos rastreadores ven el header y footer vacíos: sin menú, sin teléfono, sin
dirección, sin el schema.org del negocio. dist/ resuelve eso: cada página sale
con el header y footer ya escritos adentro, visibles para cualquier rastreador,
con o sin JavaScript.

Uso:
    python3 build.py

Sigue editando partials/header.html y partials/footer.html como fuente única;
corre este script antes de cada subida a producción. dist/ se regenera por
completo en cada corrida (no lo edites a mano).
"""
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"

PAGES = [
    "index.html", "tienda.html", "nosotros.html", "contacto.html",
    "preguntas-frecuentes.html", "404.html",
] + [f"categorias/{p.name}" for p in (ROOT / "categorias").glob("*.html")] \
  + [f"ciudades/{p.name}" for p in (ROOT / "ciudades").glob("*.html")] \
  + [f"guias/{p.name}" for p in (ROOT / "guias").glob("*.html")]

HEADER = (ROOT / "partials/header.html").read_text(encoding="utf-8")
FOOTER = (ROOT / "partials/footer.html").read_text(encoding="utf-8")

INCLUDE_RE = re.compile(r'<div data-include="(header|footer)"></div>')


def inline(html: str) -> str:
    def repl(m):
        return HEADER if m.group(1) == "header" else FOOTER
    html = INCLUDE_RE.sub(repl, html)
    # includes.js ya no hace falta una vez que el contenido está inlineado
    html = html.replace('<script src="/assets/js/includes.js"></script>\n', "")
    return html


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    for rel in PAGES:
        src = ROOT / rel
        out = DIST / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = src.read_text(encoding="utf-8")
        out.write_text(inline(html), encoding="utf-8")
        print("built:", rel)

    # Copiar assets y archivos raíz de SEO/IA tal cual
    shutil.copytree(ROOT / "assets", DIST / "assets")
    for extra in ("robots.txt", "sitemap.xml", "llms.txt", "manifest.webmanifest", ".htaccess"):
        p = ROOT / extra
        if p.exists():
            shutil.copy(p, DIST / extra)
            print("copied:", extra)

    print(f"\nListo. Sube el CONTENIDO de {DIST} (no la carpeta en sí) a la raíz del hosting.")


if __name__ == "__main__":
    main()
