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
