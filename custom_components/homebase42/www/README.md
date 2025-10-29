# Dashboard Strategy Verzeichnis

Dieses Verzeichnis enthält alle Frontend-Ressourcen für die Homebase42 Dashboard-Strategy.

## 📁 Struktur

Die bewährte **simon42-strategy** wird hier eingebunden und mit homebase42 ausgeliefert:

```
www/
└── simon42-strategy/
    ├── simon42-strategies-loader.js  # Entry Point
    │
    ├── core/
    │   ├── simon42-dashboard-strategy.js
    │   ├── simon42-dashboard-strategy-editor.js
    │   └── editor/
    │       ├── simon42-editor-handlers.js
    │       ├── simon42-editor-styles.js
    │       └── simon42-editor-template.js
    │
    ├── utils/
    │   ├── simon42-helpers.js
    │   ├── simon42-data-collectors.js
    │   ├── simon42-badge-builder.js
    │   ├── simon42-section-builder.js
    │   └── simon42-view-builder.js
    │
    ├── views/
    │   ├── simon42-view-room.js
    │   ├── simon42-view-lights.js
    │   ├── simon42-view-covers.js
    │   ├── simon42-view-security.js
    │   ├── simon42-view-batteries.js
    │   └── simon42-view-admin.js
    │
    └── cards/
        └── simon42-summary-card.js
```

## 🎯 URL-Zugriff

Nach Installation sind die Dateien verfügbar unter:
- `/hacsfiles/homebase42/simon42-strategy/simon42-strategies-loader.js`

Die Integration registriert die Ressourcen automatisch!

## 📝 Hinweise

- **Keine manuelle Resource-Registration nötig** - Die Integration macht das automatisch
- **Strategy-Name bleibt**: `custom:simon42-dashboard` (keine Änderung für bestehende User)
- **Automatischer Reload** - Änderungen werden nach Browser-Refresh sichtbar
- **Dev-Mode**: Für Entwicklung kannst du die Dateien direkt bearbeiten

## 🔄 Für Entwickler

Die simon42-strategy behält ihren etablierten Namen und Custom-Element-Namen. Homebase42 fungiert als HACS-Distribution, die:

1. **Backend-Features** bereitstellt (Sensoren, Binary Sensors, Config Flow)
2. **Frontend-Strategy** automatisch registriert
3. **Eine einzige Installation** ermöglicht (statt zwei separate Repos)
