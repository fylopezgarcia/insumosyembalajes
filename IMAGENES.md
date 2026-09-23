# Imágenes de producto — origen y pendientes

Carpeta: `assets/img/productos/` (JPG, 720–800 px, cuadradas).

## Fotos reales de estudio propias (`01 INSUMOS/CONTENIDO ORIGINAL INSUMOS/`)
Cintas (transparente 100 micras, de colores, pesada, aluminio, ducto, enmascarar, antideslizante, cera x300), etiquetas (rollo, nailon, rollo continuo), grapas plásticas, Pantera (Multitack e incoloro), stretch (12.5, 12.5 negro, 15, 30, 45) y vinipel.

## Fotogramas de los videos propios
`zuncho`, `zuncho-en-caja`, `cintas-y-zuncho`, `burbuja-en-accion`.

## Imágenes de referencia (reemplazar por foto propia)
`carton-corrugado`, `plastico-burbuja`, `espuma-polietileno`.

## Sin foto (recuadro neutro en la Tienda)
Grapa metálica, Papel kraft. Papelería y Herramientas (categorías) tampoco tienen foto real.

## Por confirmar con el negocio
- Los nombres de los productos nuevos de la Tienda salen de los nombres de archivo de las fotos (p. ej. "Stretch 12.5 cm", "Cinta de colores"). Confirmar nombre, medida y unidad de venta.
- Stretch: la Tienda ya tenía "40 cm"; ahora hay también 12.5, 15, 30 y 45. Verificar si 40 y 45 son el mismo producto.
- Zuncho: solo plástico por ahora (el metálico no se publica). Grapas: plásticas y metálicas.

## Portadas (generadas con `tools/make_covers.py`)
- `hero-inicio.jpg` se genera con `tools/make_hero.py` a partir de productos recortados (`tools/cutouts/`, hechos con `tools/cutout.swift` sobre las fotos reales).
- Rediseñadas como una sola escena de estudio (sin rejilla de tarjetas): `tools/make_category_scenes.py` genera `cat-cintas`, `cat-zunchado`, `cat-stretch`, `cat-papeleria` y `cat-carton` a partir de recortes reales en `tools/cutouts/`.
- `cat-carton.jpg` sigue usando imágenes de referencia (corrugado, burbuja, yumbolón), ya recortadas y compuestas igual que las demás. Reemplazar los recortes cuando haya foto propia.
- `banner-*.jpg` (3:1, para el encabezado de cada página de categoría) siguen con el estilo de rejilla anterior — pendiente aplicarles el mismo tratamiento si se quiere consistencia total.
- `cat-herramientas.jpg` sigue siendo una imagen generada con IA: no hay foto real de herramientas todavía.
- `bodega-nosotros.jpg` (Nosotros) confirmado: la anterior era generada con IA. Se reemplazó por `tools/make_nosotros.py`, un mosaico de 3 fotogramas reales de los videos propios (manos aplicando cinta a una caja, papel burbuja envolviendo un mueble, cartón en movimiento).
