#!/usr/bin/env python3
"""Holt die aktuellen Take-Marker-Seiten aus dem Vault und baut daraus eine Website.

Quelle bleibt der Vault (~/vault/school/projektunterricht). Dieses Skript kopiert nur.
usage: bin/build.py            -> baut nach docs/
Danach lokal: docs/index.html in Chrome öffnen. GitHub Pages zeigt den Ordner docs/ auf main.
"""
import re
import shutil
from pathlib import Path

PU = Path.home() / "vault/school/projektunterricht"
ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "docs"

KOPF = """<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
"""

# Was öffentlich nicht drinstehen soll
ERSETZEN = [
    ("Mit Aleks: Trägerplatine ja oder nein.", "Im Team: Trägerplatine ja oder nein."),
    ('href="https://claude.ai/artifact/J827aKtzqpNK1zDi6KdJV1" target="_blank" rel="noopener"', 'href="../platine/"'),
]

ZURUECK = """
<a href="../" class="tm-back" style="position:fixed;left:max(12px,env(safe-area-inset-left,0px));bottom:max(12px,env(safe-area-inset-bottom,0px));z-index:9999;
font:600 12px/1 'B612','Avenir Next',system-ui,sans-serif;letter-spacing:.02em;text-decoration:none;color:#EDF2E7;background:#13302A;
padding:8px 11px;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,.25)">← Take-Marker</a>
"""


def oeffentlich(html):
    for a, b in ERSETZEN:
        html = html.replace(a, b)
    return html


def artifact_seite(quelle, ziel):
    """Artifact-Dateien haben keinen eigenen Kopf: Kopf und Body ergänzen."""
    html = quelle.read_text()
    html = re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>\n', "", html)
    html = html.replace("<style>\n/* Konzept", "</head><body>\n<style>\n/* Konzept", 1)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(oeffentlich(KOPF + html + ZURUECK + "\n</body></html>\n"))


def ganze_seite(quelle, ziel):
    html = quelle.read_text().replace("</body>", ZURUECK + "</body>", 1)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(oeffentlich(html))


def main():
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()
    artifact_seite(PU / "aufbau-take-marker.html", SITE / "aufbau/index.html")
    artifact_seite(PU / "platine-take-marker.html", SITE / "platine/index.html")
    shutil.copytree(PU / "platine/bilder", SITE / "platine/bilder")
    dl = SITE / "platine/dateien"
    dl.mkdir()
    shutil.copy(PU / "platine/take-marker-gerber.zip", dl)
    shutil.copy(PU / "platine/kicad/take-marker.kicad_pcb", dl)
    shutil.copy(PU / "platine/kicad/take-marker.kicad_pro", dl)
    ganze_seite(PU / "code/testsuite/testsuite.html", SITE / "testsuite/index.html")
    ganze_seite(PU / "code/auswertung/auswertung.html", SITE / "auswertung/index.html")
    shutil.copy(ROOT / "start.html", SITE / "index.html")
    shutil.copy(PU / "platine/bilder/render-iso.png", SITE / "vorschau.png")
    (SITE / ".nojekyll").write_text("")
    for p in sorted(SITE.rglob("*")):
        if p.is_file():
            print(f"{p.relative_to(SITE)}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
