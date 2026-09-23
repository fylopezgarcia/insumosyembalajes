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
- `tools/make_category_scenes.py` genera `cat-cintas`, `cat-zunchado`, `cat-stretch` y `cat-carton`: productos reales recortados, con ligera inclinación y luz cálida de borde, sobre fondo verde pino oscuro con viñeta — mismo ambiente que la foto de Herramientas, pero con nuestras fotos.
- `cat-papeleria.jpg` ya NO usa ese generador: es una imagen generada por IA de un escritorio de oficina, con el logo real de Insumos Hernández reproducido en varios artículos (vasos portalápices, caja de papel, marcador, libreta). También se usa como banner dentro de `categorias/papeleria.html`.
- `cat-carton.jpg` sigue usando imágenes de referencia (corrugado, burbuja, yumbolón), ya recortadas y compuestas igual que las demás. Reemplazar los recortes cuando haya foto propia.
- `banner-*.jpg` (3:1, para el encabezado de cada página de categoría) siguen con el estilo de rejilla anterior — pendiente aplicarles el mismo tratamiento si se quiere consistencia total.
- `cat-herramientas.jpg` es una imagen generada por IA (a partir de un prompt propio, sin logos ni texto de marca — se verificó que no reproduce ningún logo real). El negocio confirmó que sí distribuye SATA, pero esta imagen NO es una foto real de su inventario ni de la marca SATA; es una recreación genérica mientras no haya foto propia. `tools/make_herramientas.py` (ilustración con PIL) queda como alternativa/respaldo si se necesita.
- `bodega-nosotros.jpg` (Nosotros) confirmado: la anterior era generada con IA. Se reemplazó por `tools/make_nosotros.py`, un mosaico de 3 fotogramas reales de los videos propios (manos aplicando cinta a una caja, papel burbuja envolviendo un mueble, cartón en movimiento).


## Nueva categoría: Etiquetas y consumibles (separada de Papelería)
- `cat-etiquetas.jpg`: banner real generado, con logo propio, texto "Etiquetas y material para recibos" y sellos de confianza — igual tratamiento que `papeleria-banner.png`.
- Productos movidos de Papelería a esta categoría en la Tienda: Etiquetas térmicas personalizadas, Etiqueta en nailon, Rollo continuo.
- `tools/make_category_scenes.py` ya NO genera `cat-papeleria.jpg` ni `cat-etiquetas.jpg` — quedan protegidos como fotos/banners reales.

## Papelería: productos confirmados con el negocio
Resmas de papel, lápices, lapiceros, cuadernos — agregados a la Tienda y a la tabla de la categoría (antes solo decía "Escritorio" genérico).


## Cartón, Cintas, Zunchado, Stretch: de vuelta al collage original
Por pedido del negocio, `cat-carton.jpg`, `cat-cintas.jpg`, `cat-zunchado.jpg` y `cat-stretch.jpg`
volvieron al estilo de rejilla de 3 fotos con bordes redondeados (el primero que hicimos, con
`tools/make_covers.py`), en vez del fondo verde pino dramático. Papelería, Etiquetas y
Herramientas conservan sus fotos/banners reales — no se tocaron.

## Orden de categorías
"Etiquetas y consumibles" va ANTES que "Papelería" en todo el sitio (menú, inicio, Tienda,
sitemap, llms.txt y los cruces "también te puede interesar" de las demás categorías).


## Carrito compartido entre categorías (assets/js/cart.js)
Las tablas de especificación de Zunchado, Cintas, Cartón y Etiquetas ahora tienen
un selector de cantidad (+/-) igual al de la Tienda, en vez de un botón "Cotizar"
fijo. Se guarda en localStorage (`ih_cart_v1`) y persiste al navegar entre
categorías. Una barra flotante permite enviarlo por WhatsApp desde cualquier
página; en la Tienda se oculta sola porque ya existe su propia barra (con
campos de empresa/ciudad) — y esos mismos productos llegan prellenados ahí.
`order-builder.js` ya no maneja los clics +/- directamente (los delega en
cart.js) y vacía el carrito compartido al enviar desde la Tienda.

Corregido de paso: "Cinta transparente" (categoría) no coincidía con
"Cinta transparente 48mm" (Tienda) — ahora usan el mismo nombre exacto,
necesario para que el carrito los reconozca como el mismo producto.


## Logo principal (header) restaurado a la versión completa
`logo-header.png` volvió a ser el logo completo (aro dorado con el texto
"SERVICIOS E INSUMOS HERNÁNDEZ S.A.S." + fábrica), generado en alta
resolución desde `brand/logo-master.png`, en vez de la marca simplificada
de solo la fábrica que se había hecho para que fuera legible en 32px.
La marca simplificada queda guardada como `logo-header-mark-simple.png`
por si se necesita después. Favicon y el ícono mono del pie de página
siguen con la marca simplificada — a esos tamaños tan pequeños, el logo
completo no se lee bien.
