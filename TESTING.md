# Tests und Reproduzierbarkeit — YouTube Shorts Automation

## Voraussetzungen
Renderprototyp: Python 3.12+, Windows SAPI, FFmpeg/ffprobe, Arial. Ursprüngliche Pipeline: andere, noch nicht reproduzierbar verifizierte lokale Abhängigkeiten.

## Befehle
```text
python -m unittest -v
```

Start/Build: python build_video.py example.json --output <NEUER_ORDNER>. Originalpipeline nicht ungeprüft starten: auch Vorschau liest YouTube und kann lokale Dateien schreiben.

## Tatsächlicher Befund vom 02.11.2026
4 Tests bestanden; neuer kompletter SAPI/FFmpeg-Smokebuild mit AAC, Dauer, Auflösung, Prüfsummen und VTT bestand; Bild angesehen, Audiopegel geprüft. Keine Transkription, Ollama-Generierung oder Uploads ausgeführt.

Bei fehlenden Paketen/Hardware/Betriebssystemen ist das Ergebnis „nicht ausgeführt“, kein Pass. Plattformnachweise aus älteren Detailberichten gelten nur für die dort genannten Versionen. Android-Automatisierung ausschließlich mit expliziter emulator-Seriennummer und bestätigtem ro.kernel.qemu=1. Physische Geräte, persönliche Medien und Produktionskonten sind keine Testfixtures.

## Vor Merge
`git diff --check` ausführen; relevante Funktionstests wiederholen, wenn Codeänderungen ihren Befund entwerten. Speicherdaten/alte Versionen erhalten. Fehlende externe Abnahmen in HANDOFF.md benennen.
