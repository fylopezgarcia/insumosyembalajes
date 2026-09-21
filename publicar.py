#!/usr/bin/env python3
"""
Prepara la publicación: reconstruye dist/ y lo sincroniza con la carpeta espejo
que usa FileZilla. Muestra qué archivos se agregan, cambian o eliminan.

    python3 publicar.py            # simulación (no toca nada en el espejo)
    python3 publicar.py --aplicar  # sincroniza el espejo y crea la etiqueta git
"""
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
ESPEJO = Path("/Users/fredy/Documents/filezilla/INSUMOSYEMBALAJES")


def run(cmd, **kw):
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)


def main():
    aplicar = "--aplicar" in sys.argv

    if not ESPEJO.is_dir():
        sys.exit(f"No existe la carpeta espejo: {ESPEJO}")

    sucio = run(["git", "status", "--porcelain"]).stdout.strip()
    if sucio and aplicar:
        sys.exit("Hay cambios sin guardar en git. Haz commit primero:\n" + sucio)

    b = run([sys.executable, "build.py"])
    if b.returncode:
        sys.exit("Falló build.py:\n" + b.stdout + b.stderr)

    flags = ["-rc", "--delete", "--itemize-changes", "--exclude=.DS_Store"]
    if not aplicar:
        flags.append("--dry-run")
    r = run(["rsync", *flags, f"{DIST}/", f"{ESPEJO}/"])
    if r.returncode:
        sys.exit("Falló rsync:\n" + r.stderr)

    nuevos, cambiados, borrados = [], [], []
    for line in r.stdout.splitlines():
        if line.endswith("/") or " " not in line:
            continue
        flag, name = line.split(None, 1)
        if flag.startswith("*deleting"):
            borrados.append(name)
        elif flag[0] in "<>c" and flag[2:].startswith("+++"):
            nuevos.append(name)
        elif flag[0] in "<>c":
            cambiados.append(name)

    for titulo, lista in (("NUEVOS", nuevos), ("CAMBIADOS", cambiados),
                          ("ELIMINADOS (bórralos también en el servidor)", borrados)):
        print(f"\n{titulo}: {len(lista)}")
        for n in lista:
            print("  ", n)

    if not (nuevos or cambiados or borrados):
        print("\nEl espejo ya está al día. No hay nada que subir.")
        return

    if not aplicar:
        print("\n(Simulación. Para aplicar: python3 publicar.py --aplicar)")
        return

    tag = f"deploy-{date.today().isoformat()}"
    n = 2
    while run(["git", "rev-parse", "-q", "--verify", f"refs/tags/{tag}"]).returncode == 0:
        tag = f"deploy-{date.today().isoformat()}-{n}"
        n += 1
    run(["git", "tag", tag])
    print(f"\nEspejo actualizado. Etiqueta git: {tag}")
    print("Ahora en FileZilla: Comparar directorios y sube lo resaltado.")


if __name__ == "__main__":
    main()
