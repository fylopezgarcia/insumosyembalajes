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
- `hero-inicio.jpg`, `cat-*.jpg` (4:3) y `banner-*.jpg` (3:1) son composiciones de las fotos reales de arriba. Para regenerarlas: `python3 tools/make_covers.py`.
- `cat-carton.jpg` usa imágenes de referencia (corrugado, burbuja, yumbolón) y `cat-herramientas.jpg` es una imagen generada con IA. Reemplazar cuando haya foto propia.
- `bodega-nosotros.jpg` (página Nosotros) no es verificable como foto de la bodega real: revisar.
