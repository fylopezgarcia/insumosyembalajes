# Sitio nuevo — Insumos Hernández

Sitio estático (HTML + CSS + JS puro, sin frameworks ni paso de build) que reemplaza al de Hostinger AI Builder.
Se puede subir tal cual a cualquier hosting estático (Hostinger con plan de hosting normal, Netlify, Cloudflare Pages, etc.) — no necesita Node, PHP ni base de datos.

## Estructura

```
sitio-nuevo/
├── index.html                  Home
├── tienda.html                 Catálogo + selector de pedido (arma el pedido y lo manda a WhatsApp)
├── nosotros.html                Quiénes somos, reseñas de Google, cómo funciona
├── contacto.html                 Dirección, mapa, WhatsApp, horario
├── preguntas-frecuentes.html
├── categorias/                  Una página por categoría de producto (SEO + contenido real)
│   ├── carton-y-proteccion.html
│   ├── cintas-y-adhesivos.html
│   ├── zunchado.html
│   ├── plastico-stretch.html
│   ├── papeleria.html
│   └── bricolage.html
├── ciudades/                    Landing por ciudad del Eje Cafetero
│   ├── pereira.html
│   ├── dosquebradas.html
│   ├── manizales.html
│   └── armenia.html
├── partials/                    Header y footer únicos, se inyectan por JS en cada página
│   ├── header.html
│   └── footer.html
└── assets/
    ├── css/  tokens.css (paleta y tipografía) · base.css (reset y layout) · components.css (nav, botones, tarjetas, etc.)
    ├── js/   includes.js (inyecta header/footer) · main.js (menú móvil, WhatsApp) · order-builder.js (selector de pedido)
    └── img/  logo y fotos — aquí van tus fotos reales cuando las tengas listas
```

## Cómo verlo mientras se construye

Necesita servirse por HTTP (no abrir el archivo directamente por doble clic), porque el header y el footer se cargan con `fetch()`. Con Node instalado:

```
npx serve .
```

o con Python:

```
python3 -m http.server 8080
```

## Estado de avance

Ver `PROGRESO.md`.
