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
import hashlib
import json
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

    inject_product_schema()
    bust_cache()
    print(f"\nListo. Sube el CONTENIDO de {DIST} (no la carpeta en sí) a la raíz del hosting.")


ROW_RE = re.compile(
    r'<tr>\s*'
    r'<td>(?:<img class="spec-thumb" src="([^"]+)"[^>]*>)?'
    r'<span class="spec-name-col"><b>([^<]+)</b></span></td>\s*'
    r'<td>([^<]*)</td>\s*'
    r'<td>([^<]*)</td>\s*'
    r'<td>.*?</td>\s*'
    r'</tr>',
    re.S,
)
BREADCRUMB_RE = re.compile(r'<nav class="breadcrumb">.*</a>\s*/\s*([^<]+?)\s*</nav>')
CANONICAL_RE = re.compile(r'<link rel="canonical" href="([^"]+)"')
SITE = "https://insumosyembalajes.com.co"
BRAND = {"@type": "Organization", "name": "Servicios e Insumos Hernández S.A.S."}


def inject_product_schema():
    """
    Marca cada producto de las tablas de categoría como schema.org/Product
    (dentro de un ItemList), para que buscadores y asistentes de IA puedan
    leer nombre, foto, descripción y categoría de cada uno directamente
    desde el HTML — sin precio ni "offers", porque el negocio cotiza por
    WhatsApp y no maneja precio fijo publicado (agregarlo sin uno real
    violaría las guías de datos estructurados de Google).
    """
    n_pages = 0
    n_products = 0
    for f in sorted((DIST / "categorias").glob("*.html")):
        html = f.read_text(encoding="utf-8")
        rows = ROW_RE.findall(html)
        if not rows:
            continue
        crumb = BREADCRUMB_RE.search(html)
        canon = CANONICAL_RE.search(html)
        category = crumb.group(1).strip() if crumb else None
        page_url = canon.group(1) if canon else None

        items = []
        for i, (img, name, presentacion, uso) in enumerate(rows, start=1):
            product = {
                "@type": "Product",
                "name": name.strip(),
                "description": (uso.strip() or presentacion.strip()),
                "brand": BRAND,
            }
            if category:
                product["category"] = category
            if img:
                product["image"] = SITE + img
            if page_url:
                product["url"] = page_url
            items.append({"@type": "ListItem", "position": i, "item": product})
            n_products += 1

        data = {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": category or f.stem,
            "itemListElement": items,
        }
        script = '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + '\n</script>\n'
        html = html.replace("</head>", script + "</head>", 1)
        f.write_text(html, encoding="utf-8")
        n_pages += 1
    print(f"product schema: {n_products} productos en {n_pages} páginas de categoría")


def bust_cache():
    """
    Hostinger sirve CSS/JS con cache-control de 7 días (ver .htaccess): sin
    esto, cada corrección tarda hasta una semana en verse en los celulares
    que ya visitaron el sitio (Safari, y sobre todo el navegador interno de
    WhatsApp, que cachea aparte y es más difícil de refrescar a mano).

    Le agrega "?v=<hash del contenido>" a cada CSS/JS en el HTML ya generado,
    así el navegador solo vuelve a descargar el archivo cuando su contenido
    realmente cambió — el resto del tiempo sigue aprovechando la caché.
    """
    versions = {}
    for f in list((DIST / "assets/css").glob("*.css")) + list((DIST / "assets/js").glob("*.js")):
        rel = "/" + f.relative_to(DIST).as_posix()
        versions[rel] = hashlib.md5(f.read_bytes()).hexdigest()[:8]

    pattern = re.compile(r'((?:href|src)=")(/assets/(?:css|js)/[^"?]+\.(?:css|js))(")')

    def repl(m):
        path = m.group(2)
        v = versions.get(path)
        return f'{m.group(1)}{path}{"?v=" + v if v else ""}{m.group(3)}'

    for f in DIST.glob("**/*.html"):
        f.write_text(pattern.sub(repl, f.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"cache-busting: {len(versions)} archivos CSS/JS versionados")


if __name__ == "__main__":
    main()
