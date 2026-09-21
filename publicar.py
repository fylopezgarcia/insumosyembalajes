#!/usr/bin/env python3
"""
Prepara la publicación con dos carpetas dentro de la carpeta de FileZilla:

  espejo/  = copia exacta de lo que HAY en Hostinger (solo cambia con --subido)
  subir/   = solo los archivos nuevos o cambiados desde el último --subido,
             más BORRAR.txt con lo que hay que eliminar en el servidor

    python3 publicar.py            # reconstruye dist/ y regenera subir/
    python3 publicar.py --subido   # ya subí todo: actualiza espejo/, vacía subir/, etiqueta git
"""
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
BASE = Path("/Users/fredy/Documents/filezilla/INSUMOSYEMBALAJES")
ESPEJO = BASE / "espejo"
SUBIR = BASE / "subir"
RSYNC = ["rsync", "-rc", "--delete", "--itemize-changes", "--exclude=.DS_Store"]


def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)


def clasificar(salida):
    nuevos, cambiados, borrados = [], [], []
    for line in salida.splitlines():
        if line.endswith("/") or " " not in line:
            continue
        flag, name = line.split(None, 1)
        if flag.startswith("*deleting"):
            borrados.append(name)
        elif flag[0] in "<>c" and flag[2:].startswith("+++"):
            nuevos.append(name)
        elif flag[0] in "<>c":
            cambiados.append(name)
    return nuevos, cambiados, borrados


def construir():
    b = run([sys.executable, "build.py"])
    if b.returncode:
        sys.exit("Falló build.py:\n" + b.stdout + b.stderr)


def marcar_subido():
    sucio = run(["git", "status", "--porcelain"]).stdout.strip()
    if sucio:
        sys.exit("Hay cambios sin guardar en git. Haz commit primero:\n" + sucio)
    construir()
    ESPEJO.mkdir(parents=True, exist_ok=True)
    r = run([*RSYNC, f"{DIST}/", f"{ESPEJO}/"])
    if r.returncode:
        sys.exit("Falló rsync:\n" + r.stderr)
    if SUBIR.exists():
        shutil.rmtree(SUBIR)
    SUBIR.mkdir()

    tag = f"deploy-{date.today().isoformat()}"
    n = 2
    while run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"]).returncode == 0:
        tag = f"deploy-{date.today().isoformat()}-{n}"
        n += 1
    run(["git", "tag", tag])
    run(["git", "push", "-q", "origin", tag])
    print(f"espejo/ actualizado, subir/ vacío. Etiqueta git: {tag}")


def preparar_subida():
    construir()
    ESPEJO.mkdir(parents=True, exist_ok=True)
    r = run([*RSYNC, "--dry-run", f"{DIST}/", f"{ESPEJO}/"])
    if r.returncode:
        sys.exit("Falló rsync:\n" + r.stderr)
    nuevos, cambiados, borrados = clasificar(r.stdout)

    if SUBIR.exists():
        shutil.rmtree(SUBIR)
    SUBIR.mkdir()
    for rel in nuevos + cambiados:
        dst = SUBIR / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(DIST / rel, dst)
    if borrados:
        (SUBIR / "BORRAR.txt").write_text(
            "Elimina estos archivos del servidor (public_html):\n\n" + "\n".join(borrados) + "\n",
            encoding="utf-8")

    for titulo, lista in (("NUEVOS", nuevos), ("CAMBIADOS", cambiados),
                          ("A BORRAR EN EL SERVIDOR", borrados)):
        print(f"\n{titulo}: {len(lista)}")
        for n in lista:
            print("  ", n)

    if not (nuevos or cambiados or borrados):
        print("\nNo hay nada pendiente por subir.")
        return
    print(f"\nSube el contenido de:\n  {SUBIR}\na la raíz del hosting."
          "\nCuando termines: python3 publicar.py --subido")


def main():
    if "--subido" in sys.argv:
        marcar_subido()
    else:
        preparar_subida()


if __name__ == "__main__":
    main()
