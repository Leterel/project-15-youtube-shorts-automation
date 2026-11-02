# Projekt 17: YouTube Shorts Automation

## Ziel
Ein weitgehend automatisierter deutschsprachiger YouTube-Shorts-Kanal im Bereich Technik, Computer und KI-Fakten. Möglichst geringe laufende Kosten (Startbudget: 0 EUR), ohne eigene Kamera und ohne eigene Sprachaufnahme. Langfristiges Ziel: Einnahmen über YouTube, sofern die Monetarisierungsvoraussetzungen erfüllt werden.

## Status (31.10.2026)
- GitHub-Repository angelegt, privat.
- Windows und PowerShell 7.6.9 im Einsatz.
- FFmpeg 9.0.2 vorhanden und ausführbar.
- Python 3.12.10 vorhanden und ausführbar.
- Git und GitHub CLI vorhanden.
- Windows SAPI-Sprachausgabe funktioniert.
- Installierte Stimmen: Microsoft Hedda Desktop (Deutsch) und Microsoft Zira Desktop (Englisch/USA).
- Hedda wurde mit einem Testsatz abgespielt; klingt künstlich, ist für den ersten Prototyp aber akzeptabel.
- Noch kein Video erzeugt, kein automatischer Upload eingerichtet, keine Monetarisierung erreicht.

## Erstes Testvideo
Arbeitstitel: „Warum braucht KI eigentlich so viel Arbeitsspeicher?“
- Sprache: Deutsch
- Format: vertikal 9:16
- Ziellänge: ungefähr 30 Sekunden
- Elemente: eigener kurzer Erklärtext, synthetische Sprachausgabe, lesbare Texteinblendungen/Animationen
- Umsetzung zunächst lokal und überprüfbar, ohne automatisches Veröffentlichen

## Geplante technische Pipeline
1. Eigene Themenideen und kurze, faktisch geprüfte Skripte erstellen.
2. Skripte automatisch in Sprache umwandeln (zunächst Windows SAPI/Hedda).
3. Mit FFmpeg Video im Shorts-Format mit eigenen Grafiken, Text und Audio erzeugen.
4. Qualität, Fakten, Lesbarkeit und Rechte prüfen.
5. Erst nach Freigabe Veröffentlichung/Upload automatisieren.
6. Ergebnisse auswerten und Vorlagen iterativ verbessern.

## Grundsätze und Risiken
- Keine identischen Massen-Reuploads oder bloß minimale Abwandlungen fremder Videos.
- Originalität und eigener Informationswert sind wichtig; repetitive oder massenhaft produzierte Inhalte können von YouTube bei der Monetarisierung abgelehnt werden.
- Rechte an Bildern, Musik, Videomaterial und Stimmen beachten.
- Masse allein garantiert weder Reichweite noch Einnahmen.
- Kein kostenpflichtiger Dienst ohne vorherige Entscheidung.
- Bestehende Dateien, Repositories und andere Projekte nicht ungefragt verändern.
- Kleine, nachvollziehbare Schritte; vor weiteren Änderungen jeweils Ergebnisse prüfen.

## Offene Entscheidungen
- Lokales Arbeitsverzeichnis für die Videoerstellung festlegen.
- Für den Prototyp Hedda verwenden; später ggf. eine natürlichere kostenlose Stimme evaluieren.
- Konkretes erstes Skript und visuelle Gestaltung festlegen.
- Upload und Veröffentlichungsfreigabe erst später planen.

## Bisherige technische Tests
```text
ffmpeg version 9.0.2-full_build-www.gyan.dev
Python 3.12.10
PowerShell 7.6.9
SAPI-Stimmen:
  Microsoft Hedda Desktop - German
  Microsoft Zira Desktop - English (United States)
```

## Projektabgrenzung
Dieses Repository gehört ausschließlich zur YouTube-Shorts-Automatisierung. Es ist unabhängig von anderen GitHub-/GitLab-Projekten und weiteren lokalen Arbeitsverzeichnissen.

## Lokaler Videoprototyp — 02.11.2026

`build_video.py` erzeugt aus einem eigenen JSON-Skript deutsche SAPI-Sprache
und ein vertikales 720×1280-MP4 mit eigenen Textgrafiken. Keine Python-Pakete,
Downloads, Konten oder laufenden Kosten. Windows, Python 3.12+, FFmpeg/ffprobe,
Arial und eine installierte deutsche SAPI-Stimme werden vorab geprüft.

```powershell
python -m unittest -v
python build_video.py example.json --output build/erster-entwurf
```

Der Zielordner muss neu sein; vorhandene Dateien werden nicht überschrieben.
`verification.json` enthält Auflösung und tatsächliche Dauer. Szenendauern folgen
der Sprachausgabe. Der Entwurf ist sichtbar als solcher und mit synthetischer
Stimme gekennzeichnet. Vor einer Veröffentlichung Text, Ton, Lesbarkeit und
Quellen prüfen. Kein automatischer Upload und keine Monetarisierung eingerichtet.
Die Beispielaussagen zu Gewichten und Kontext sind technische Erklärungen ohne
konkrete Speicherbedarfszusage; unterschiedliche Modellarchitekturen unterscheiden
sich. Nächster Schritt: Hör-/Sichtprüfung und engeres Timing auf etwa 30 Sekunden.

Technische Primärquellen für das Beispiel (geprüft 02.11.2026):
[Hugging Face: KV-Cache](https://github.com/huggingface/transformers/blob/main/docs/source/en/cache_explanation.md)
und [Cache-Speicherstrategien](https://huggingface.co/docs/transformers/v4.50.0/kv_cache).
Das lokale SAPI-Hilfsskript läuft mit einer nur für den Unterprozess geltenden
ExecutionPolicy; Systemeinstellungen werden nicht geändert.

### Layoutkorrektur — 02.11.2026

Vor dem Anlegen des Zielordners werden Überschriften und Untertitel konservativ
nach Breite und Höhe umbrochen; bei Bedarf wird die Schrift bis zu einer
festgelegten Mindestgröße verkleinert. Nicht passende Texte werden abgewiesen.
Zeilenumbrüche werden ausdrücklich als LF geschrieben, damit FFmpeg unter
Windows keine zusätzlichen Leerzeilen rendert. Szenen behalten eigene Textdateien.
Die installierte Schrift wird direkt verwendet, weder kopiert noch gelöscht.
Das ersetzt keine Sichtprüfung bei ungewöhnlichen Zeichen oder neuen Inhalten.
Der eigene Quellcode steht unter MIT; siehe LICENSE.
