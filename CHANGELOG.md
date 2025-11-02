# Changelog

Alle wichtigen Änderungen an diesem Projekt werden in dieser Datei dokumentiert.

Das Format basiert auf [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
und dieses Projekt folgt [Semantic Versioning](https://semver.org/lang/de/).

## [Unreleased]

### Hinzugefügt
- **LLM State Export** - Automatischer State-Export für AI/LLM Integration
  - **Automatischer Export**: Alle 60 Minuten + 5 Minuten nach Neustart
  - Service `homebase42.export_states` für manuellen Export
  - Exportiert alle Entity-States als JSON für LLM-Kontext
  - Automatische Areazuordnung über Entity- und Device-Registry
  - Flexible Konfiguration (Attribute, Kontext, etc.)
  - Optimiertes Format für AI/LLM Integration
  - Event-Trigger nach erfolgreichem Export
  - Deutsche und englische Übersetzungen
  - Umfangreiche Dokumentation mit Beispielen

### Geplant
- Energy sensor monitoring mit Benachrichtigungen
- Performance metrics sensor
- Erweiterte Admin-Views im Dashboard
- Weitere Automation Blueprints

## [0.1.0] - 2025-10-29

### Hinzugefügt
- Initiales Release von Homebase42
- Config Flow für UI-basierte Einrichtung
- Binary Sensor für nicht verfügbare Entitäten
- Binary Sensor für kritische Batteriestände
- Count Sensor für nicht verfügbare Entitäten
- Count Sensor für niedrige Batteriestände
- Grundlegende Konfigurationsoptionen:
  - Admin-Features Toggle
  - Batterie-Schwellwerte
  - Unavailable-Benachrichtigungsverzögerung
- Deutsche Übersetzungen (strings.json)
- HACS-Unterstützung
- Grundlegende Dokumentation

### Bekannte Einschränkungen
- Dashboard-Strategy Integration noch nicht implementiert
- Blueprints noch nicht verfügbar
- Englische Übersetzungen fehlen noch

[Unreleased]: https://github.com/TheRealSimon42/homebase42/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/TheRealSimon42/homebase42/releases/tag/v0.1.0
