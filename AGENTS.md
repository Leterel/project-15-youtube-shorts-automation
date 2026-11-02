# Agentenleitfaden — YouTube Shorts Automation

## Einstieg
Öffentliches Repo enthält einen lokalen SAPI/FFmpeg-Renderprototyp. Die vorhandene eigentliche Whisper/Ollama/Upload-Pipeline liegt separat lokal und wurde nur gelesen.

Lies README.md, TESTING.md und HANDOFF.md. Anforderungen und vorhandene Funktionen unterscheiden. Technische Grundlagen: README.md. Die bestehenden Detaildokumente bleiben maßgeblich; keine leeren SPEC-/ARCHITECTURE-/TODO-Kopien erzeugen. Offene Arbeit und Verlauf: README.md; konkrete Einnahmegrenzen: MONETIZATION.md, soweit vorhanden.

## Umgebung und Start
Renderprototyp: Python 3.12+, Windows SAPI, FFmpeg/ffprobe, Arial. Ursprüngliche Pipeline: andere, noch nicht reproduzierbar verifizierte lokale Abhängigkeiten.

python build_video.py example.json --output <NEUER_ORDNER>. Originalpipeline nicht ungeprüft starten: auch Vorschau liest YouTube und kann lokale Dateien schreiben.

Tests: `python -m unittest -v`. Bei mehreren Befehlen einzeln ausführen und jeden Exitcode prüfen. Vorhandene Installationen verwenden; fehlende Voraussetzungen melden statt automatisch globale Pakete oder Modelle zu installieren.

## Grenzen
- Größere Änderungen auf einem eigenen Branch; zuerst git status und fremde Änderungen prüfen. Keine parallelen widersprüchlichen Arbeiten am selben Branch.
- Keine Dateien/Repos löschen oder verschieben, keine Historien umschreiben, kein Force-Push. Keine Lizenzänderungen ohne konkrete Freigabe.
- Keine Secrets, privaten Daten, echten Nutzerinhalte oder großen generierten Dateien committen. Keine Sichtbarkeitsänderungen oder zusätzlichen Veröffentlichungen ohne Freigabe.
- Keine bezahlten Dienste, Werbenetzwerke, Zahlungsanbieter oder externe Nachrichten aktivieren.
- Keine Originalvideos, OAuth-Konfiguration, Tokens oder privaten Metadaten committen. --upload und API-/Produktivänderungen benötigen konkrete Freigabe.
- Projektwerkzeuge ändern keine anderen Projektquellen. Build-/Testartefakte in isolierten, ignorierten Arbeitsordnern halten. Vorhandene Ausgaben nicht unbesehen überschreiben.

## Nächste sichere Etappe
Bestehende private Pipeline isoliert testen: Hash-gebundener Transkriptcache, Planungsfallback und Fortschritt/ETA. Vor Übernahme in öffentliches Repo gesondert prüfen/freigeben.

## Übergabe
HANDOFF.md aktualisieren: Ausgangscommit/Branch, konkrete Änderungsliste, ausgeführte Befehle, Ergebnis, ausgelassene Tests samt Grund, Risiken und nächste Etappe. Nur tatsächlich ausgeführte Tests als bestanden ausweisen. Vor Merge Diff und Tests prüfen; externe Freigaben bleiben offen.
