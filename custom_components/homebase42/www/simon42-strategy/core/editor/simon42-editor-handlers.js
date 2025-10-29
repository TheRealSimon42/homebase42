// ====================================================================
// SIMON42 EDITOR HANDLERS
// ====================================================================
// Event-Handler für den Dashboard Strategy Editor

import { renderAreaEntitiesHTML } from './simon42-editor-template.js';

export function attachEnergyCheckboxListener(element, callback) {
  const energyCheckbox = element.querySelector('#show-energy');
  if (energyCheckbox) {
    energyCheckbox.addEventListener('change', (e) => {
      callback(e.target.checked);
    });
  }
}

export function attachSearchCardCheckboxListener(element, callback) {
  const searchCardCheckbox = element.querySelector('#show-search-card');
  if (searchCardCheckbox) {
    searchCardCheckbox.addEventListener('change', (e) => {
      callback(e.target.checked);
    });
  }
}

export function attachSubviewsCheckboxListener(element, callback) {
  const subviewsCheckbox = element.querySelector('#show-subviews');
  if (subviewsCheckbox) {
    subviewsCheckbox.addEventListener('change', (e) => {
      callback(e.target.checked);
    });
  }
}

export function attachAdminFeaturesCheckboxListener(element, callback) {
  const adminFeaturesCheckbox = element.querySelector('#show-admin-features');
  if (adminFeaturesCheckbox) {
    adminFeaturesCheckbox.addEventListener('change', (e) => {
      callback(e.target.checked);
    });
  }
}

export function attachGroupByFloorsCheckboxListener(element, callback) {
  const groupByFloorsCheckbox = element.querySelector('#group-by-floors');
  if (groupByFloorsCheckbox) {
    groupByFloorsCheckbox.addEventListener('change', (e) => {
      callback(e.target.checked);
    });
  }
}

export function attachAreaCheckboxListeners(element, callback) {
  const areaCheckboxes = element.querySelectorAll('.area-checkbox');
  areaCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      const areaId = e.target.dataset.areaId;
      const isVisible = e.target.checked;
      callback(areaId, isVisible);
      
      // Disable/Enable expand button
      const areaItem = e.target.closest('.area-item');
      const expandButton = areaItem.querySelector('.expand-button');
      if (expandButton) {
        expandButton.disabled = !isVisible;
      }
    });
  });
}

export function attachExpandButtonListeners(element, hass, config, onEntitiesLoad) {
  const expandButtons = element.querySelectorAll('.expand-button');
  
  expandButtons.forEach(button => {
    button.addEventListener('click', async (e) => {
      e.stopPropagation();
      
      const areaId = button.dataset.areaId;
      const areaContent = element.querySelector(`.area-content[data-area-id="${areaId}"]`);
      const expandIcon = button.querySelector('.expand-icon');
      
      if (!areaContent) return;
      
      const isExpanded = areaContent.style.display !== 'none';
      
      if (isExpanded) {
        // Collapse
        areaContent.style.display = 'none';
        expandIcon.style.transform = 'rotate(0deg)';
      } else {
        // Expand
        areaContent.style.display = 'block';
        expandIcon.style.transform = 'rotate(90deg)';
        
        // Lade Entitäten wenn noch nicht geladen
        if (areaContent.querySelector('.loading-placeholder')) {
          try {
            // Import data collectors
            const { getAllEntitiesForArea, groupEntitiesByDomain } = await import('../data/simon42-data-collectors.js');
            
            // Sammle Entities für diesen Bereich
            const areaEntities = getAllEntitiesForArea(areaId, hass);
            const groupedEntities = groupEntitiesByDomain(areaEntities, hass);
            
            // Hole hidden entities aus config
            const areaConfig = config.areas_options?.[areaId] || {};
            const groupsOptions = areaConfig.groups_options || {};
            
            const hiddenEntities = {};
            Object.keys(groupsOptions).forEach(group => {
              hiddenEntities[group] = groupsOptions[group].hidden || [];
            });
            
            const entityOrders = {};
            Object.keys(groupsOptions).forEach(group => {
              entityOrders[group] = groupsOptions[group].order || [];
            });
            
            // Render Entities
            areaContent.innerHTML = renderAreaEntitiesHTML(
              areaId,
              groupedEntities,
              hiddenEntities,
              entityOrders,
              hass
            );
            
            // Attach listeners für Group Checkboxen
            attachGroupCheckboxListeners(element, onEntitiesLoad);
            
            // Attach listeners für Entity Checkboxen
            attachEntityCheckboxListeners(element, onEntitiesLoad);
            
            // Attach listeners für Entity Expand Buttons
            attachEntityExpandButtonListeners(element, element);
            
          } catch (error) {
            console.error('Error loading entities for area:', error);
            areaContent.innerHTML = '<div class="error-state">Fehler beim Laden der Entitäten</div>';
          }
        }
      }
    });
  });
}

