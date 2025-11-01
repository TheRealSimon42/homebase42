# Homebase42 Templates

Dieser Ordner enthält Template-Sensoren, die von der Homebase42 Integration bereitgestellt werden.

## Wie funktioniert es?

Wenn du optionale Templates in der Homebase42 Integration aktivierst, werden diese automatisch in den `config/packages/homebase42/` Ordner deiner Home Assistant Installation kopiert.

## Voraussetzung: Packages aktivieren

Damit die Templates funktionieren, musst du **Packages in deiner Home Assistant Configuration aktivieren**:

1. Öffne deine `configuration.yaml`
2. Füge folgende Zeilen hinzu (falls nicht bereits vorhanden):

```yaml
homeassistant:
  packages: !include_dir_named packages
```

3. Erstelle den Ordner `config/packages/` falls er nicht existiert
4. Starte Home Assistant neu

## Verfügbare Templates

### Wetter-Vorhersagen (`s42_weather_forecasts.yaml`)

Erstellt Template-Sensoren für Wettervorhersagen:

**Tägliche Vorhersagen:**
- `sensor.wetter_vorhersage_taglich` - Vollständige tägliche Vorhersage
- `sensor.wetter_vorhersage_des_heutigen_tages` - Vorhersage für heute
- `sensor.wetter_vorhersage_des_nachsten_tages` - Vorhersage für morgen

**Stündliche Vorhersagen:**
- `sensor.wetter_vorhersage_stundlich` - Vollständige stündliche Vorhersage
- `sensor.wetter_vorhersage_der_nachsten_stunde` - Vorhersage für die nächste Stunde
- `sensor.regen_menge_der_jetzigen_stunde` - Aktuelle Regenmenge

**Zusätzlich:**
- `sensor.hochsttemperatur_des_tages_uhrzeit` - Zeitpunkt der Höchsttemperatur

Die Wetter-Entität kann in den Einstellungen der Integration konfiguriert werden (Standard: `weather.forecast_home`).

## Deinstallation

Wenn du ein Template deaktivierst, wird die entsprechende Datei automatisch aus dem `packages/homebase42/` Ordner entfernt. Der Ordner selbst bleibt jedoch bestehen, falls andere Templates aktiv sind.
