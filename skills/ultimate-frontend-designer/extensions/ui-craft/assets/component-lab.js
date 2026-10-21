/* Offline demonstrations only. Dynamic strings enter the DOM through textContent. */
'use strict';
(() => {
  const $ = (id) => document.getElementById(id);
  const on = (id, event, handler) => $(id).addEventListener(event, handler);
  const say = (id, message) => { $(id).textContent = message; };

  // Bounded initialization inventory: both DOM ids and pattern keys must be unique.
  const ids = [...document.querySelectorAll('[id]')].map((node) => node.id);
  const patterns = [...document.querySelectorAll('[data-pattern]')];
  const keys = patterns.map((node) => node.dataset.pattern);
  const duplicates = (values) => [...new Set(values.filter((value, index) => values.indexOf(value) !== index))];
  const repeated = [...duplicates(ids), ...duplicates(keys)];
  const valid = patterns.length === 19 && repeated.length === 0 && patterns.every((node) => node.id === node.dataset.pattern);
  say('inventory-status', valid ? '19 distinct patterns initialized · offline demo' : `Inventory issue: ${patterns.length} patterns; duplicate ids/keys: ${repeated.join(', ') || 'none'}. Expected 19 matching stable ids.`);
  if (!valid) console.error('Component lab inventory mismatch', { count: patterns.length, duplicates: repeated });

  let focused = false;
  on('focus-start', 'click', () => {
    focused = !focused;
    say('focus-start', focused ? 'End demo focus session' : 'Start a demo focus session');
    say('focus-status', focused ? 'Demo session active. Your next step: write one clear sentence.' : 'Demo session ended. Ready to start again.');
  });
  document.querySelectorAll('[name="rhythm"]').forEach((input) => input.addEventListener('change', () => say('rhythm-status', `Selected: ${input.value} minutes.`)));
  on('brief-toggle', 'click', () => {
    const expanded = $('brief-toggle').getAttribute('aria-expanded') === 'true';
    $('brief-toggle').setAttribute('aria-expanded', String(!expanded));
    $('brief-more').hidden = expanded;
    say('brief-toggle', expanded ? 'Read the full brief' : 'Collapse the full brief');
  });

  // Native modal dialogs provide focus containment and Escape. Explicit restoration
  // covers both close buttons and native cancel without depending on browser heuristics.
  const openers = new Map();
  function openDialog(id, opener) {
    openers.set(id, opener);
    $(id).showModal();
  }
  ['delivery-drawer', 'archive-dialog'].forEach((id) => {
    $(id).addEventListener('close', () => {
      const opener = openers.get(id);
      if (opener && !opener.hidden && !opener.disabled) opener.focus();
      else if (id === 'archive-dialog') $('archive-restore').focus();
    });
  });
  document.querySelectorAll('[data-close]').forEach((button) => button.addEventListener('click', () => $(button.dataset.close).close()));
  on('drawer-open', 'click', (event) => openDialog('delivery-drawer', event.currentTarget));

  const projects = {
    atlas: ['Atlas journal', 'An independent reading journal. Next: review the opening spread.', 'Owner: Demo editorial team'],
    tide: ['Tide index', 'A coastal field notebook. Next: organize the observation cards.', 'Owner: Demo research team'],
    moss: ['Moss archive', 'A material reference collection. Next: tag the paper samples.', 'Owner: Demo archive team']
  };
  document.querySelectorAll('[data-project]').forEach((button) => button.addEventListener('click', () => {
    document.querySelectorAll('[data-project]').forEach((item) => item.setAttribute('aria-pressed', String(item === button)));
    const project = projects[button.dataset.project];
    ['project-title', 'project-description', 'project-owner'].forEach((id, index) => say(id, project[index]));
  }));
  on('landscape-toggle', 'click', () => {
    const evening = $('landscape').classList.toggle('evening');
    $('landscape-toggle').setAttribute('aria-pressed', String(evening));
    say('landscape-toggle', evening ? 'Show dawn palette' : 'Show evening palette');
    say('landscape-title', `Original abstract mountain illustration at ${evening ? 'evening' : 'dawn'}`);
  });
  on('release-checks', 'change', () => {
    const count = $('release-checks').querySelectorAll(':checked').length;
    $('release-progress').value = count;
    $('release-progress').textContent = `${count} of 3`;
    say('progress-status', `${count} of 3 completed.${count === 3 ? ' Demo checklist ready.' : ''}`);
  });
  on('annual-plan', 'change', () => {
    const annual = $('annual-plan').checked;
    say('plan-price', annual ? '$10' : '$12');
    say('billing-detail', annual ? 'Demo annual total: $120, billed once. No checkout.' : 'Demo monthly total: $12. No checkout.');
    say('plan-status', 'Fictional pricing for layout reference.');
  });
  on('plan-preview', 'click', () => say('plan-status', $('annual-plan').checked ? 'Demo selection: annual, $120 total. Nothing purchased.' : 'Demo selection: monthly, $12 per month. Nothing purchased.'));
  on('differences-only', 'change', () => {
    document.querySelectorAll('#compare [data-same]').forEach((row) => { row.hidden = $('differences-only').checked; });
    say('compare-status', $('differences-only').checked ? 'Showing 2 differing rows.' : 'Showing all 3 comparison rows.');
  });
  let reviewComplete = false;
  on('timeline-advance', 'click', () => {
    reviewComplete = !reviewComplete;
    if (reviewComplete) $('timeline-review').removeAttribute('aria-current');
    else $('timeline-review').setAttribute('aria-current', 'step');
    $('timeline-review').querySelector('strong').textContent = reviewComplete ? 'Review · complete' : 'Review · current';
    say('timeline-advance', reviewComplete ? 'Reopen demo review' : 'Mark demo review complete');
    say('timeline-status', reviewComplete ? 'All three demo milestones complete.' : 'Two of three milestones complete.');
  });
  let eventCount = 2;
  on('activity-add', 'click', () => {
    eventCount += 1;
    const item = document.createElement('li');
    item.textContent = `Demo collaborator added a reference. Sample event ${eventCount}`;
    $('activity-feed').prepend(item);
    while ($('activity-feed').children.length > 5) $('activity-feed').lastElementChild.remove();
    say('activity-status', `${$('activity-feed').children.length} visible sample events. Latest 5 retained.`);
  });
  function setNotice(visible) {
    $('notice').hidden = !visible;
    $('notice-recovery').hidden = visible;
    say('notice-status', visible ? 'Reading notice restored.' : 'Reading notice dismissed. Undo is available.');
    $(visible ? 'notice-dismiss' : 'notice-undo').focus();
  }
  on('notice-dismiss', 'click', () => setNotice(false));
  on('notice-undo', 'click', () => setNotice(true));

  on('local-file', 'change', () => {
    const file = $('local-file').files[0];
    if (!file) { say('file-status', 'No file selected.'); return; }
    const allowed = /\.(png|jpe?g|pdf)$/i.test(file.name);
    const mimeAllowed = !file.type || ['image/png', 'image/jpeg', 'application/pdf'].includes(file.type);
    const validFile = allowed && mimeAllowed && file.size > 0 && file.size <= 2 * 1024 * 1024;
    $('local-file').setAttribute('aria-invalid', String(!validFile));
    say('file-status', validFile ? `Locally accepted: ${file.name} (${Math.ceil(file.size / 1024)} KiB). Metadata validation only; no upload.` : `Rejected: ${file.name}. Choose a nonempty PNG, JPEG, or PDF of at most 2 MiB. No upload occurred.`);
  });
  on('file-clear', 'click', () => {
    $('local-file').value = '';
    $('local-file').removeAttribute('aria-invalid');
    say('file-status', 'Local attachment cleared.');
  });

  const favoriteKey = 'ui-craft-pro:component-lab:quiet-workspace:v1';
  let favorite = false;
  function renderFavorite() {
    $('favorite-toggle').setAttribute('aria-pressed', String(favorite));
    say('favorite-toggle', favorite ? 'Remove Quiet workspace from favorites' : 'Save Quiet workspace');
  }
  try {
    favorite = localStorage.getItem(favoriteKey) === 'saved';
    say('favorite-status', favorite ? 'Saved in local storage.' : 'Not saved. Local storage is browser-specific.');
  } catch {
    say('favorite-status', 'Local storage is unavailable. Saving may fail; no saved state can be confirmed.');
  }
  renderFavorite();
  on('storage-failure', 'change', () => say('favorite-status', $('storage-failure').checked ? 'Demo failure enabled. Try the favorite button; the current state will be preserved.' : 'Demo failure disabled. Try saving again.'));
  on('favorite-toggle', 'click', () => {
    const next = !favorite;
    try {
      if ($('storage-failure').checked) throw new Error('Demo failure');
      if (next) localStorage.setItem(favoriteKey, 'saved');
      else localStorage.removeItem(favoriteKey);
      favorite = next;
      renderFavorite();
      say('favorite-status', favorite ? 'Favorite saved in local storage.' : 'Favorite removed from local storage.');
    } catch {
      say('favorite-status', $('storage-failure').checked ? 'Simulated demo storage failure. Favorite unchanged. Disable the failure option to retry.' : 'Storage write failed. Favorite unchanged. Browser privacy or storage settings may prevent saving.');
    }
  });

  let workspaceName = 'Paper studio';
  function finishEdit() {
    $('settings-form').hidden = true;
    $('settings-edit').hidden = false;
    $('settings-edit').focus();
  }
  on('settings-edit', 'click', () => {
    $('settings-form').hidden = false;
    $('settings-edit').hidden = true;
    $('workspace-input').value = workspaceName;
    $('workspace-input').removeAttribute('aria-invalid');
    say('settings-status', 'Editing demo name. No server is connected.');
    $('workspace-input').focus();
  });
  on('settings-cancel', 'click', () => { finishEdit(); say('settings-status', 'Edit canceled. Demo name unchanged.'); });
  on('workspace-input', 'input', () => $('workspace-input').removeAttribute('aria-invalid'));
  on('settings-form', 'submit', (event) => {
    event.preventDefault();
    const value = $('workspace-input').value.trim();
    if (value.length < 2 || value.length > 40) {
      $('workspace-input').setAttribute('aria-invalid', 'true');
      say('settings-status', 'Enter 2–40 characters after trimming surrounding spaces.');
      $('workspace-input').focus();
      return;
    }
    if ($('save-failure').checked) {
      say('settings-status', 'Simulated demo save failure. Your input is retained. Uncheck the failure option and retry.');
      return;
    }
    workspaceName = value;
    say('workspace-name', value);
    finishEdit();
    say('settings-status', 'Demo name saved in page memory only. Reload resets it.');
  });

  const tabs = [...document.querySelectorAll('#tabs [role="tab"]')];
  function activateTab(tab, focus) {
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      $(item.getAttribute('aria-controls')).hidden = !selected;
    });
    if (focus) tab.focus();
  }
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => activateTab(tab, false));
    tab.addEventListener('keydown', (event) => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      if (event.key === 'ArrowLeft') next = (index - 1 + tabs.length) % tabs.length;
      if (event.key === 'Home') next = 0;
      if (event.key === 'End') next = tabs.length - 1;
      if (next === undefined) return;
      event.preventDefault();
      activateTab(tabs[next], true);
    });
  });

  const records = [['The quiet margin', 'Essay'], ['Coastal notes', 'Field guide'], ['A room for paper', 'Interview'], ['Slow systems', 'Essay'], ['Collected mornings', 'Journal']];
  const pageSize = 2;
  let page = 0;
  function renderData() {
    const state = $('data-state').value;
    const ready = state === 'ready';
    $('data-results').hidden = !ready;
    $('data-body').replaceChildren();
    $('data-prev').disabled = !ready || page === 0;
    $('data-next').disabled = !ready || (page + 1) * pageSize >= records.length;
    $('data-retry').hidden = state !== 'error';
    if (!ready) {
      say('data-status', state === 'empty' ? 'No reading records. Choose Ready to restore the sample dataset.' : 'Simulated demo load error. No remote request was made. Retry restores the sample dataset.');
      return;
    }
    records.slice(page * pageSize, (page + 1) * pageSize).forEach((record) => {
      const row = document.createElement('tr');
      record.forEach((value) => { const cell = document.createElement('td'); cell.textContent = value; row.append(cell); });
      $('data-body').append(row);
    });
    say('data-status', `Page ${page + 1} of ${Math.ceil(records.length / pageSize)} · records ${page * pageSize + 1}–${Math.min((page + 1) * pageSize, records.length)} of ${records.length}.`);
  }
  on('data-state', 'change', () => { page = 0; renderData(); });
  on('data-prev', 'click', () => { if (page > 0) page -= 1; renderData(); });
  on('data-next', 'click', () => { if ((page + 1) * pageSize < records.length) page += 1; renderData(); });
  on('data-retry', 'click', () => { $('data-state').value = 'ready'; page = 0; renderData(); $('data-state').focus(); });
  renderData();

  on('archive-open', 'click', (event) => openDialog('archive-dialog', event.currentTarget));
  on('archive-confirm', 'click', () => {
    $('archive-open').hidden = true;
    $('archive-restore').hidden = false;
    say('archive-status', 'Demo draft archived in page memory. Restore is available.');
    $('archive-dialog').close();
  });
  on('archive-restore', 'click', () => {
    $('archive-open').hidden = false;
    $('archive-restore').hidden = true;
    say('archive-status', 'Demo draft restored.');
    $('archive-open').focus();
  });
  on('effects-pause', 'click', () => {
    const paused = $('effects').classList.toggle('paused');
    $('effects-pause').setAttribute('aria-pressed', String(paused));
    say('effects-pause', paused ? 'Resume decorative effects' : 'Pause decorative effects');
  });
})();