export function attachGroupCheckboxListeners(element, callback) {
  const groupCheckboxes = element.querySelectorAll('.group-checkbox');
  
  groupCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      const areaId = e.target.dataset.areaId;
      const group = e.target.dataset.group;
      const isVisible = e.target.checked;
      
      // null für entityId bedeutet: alle Entities in der Gruppe
      callback(areaId, group, null, isVisible);
      
      // Update alle Entity-Checkboxen in dieser Gruppe
      const entityList = element.querySelector(`.entity-list[data-area-id="${areaId}"][data-group="${group}"]`);
      if (entityList) {
        const entityCheckboxes = entityList.querySelectorAll('.entity-checkbox');
        entityCheckboxes.forEach(cb => {
          cb.checked = isVisible;
        });
      }
      
      // Entferne indeterminate state
      e.target.indeterminate = false;
      e.target.removeAttribute('data-indeterminate');
    });
  });
}

export function attachEntityCheckboxListeners(element, callback) {
  const entityCheckboxes = element.querySelectorAll('.entity-checkbox');
  
  entityCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      const areaId = e.target.dataset.areaId;
      const group = e.target.dataset.group;
      const entityId = e.target.dataset.entityId;
      const isVisible = e.target.checked;
      
      callback(areaId, group, entityId, isVisible);
      
      // Update Group-Checkbox state (all/some/none checked)
      const entityList = element.querySelector(`.entity-list[data-area-id="${areaId}"][data-group="${group}"]`);
      const groupCheckbox = element.querySelector(`.group-checkbox[data-area-id="${areaId}"][data-group="${group}"]`);
      
      if (entityList && groupCheckbox) {
        const allCheckboxes = Array.from(entityList.querySelectorAll('.entity-checkbox'));
        const checkedCount = allCheckboxes.filter(cb => cb.checked).length;
        
        if (checkedCount === 0) {
          groupCheckbox.checked = false;
          groupCheckbox.indeterminate = false;
          groupCheckbox.removeAttribute('data-indeterminate');
        } else if (checkedCount === allCheckboxes.length) {
          groupCheckbox.checked = true;
          groupCheckbox.indeterminate = false;
          groupCheckbox.removeAttribute('data-indeterminate');
        } else {
          groupCheckbox.checked = false;
          groupCheckbox.indeterminate = true;
          groupCheckbox.setAttribute('data-indeterminate', 'true');
        }
      }
    });
  });
}

export function attachEntityExpandButtonListeners(element, editorElement) {
  const expandButtons = element.querySelectorAll('.expand-button-small');
  
  expandButtons.forEach(button => {
    button.addEventListener('click', (e) => {
      e.stopPropagation();
      
      const areaId = button.dataset.areaId;
      const group = button.dataset.group;
      const entityList = element.querySelector(`.entity-list[data-area-id="${areaId}"][data-group="${group}"]`);
      const expandIcon = button.querySelector('.expand-icon-small');
      
      if (!entityList) return;
      
      const isExpanded = entityList.style.display !== 'none';
      
      if (isExpanded) {
        // Collapse
        entityList.style.display = 'none';
        expandIcon.style.transform = 'rotate(0deg)';
      } else {
        // Expand
        entityList.style.display = 'block';
        expandIcon.style.transform = 'rotate(90deg)';
      }
    });
  });
}

export function attachDragAndDropListeners(element, onOrderChange) {
  const areaList = element.querySelector('#area-list');
  if (!areaList) return;

  let draggedItem = null;

  areaList.addEventListener('dragstart', (e) => {
    if (e.target.classList.contains('drag-handle')) {
      draggedItem = e.target.closest('.area-item');
      draggedItem.style.opacity = '0.5';
      e.dataTransfer.effectAllowed = 'move';
    }
  });

  areaList.addEventListener('dragend', (e) => {
    if (draggedItem) {
      draggedItem.style.opacity = '1';
      draggedItem = null;
    }
  });

  areaList.addEventListener('dragover', (e) => {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    const afterElement = getDragAfterElement(areaList, e.clientY);
    if (afterElement == null) {
      areaList.appendChild(draggedItem);
    } else {
      areaList.insertBefore(draggedItem, afterElement);
    }
  });

  areaList.addEventListener('drop', (e) => {
    e.preventDefault();
    onOrderChange();
  });
}

function getDragAfterElement(container, y) {
  const draggableElements = [...container.querySelectorAll('.area-item:not(.dragging)')];

  return draggableElements.reduce((closest, child) => {
    const box = child.getBoundingClientRect();
    const offset = y - box.top - box.height / 2;

    if (offset < 0 && offset > closest.offset) {
      return { offset: offset, element: child };
    } else {
      return closest;
    }
  }, { offset: Number.NEGATIVE_INFINITY }).element;
}

export function sortAreaItems(element) {
  const areaList = element.querySelector('#area-list');
  if (!areaList) return;

  const items = Array.from(areaList.querySelectorAll('.area-item'));
  items.sort((a, b) => {
    const orderA = parseInt(a.dataset.order);
    const orderB = parseInt(b.dataset.order);
    return orderA - orderB;
  });

  items.forEach(item => areaList.appendChild(item));
}
