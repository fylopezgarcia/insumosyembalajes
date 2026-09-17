# Cómo publicar cambios — Insumos Hernández

Este documento es la referencia fija: cada vez que edites el sitio y quieras subirlo a producción, sigue estos pasos en orden. No dependas de la memoria — sigue la lista.

## Por qué está armado así

- **`sitio-nuevo/` es la única fuente de verdad.** Editas `header.html`, `footer.html`, cualquier página o los estilos, siempre ahí — nunca directamente en el servidor ni en `dist/`.
- **`dist/` es generado, no se edita a mano.** Sale de correr `build.py`, que "hornea" el header y footer (hoy en un solo archivo cada uno) dentro de cada página, para que el sitio funcione igual de bien con JavaScript que sin él — clave para que los rastreadores de IA y buscadores vean el menú, el teléfono y el schema del negocio.
- **Git guarda la historia.** Cada cambio real queda como un commit con fecha y descripción — puedes ver qué cambió y cuándo, y si algo sale mal, hay a dónde volver.
- **Solo el CONTENIDO de `dist/` sube al hosting** — nunca subas `sitio-nuevo/` completo (eso subiría `build.py`, el `.git`, este mismo archivo, etc. — cosas que no necesita el servidor).

## Antes de la primera subida — respaldo obligatorio

Vas a reemplazar lo que hoy está en Hostinger (el sitio hecho con AI Builder). Antes de subir nada nuevo:

1. Abre FileZilla y conéctate a tu hosting.
2. Entra a la carpeta raíz del sitio (normalmente `public_html/` — si el dominio es un dominio adicional en un plan con varios sitios, puede ser `domains/insumosyembalajes.com.co/public_html/`).
3. Selecciona **todo** el contenido actual → clic derecho → **Descargar** → guárdalo en una carpeta local tipo `respaldo-sitio-viejo-2026-09/`. No lo borres del servidor todavía.
4. Solo cuando el sitio nuevo esté subido y verificado en vivo, borras lo viejo del servidor.

## Cada vez que publiques un cambio

1. **Edita** lo que necesites dentro de `sitio-nuevo/` (páginas, `partials/header.html`, `partials/footer.html`, `assets/css/`, etc.).
2. **Construye:**
   ```
   cd sitio-nuevo
   python3 build.py
   ```
   Revisa que termine sin errores y que diga "Listo. Sube el CONTENIDO de .../dist".
3. **Revisa localmente antes de subir** (opcional pero recomendado si el cambio es grande):
   ```
   python3 -m http.server 8080 --directory dist
   ```
   y ábrelo en el navegador en `http://localhost:8080`.
4. **Guarda el cambio en git** (esto es lo que te da la "historia"):
   ```
   git add -A
   git commit -m "Describe qué cambiaste, en español, corto y claro"
   ```
5. **Sube por FileZilla:**
   - Conéctate al hosting.
   - En el panel izquierdo (tu PC), entra a la carpeta `dist/`.
   - En el panel derecho (el servidor), entra a `public_html/` (o la que corresponda).
   - Selecciona todo el contenido de `dist/` → arrastra al panel derecho → confirma sobrescribir.
   - **Tip:** en FileZilla, menú **Servidor → Comparar directorios**, actívalo antes de arrastrar — así solo resalta y sube lo que realmente cambió, en vez de todo el sitio cada vez.
6. **Verifica en vivo:** abre insumosyembalajes.com.co en el navegador (en modo incógnito, para evitar caché) y revisa que el cambio se vea bien.

## Si algo sale mal después de subir

- **En el servidor:** vuelve a subir por FileZilla el respaldo que descargaste (o la versión anterior de `dist/` si guardaste una).
- **En el código:** `git log --oneline` para ver el historial, y `git checkout <hash-del-commit-anterior> -- .` para recuperar una versión anterior de los archivos antes de reconstruir y volver a subir.

## Guardar la historia fuera de esta máquina (recomendado, no urgente)

Hoy el historial de git vive solo en este computador. Si el disco falla o cambias de equipo, se pierde. La forma estándar de resolver esto es tener una copia en **GitHub** (gratis, puede ser un repositorio privado):

1. Crea una cuenta en [github.com](https://github.com) si no tienes una.
2. Crea un repositorio nuevo, privado, vacío (sin README).
3. Avísame cuando lo tengas creado y te doy los 2 comandos exactos para conectar este repo local y subir todo el historial de una vez.

Esto no cambia nada de cómo publicas (sigues usando FileZilla) — es solo un respaldo adicional de la historia del código. Una vez esté en GitHub, hay una mejora futura opcional: Hostinger tiene una función de "Git" en su panel que puede jalar automáticamente los cambios desde GitHub sin necesidad de FileZilla — algo para evaluar más adelante, no ahora.
