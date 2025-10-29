// ====================================================================
// VIEW STRATEGY - BATTERIEN (Batterie-Übersicht) - OPTIMIERT
// ====================================================================
// KEIN unnötiges Map-Caching mehr - nutzt direkt hass.entities[entityId]
// Liest Batterie-Schwellwerte aus der Homebase42-Integration
// ====================================================================

import { getExcludedLabels } from '../utils/simon42-helpers.js';

class Simon42ViewBatteriesStrategy {
  static async generate(config, hass) {
    const { entities } = config;
    
    const excludeLabels = getExcludedLabels(entities);
    const excludeSet = new Set(excludeLabels);
    
    // Hole hidden entities aus areas_options (wenn config übergeben wurde)
    // Batterien könnten in verschiedenen Gruppen sein, daher alle durchsuchen
    const hiddenFromConfig = new Set();
    if (config.config?.areas_options) {
      for (const areaOptions of Object.values(config.config.areas_options)) {
        if (areaOptions.groups_options) {
          // Durchsuche alle Gruppen nach versteckten Entities
          for (const groupOptions of Object.values(areaOptions.groups_options)) {
            if (groupOptions.hidden) {
              groupOptions.hidden.forEach(id => hiddenFromConfig.add(id));
            }
          }
        }
      }
    }

    // Lese Batterie-Schwellwerte aus der Homebase42-Integration
    let criticalThreshold = 20; // Default
    let lowThreshold = 50; // Default
    
    // Suche nach der Homebase42 Config Entry
    const homebase42Entries = Object.values(hass.config_entries || {})
      .filter(entry => entry.domain === 'homebase42');
    
    if (homebase42Entries.length > 0) {
      const homebase42Entry = homebase42Entries[0];
      const options = homebase42Entry.options || {};
      
      // Lese die konfigurierten Schwellwerte
      criticalThreshold = options.battery_critical_threshold || 20;
      lowThreshold = options.battery_low_threshold || 50;
    }

    // OPTIMIERT: Filter-Reihenfolge - KEIN Map-Caching mehr!
    const batteryEntities = Object.keys(hass.states)
      .filter(entityId => {
        const state = hass.states[entityId];
        if (!state) return false;
        
        // 1. Battery-Check zuerst (String-includes ist schnell)
        const isBattery = entityId.includes('battery') || 
                         state.attributes?.device_class === 'battery';
        if (!isBattery) return false;
        
        // 2. Registry-Check - DIREKT aus hass.entities (O(1) Lookup)
        const registryEntry = hass.entities?.[entityId];
        if (registryEntry?.hidden === true) return false;
        
        // 3. Exclude-Checks (Set-Lookup = O(1))
        if (excludeSet.has(entityId)) return false;
        if (hiddenFromConfig.has(entityId)) return false;
        
        // 4. Value-Check am Ende
        const value = parseFloat(state.state);
        return !isNaN(value); // Nur numerische Werte
      });

    // Gruppiere nach Batteriestatus mit dynamischen Schwellwerten
    const critical = []; // < criticalThreshold
    const low = []; // criticalThreshold - lowThreshold
    const good = []; // > lowThreshold
    
    batteryEntities.forEach(entityId => {
      const state = hass.states[entityId];
      const value = parseFloat(state.state);
      
      if (value <= criticalThreshold) {
        critical.push(entityId);
      } else if (value <= lowThreshold) {
        low.push(entityId);
      } else {
        good.push(entityId);
      }
    });

    const sections = [];

    // Kritische Batterien
    if (critical.length > 0) {
      sections.push({
        type: "grid",
        cards: [
          {
            type: "heading",
            heading: `🔴 Kritisch (≤ ${criticalThreshold}%) - ${critical.length} ${critical.length === 1 ? 'Batterie' : 'Batterien'}`,
            heading_style: "title"
          },
          ...critical.map(entity => ({
            type: "tile",
            entity: entity,
            vertical: false,
            state_content: ["state", "last_changed"],
            color: "red"
          }))
        ]
      });
    }

    // Niedrige Batterien
    if (low.length > 0) {
      sections.push({
        type: "grid",
        cards: [
          {
            type: "heading",
            heading: `🟡 Niedrig (${criticalThreshold + 1}-${lowThreshold}%) - ${low.length} ${low.length === 1 ? 'Batterie' : 'Batterien'}`,
            heading_style: "title"
          },
          ...low.map(entity => ({
            type: "tile",
            entity: entity,
            vertical: false,
            state_content: ["state", "last_changed"],
            color: "yellow"
          }))
        ]
      });
    }

    // Gute Batterien
    if (good.length > 0) {
      sections.push({
        type: "grid",
        cards: [
          {
            type: "heading",
            heading: `🟢 Gut (> ${lowThreshold}%) - ${good.length} ${good.length === 1 ? 'Batterie' : 'Batterien'}`,
            heading_style: "title"
          },
          ...good.map(entity => ({
            type: "tile",
            entity: entity,
            vertical: false,
            state_content: ["state", "last_changed"],
            color: "green"
          }))
        ]
      });
    }

    return {
      type: "sections",
      sections: sections
    };
  }
}

// Registriere Custom Element
customElements.define("ll-strategy-simon42-view-batteries", Simon42ViewBatteriesStrategy);
