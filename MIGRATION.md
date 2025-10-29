# Migration Guide: simon42-strategy → homebase42

## 📋 Übersicht

Deine bestehende `simon42-strategy` wird **Teil von homebase42**, ohne ihren Namen zu ändern. User installieren dann nur noch homebase42 und bekommen automatisch die Dashboard-Strategy mit dazu.

## 🔄 Dateien kopieren

### Schritt 1: Struktur vorbereiten

Deine aktuelle simon42-strategy Struktur:
```
simon42-strategy/
├── simon42-strategies-loader.js
├── core/
│   ├── simon42-dashboard-strategy.js
│   ├── simon42-dashboard-strategy-editor.js
│   └── editor/
├── utils/
├── views/
└── cards/
```

Ziel-Struktur in homebase42:
```
custom_components/homebase42/www/simon42-strategy/
├── simon42-strategies-loader.js
├── core/
│   ├── simon42-dashboard-strategy.js
│   ├── simon42-dashboard-strategy-editor.js
│   └── editor/
├── utils/
├── views/
└── cards/
```

### Schritt 2: Kopieren

```bash
# Navigiere zum homebase42 Repo
cd homebase42/custom_components/homebase42/www

# Lösche den Platzhalter
rm -rf simon42-strategy

# Kopiere deine simon42-strategy hierher
cp -r /pfad/zu/deiner/simon42-strategy ./simon42-strategy

# Prüfe die Struktur
ls -la simon42-strategy/
```

### Schritt 3: Keine Änderungen nötig!

✅ **Alle Dateinamen bleiben gleich**
✅ **Alle Imports bleiben gleich**
✅ **Alle Custom Element Namen bleiben gleich**
✅ **Strategy-Name bleibt `custom:simon42-dashboard`**

## 📝 Was ändert sich für User?

### Vorher (zwei separate Installationen):
```yaml
# 1. simon42-strategy manuell installieren
# 2. In configuration.yaml:
lovelace:
  resources:
    - url: /local/simon42-strategy/simon42-strategies-loader.js
      type: module

# 3. Dashboard erstellen mit:
strategy:
  type: custom:simon42-dashboard
```

### Nachher (eine HACS Installation):
```yaml
# 1. homebase42 über HACS installieren
# 2. Keine manuelle Resource-Registration mehr nötig!
# 3. Dashboard erstellen mit:
strategy:
  type: custom:simon42-dashboard
```

## 🎯 Vorteile der Integration

1. **Eine Installation statt zwei** - User müssen nur homebase42 über HACS installieren
2. **Automatische Resource-Registration** - Keine YAML-Änderungen mehr nötig
3. **Gemeinsame Updates** - Backend und Frontend werden zusammen aktualisiert
4. **Bessere Discoverability** - User finden alles an einem Ort

## 🔍 URL-Zugriff nach Integration

Die simon42-strategy wird verfügbar unter:
```
/hacsfiles/homebase42/simon42-strategy/simon42-strategies-loader.js
```

Statt wie bisher:
```
/local/simon42-strategy/simon42-strategies-loader.js
```

**Aber:** Home Assistant findet die Strategy automatisch über den Custom Element Namen `custom:simon42-dashboard` - User müssen die URL nie selbst angeben!

## ✅ Checkliste vor Release

- [ ] simon42-strategy Dateien kopiert
- [ ] Alle Dateien im `www/simon42-strategy/` Verzeichnis
- [ ] Test-Installation in lokalem Home Assistant
- [ ] Dashboard mit `custom:simon42-dashboard` erstellen
- [ ] Grafischer Editor funktioniert
- [ ] Alle Views werden korrekt generiert
- [ ] Browser-Console zeigt keine Fehler
- [ ] README.md enthält simon42-strategy Dokumentation

## 🚀 Deployment

Nach dem Kopieren der Dateien:

```bash
# Git Repository aktualisieren
git add custom_components/homebase42/www/simon42-strategy/
git commit -m "feat: integrate simon42-strategy into homebase42"
git push

# Tag für Release erstellen
git tag -a v0.1.0 -m "Initial release with integrated simon42-strategy"
git push origin v0.1.0
```

## 📚 Dokumentation aktualisieren

Stelle sicher, dass die README.md erwähnt:
- ✅ simon42-strategy ist integriert
- ✅ Keine separate Installation mehr nötig
- ✅ Strategy-Name bleibt `custom:simon42-dashboard`
- ✅ Alle bestehenden Features sind verfügbar
- ✅ Screenshots/GIFs des Dashboards

## 🤝 Backwards Compatibility

User mit bestehender simon42-strategy können:
1. homebase42 installieren
2. Die alte simon42-strategy Resource-Zeile aus configuration.yaml löschen
3. Die alten simon42-strategy Dateien aus `/www/` löschen
4. Dashboard funktioniert weiter ohne Änderungen!
