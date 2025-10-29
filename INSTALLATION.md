# Homebase42 - Installationsanleitung

## 📦 Installation über HACS

### Voraussetzungen
- Home Assistant 2024.1.0 oder höher
- HACS installiert und konfiguriert

### Schritte

1. **Repository hinzufügen**
   - Öffne HACS
   - Gehe zu **Integrationen**
   - Klicke auf das Menü (⋮) oben rechts
   - Wähle **Benutzerdefinierte Repositories**
   - URL: `https://github.com/DEIN-USERNAME/homebase42`
   - Kategorie: **Integration**
   - Klicke auf **Hinzufügen**

2. **Integration installieren**
   - Suche nach "Homebase42"
   - Klicke auf **Herunterladen**
   - Warte bis der Download abgeschlossen ist

3. **Home Assistant neu starten**
   - Gehe zu **Einstellungen** → **System**
   - Klicke auf **Neu starten**

4. **Integration einrichten**
   - Gehe zu **Einstellungen** → **Geräte & Dienste**
   - Klicke auf **Integration hinzufügen**
   - Suche nach "Homebase42"
   - Folge dem Konfigurationsassistenten

## 🔧 Manuelle Installation

### Schritte

1. **Dateien kopieren**
   ```bash
   cd /config
   # Erstelle custom_components falls nicht vorhanden
   mkdir -p custom_components
   
   # Kopiere homebase42 Verzeichnis
   cp -r /pfad/zu/homebase42/custom_components/homebase42 custom_components/
   ```

2. **Verzeichnisstruktur prüfen**
   ```
   /config/
   └── custom_components/
       └── homebase42/
           ├── __init__.py
           ├── manifest.json
           ├── config_flow.py
           ├── binary_sensor.py
           ├── sensor.py
           ├── const.py
           ├── strings.json
           └── www/
               └── simon42-strategy/
                   └── ... (alle JS-Dateien)
   ```

3. **Home Assistant neu starten**

4. **Integration einrichten** (siehe oben)

## ⚙️ Konfiguration

### Erste Einrichtung

Beim ersten Start werden folgende Optionen abgefragt:

| Option | Beschreibung | Standard |
|--------|--------------|----------|
| **Admin-Features aktivieren** | Zeigt Admin-Views im Dashboard | `Aus` |
| **Kritischer Batteriestand** | Schwellwert für kritische Warnungen | `20%` |
| **Niedriger Batteriestand** | Schwellwert für Warnungen | `50%` |
| **Verzögerung für Benachrichtigungen** | Wartezeit bevor unavailable gemeldet wird | `3 Stunden` |

### Optionen später ändern

1. Gehe zu **Einstellungen** → **Geräte & Dienste**
2. Finde **Homebase42** in der Liste
3. Klicke auf **Konfigurieren**
4. Passe die Einstellungen an

## 🎨 Dashboard erstellen

### Mit der simon42-strategy

1. **Dashboard hinzufügen**
   - Gehe zu **Einstellungen** → **Dashboards**
   - Klicke auf **Dashboard hinzufügen**
   - Wähle **Strategie**
   - Wähle **simon42-dashboard**

2. **Fertig!**
   - Das Dashboard wird automatisch generiert
   - Alle deine Bereiche werden erkannt
   - Entities werden intelligent gruppiert

### Manuelle Konfiguration (optional)

Falls du die Strategy manuell konfigurieren möchtest:

```yaml
strategy:
  type: custom:simon42-dashboard
  areas_display: visible  # oder 'hidden', oder liste von area_ids
  group_by_floors: false
  show_search_card: false
  areas_options:
    wohnzimmer:
      groups_options:
        lights:
          hidden:
            - light.wohnzimmer_stehlampe
```

## 🔍 Überprüfung

### Integration läuft?

Prüfe folgende Entities:

```
binary_sensor.homebase42_unavailable_entities
binary_sensor.homebase42_battery_critical
sensor.homebase42_unavailable_count
sensor.homebase42_battery_low_count
```

### Dashboard-Strategy geladen?

1. Öffne die Entwicklertools im Browser (F12)
2. Gehe zur Konsole
3. Suche nach: `Simon42 Dashboard Strategies loaded`

### Resources verfügbar?

URL sollte erreichbar sein:
```
http://DEINE-HA-URL:8123/hacsfiles/homebase42/simon42-strategy/simon42-strategies-loader.js
```

## 🐛 Troubleshooting

### Integration erscheint nicht

- **Lösung 1**: Home Assistant neu starten
- **Lösung 2**: Cache des Browsers löschen
- **Lösung 3**: Prüfe die Logs unter **Einstellungen** → **System** → **Protokolle**

### Dashboard-Strategy nicht verfügbar

- **Lösung 1**: Prüfe ob `/hacsfiles/homebase42/` erreichbar ist
- **Lösung 2**: Browser-Cache löschen (Strg+Shift+R)
- **Lösung 3**: Im Entwicklertools-Console nach Fehlern suchen

### Sensoren zeigen keine Daten

- **Lösung 1**: Warte 5 Minuten (Scan-Interval)
- **Lösung 2**: Gehe zu **Entwicklerwerkzeuge** → **Zustände** und prüfe die Entities
- **Lösung 3**: Starte Home Assistant neu

### Fehler in den Logs

Häufige Fehler und Lösungen:

```
FileNotFoundError: www/simon42-strategy
→ Stelle sicher, dass die simon42-strategy Dateien kopiert wurden
```

```
ImportError: cannot import name 'X'
→ Prüfe die manifest.json Version und HA-Kompatibilität
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/DEIN-USERNAME/homebase42/issues)
- **Forum**: [Home Assistant Community](https://community.home-assistant.io/)
- **Logs**: Aktiviere Debug-Logging in `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.homebase42: debug
```
