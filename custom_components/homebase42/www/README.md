# Dashboard Strategy Verzeichnis

Dieses Verzeichnis enthält alle Frontend-Ressourcen für die Homebase42 Dashboard-Strategy.

## 📁 Struktur

```
www/
└── homebase42-strategy/
    ├── homebase42-strategies-loader.js  # Entry Point
    │
    ├── core/
    │   ├── homebase42-dashboard-strategy.js
    │   ├── homebase42-dashboard-strategy-editor.js
    │   └── editor/
    │       ├── homebase42-editor-handlers.js
    │       ├── homebase42-editor-styles.js
    │       └── homebase42-editor-template.js
    │
    ├── utils/
    │   ├── homebase42-helpers.js
    │   ├── homebase42-data-collectors.js
    │   ├── homebase42-badge-builder.js
    │   ├── homebase42-section-builder.js
    │   └── homebase42-view-builder.js
    │
    ├── views/
    │   ├── homebase42-view-room.js
    │   ├── homebase42-view-lights.js
    │   ├── homebase42-view-covers.js
    │   ├── homebase42-view-security.js
    │   ├── homebase42-view-batteries.js
    │   └── homebase42-view-admin.js        # NEU: Admin-View
    │
    └── cards/
        └── homebase42-summary-card.js
```

## 🔄 Migration von simon42-strategy

Wenn du deine bestehenden `simon42-strategy` Dateien hierher kopierst:

1. **Umbenennen**: `simon42` → `homebase42` in allen Dateinamen
2. **Namespace anpassen**: Alle Importe und Custom Element Namen anpassen
3. **Admin-View hinzufügen**: Neue View für Admin-Features erstellen

## 🎯 URL-Zugriff

Nach Installation sind die Dateien verfügbar unter:
- `/hacsfiles/homebase42/homebase42-strategy/homebase42-strategies-loader.js`

Die Integration registriert die Ressourcen automatisch!

## 📝 Hinweise

- **Keine manuelle Resource-Registration nötig** - Die Integration macht das automatisch
- **Automatischer Reload** - Änderungen werden nach Browser-Refresh sichtbar
- **Dev-Mode**: Für Entwicklung kannst du die Dateien direkt bearbeiten
