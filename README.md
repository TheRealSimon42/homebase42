# Homebase42 🏠🚀

**Deine zentrale Anlaufstelle für einen besseren Start in Home Assistant**

Homebase42 ist eine umfassende Custom Integration für Home Assistant, die besonders Anfängern den Einstieg erleichtert und gleichzeitig fortgeschrittenen Nutzern mächtige Werkzeuge an die Hand gibt.

## ✨ Features

### 🎨 Intelligentes Dashboard (simon42-strategy)
- **Automatische Dashboard-Generierung** - Erstellt automatisch ein übersichtliches Dashboard basierend auf deinen Bereichen und Geräten
- **Grafischer Konfigurator** - Keine YAML-Kenntnisse erforderlich
- **Modulare Views** - Lichter, Rollos, Sicherheit, Batterien und mehr
- **Echtzeit-Updates** - Alle Änderungen werden sofort sichtbar
- **Die bewährte simon42-strategy** ist vollständig integriert und wird mit homebase42 ausgeliefert

### 🔍 Intelligente Überwachung
- **Nicht verfügbare Entitäten** - Automatische Erkennung und Benachrichtigung
- **Batterie-Monitoring** - Warnungen bei kritischem und niedrigem Batteriestand
- **Performance-Tracking** - Überwache die Gesundheit deines Systems
- **Energie-Sensor-Überwachung** - Warnungen wenn Sensoren keine Daten mehr liefern

### 🤖 Vorkonfigurierte Automationen
- **Batterie-Warnungen** - Automatische Benachrichtigungen bei kritischen Batterieständen
- **Unavailable-Alerts** - Werde informiert wenn wichtige Entitäten ausfallen
- **Energie-Tracking** - Überwache deine Energie-Sensoren
- **Blueprints** - Einfach anpassbare Automationen für deine Bedürfnisse

### 📊 Sensoren & Binary Sensors
- `binary_sensor.homebase42_unavailable_entities` - Zeigt an ob es nicht verfügbare Entitäten gibt
- `binary_sensor.homebase42_battery_critical` - Warnung bei kritischen Batterien
- `sensor.homebase42_unavailable_count` - Anzahl nicht verfügbarer Entitäten
- `sensor.homebase42_battery_low_count` - Anzahl Batterien mit niedrigem Stand

## 📦 Installation

### HACS (empfohlen)

1. Öffne HACS in deinem Home Assistant
2. Gehe zu **Integrationen**
3. Klicke auf das Menü (⋮) oben rechts
4. Wähle **Benutzerdefinierte Repositories**
5. Füge die URL hinzu: `https://github.com/TheRealSimon42/homebase42`
6. Kategorie: **Integration**
7. Klicke auf **Hinzufügen**
8. Suche nach "Homebase42" und installiere es
9. Starte Home Assistant neu

### Manuelle Installation

1. Kopiere den `custom_components/homebase42` Ordner in dein `config/custom_components/` Verzeichnis
2. Starte Home Assistant neu

## ⚙️ Einrichtung

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Klicke auf **Integration hinzufügen**
3. Suche nach "Homebase42"
4. Folge dem Konfigurationsassistenten

### Konfigurationsoptionen

- **Admin-Features aktivieren** - Zeigt zusätzliche Admin-Views im Dashboard
- **Kritischer Batteriestand** - Schwellwert für kritische Batterie-Warnungen (Standard: 20%)
- **Niedriger Batteriestand** - Schwellwert für niedrige Batterie-Warnungen (Standard: 50%)
- **Verzögerung für Benachrichtigungen** - Wie lange eine Entität unavailable sein muss (Standard: 3 Stunden)

## 🎯 Dashboard-Strategy

Nach der Installation ist die bewährte **simon42-strategy** automatisch verfügbar:

### Neues Dashboard erstellen

1. Gehe zu **Einstellungen** → **Dashboards**
2. Klicke auf **Dashboard hinzufügen**
3. Wähle **Strategie**
4. Wähle **simon42-dashboard** (wird automatisch erkannt)
5. Fertig! Dein Dashboard wird automatisch generiert

**Wichtig:** Die Dashboard-Strategy heißt weiterhin `custom:simon42-dashboard` und behält alle bisherigen Funktionen. Sie wird jetzt einfach als Teil von homebase42 ausgeliefert, sodass keine separate Installation mehr nötig ist!

### Features der Dashboard-Strategy

- **Automatische Raum-Erkennung** - Nutzt deine Home Assistant Areas
- **Intelligente Gruppierung** - Entities nach Typ und Status gruppiert
- **Batch-Aktionen** - Steuere mehrere Geräte gleichzeitig
- **Optionale Integrationen** - Unterstützt Search Card, Alarm Panels, Reolink Kameras
- **Performance-optimiert** - Minimale Last auf deinem System
- **Grafischer Editor** - Drag & Drop Konfiguration ohne YAML

## 📚 Dokumentation

### Verwendung der Sensoren in Automationen

```yaml
automation:
  - alias: "Warnung bei nicht verfügbaren Entitäten"
    trigger:
      - platform: state
        entity_id: binary_sensor.homebase42_unavailable_entities
        to: "on"
        for: "00:10:00"
    action:
      - service: notify.mobile_app
        data:
          title: "Homebase42 Warnung"
          message: "{{ state_attr('binary_sensor.homebase42_unavailable_entities', 'count') }} Entitäten sind nicht verfügbar!"
```

### Dashboard-Konfiguration

Die Dashboard-Strategy kann über den grafischen Editor konfiguriert werden:

1. Öffne dein Homebase42-Dashboard
2. Klicke auf **Bearbeiten**
3. Klicke auf das ⚙️ Symbol oben rechts
4. Passe Bereiche, Sortierung und Filter an

## 🤝 Beitragen

Beiträge sind willkommen! Bitte:

1. Forke das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/AmazingFeature`)
3. Committe deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Changelog

Siehe [CHANGELOG.md](CHANGELOG.md) für Details zu Änderungen zwischen Versionen.

## 📄 Lizenz

**Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**

### Du darfst:
- ✅ **Teilen** - Das Material kopieren und weiterverbreiten
- ✅ **Bearbeiten** - Das Material remixen, verändern und darauf aufbauen

### Unter folgenden Bedingungen:
- 📝 **Namensnennung** - Angemessene Urheber-Nennung
- 🚫 **Nicht kommerziell** - Keine kommerzielle Nutzung
- 🔄 **Weitergabe unter gleichen Bedingungen** - Bei Veränderungen unter gleicher Lizenz

### 💼 Kommerzielle Nutzung

Interessiert an kommerzieller Nutzung? Kontaktiere mich für individuelle Lizenzvereinbarungen:

**👉 [Kontaktformular](https://www.simon42.com/contact/)**

**Siehe LICENSE-Datei für vollständige Details**

## 🙏 Danksagungen

- Home Assistant Community für Inspiration und Feedback
- Alle Contributors und Tester
- Besonderer Dank an die Home Assistant Core-Entwickler

## 💬 Support

- **Probleme?** Öffne ein [Issue](https://github.com/TheRealSimon42/homebase42/issues)
- **Fragen?** Diskutiere im [Home Assistant Community Forum](https://community.home-assistant.io/)
- **Updates?** Folge dem Repository für die neuesten Änderungen

---

**Entwickelt mit ❤️ für die Home Assistant Community**
