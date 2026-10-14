(function () {
  'use strict';
  if (!document.documentElement.classList.contains('desktop-shell')) return;

  var routeLabels = {
    home: 'COMMAND CENTER', quests: 'DAILY PROTOCOL', dungeon: 'QUESTS & BOSSES',
    character: 'CHARACTER & STATUS', skills: 'SKILL TREE & MASTERY',
    inventory: 'INVENTORY & EQUIPMENT', vault: 'JOURNAL & PROOF VAULT',
    more: 'ANALYTICS & ACHIEVEMENTS', world: 'LIVING WORLD',
    arc: 'PERSONAL ARC', ascension: 'LIFETIME RECORD'
  };

  function esc(value) {
    if (typeof escapeHTML === 'function') return escapeHTML(String(value == null ? '' : value));
    return String(value == null ? '' : value).replace(/[&<>"']/g, function (c) {
      return ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c];
    });
  }
  function setText(id, value) {
    var el = document.getElementById(id);
    if (el) el.textContent = value;
  }
  function progress(value, total) {
    if (!total) return 0;
    return Math.max(0, Math.min(100, Math.round((Number(value) / Number(total)) * 100)));
  }
  function nextRank(level) {
    var ranks = [{ level: 5, name: 'D' }, { level: 12, name: 'C' }, { level: 20, name: 'B' }, { level: 30, name: 'A' }, { level: 40, name: 'S' }, { level: 55, name: 'MONARCH' }];
    return ranks.find(function (rank) { return level < rank.level; }) || null;
  }
  function addDashboard() {
    var main = document.querySelector('.layout .maincol');
    if (!main || document.getElementById('desktopDashboard')) return;
    var section = document.createElement('section');
    section.id = 'desktopDashboard';
    section.className = 'card section shadow-screen';
    section.dataset.shadowScreen = 'home';
    section.innerHTML = [
      '<div class="ss-dashboard">',
      '  <section class="ss-overview">',
      '    <div class="ss-welcome"><div><div class="ss-kicker" id="desktopKicker">WINTER ARC // COMMAND CENTER</div><h1 id="desktopWelcome">Welcome back, Shadow.</h1><p id="desktopWelcomeSub">Another day. Another step toward your true self.</p></div><div class="ss-welcome-quote">“The only limit is the one you accept.”</div></div>',
      '    <div class="ss-status-cards">',
      '      <article class="ss-status-card ss-rank-card"><div class="ss-rank-emblem"><img id="desktopRankEmblem" src="assets/rank_e.webp" alt="Current rank emblem"></div><div class="ss-status-main"><span class="ss-card-label" id="desktopRank">E GRADE</span><strong id="desktopLevel">Lv. 1</strong><div class="ss-progress"><i id="desktopXpProgress"></i></div><small id="desktopXpText">0 / 100 XP</small></div></article>',
      '      <article class="ss-status-card ss-arc-card"><div class="ss-card-label">CURRENT STAGE</div><strong id="desktopChapter">1. Awakening</strong><div class="ss-arc-day"><span id="desktopDay">Day 1 / 90</span><button class="ss-link" data-go="arc">VIEW CALENDAR →</button></div><div class="ss-progress"><i id="desktopArcProgress"></i></div><small id="desktopArcText">Lifetime progression</small></article>',
      '      <article class="ss-status-card ss-next-card"><div class="ss-next-emblem"><img id="desktopNextRankEmblem" src="assets/rank_d.webp" alt="Next rank emblem"></div><div><div class="ss-card-label">NEXT RANK</div><strong id="desktopNextRank">D Grade</strong><small id="desktopNextRankSub">Need — XP</small></div></article>',
      '    </div>',
      '  </section>',
      '  <div class="ss-main-row">',
      '    <section class="ss-panel ss-mission-panel"><div class="ss-panel-head"><div class="ss-title-with-icon"><span class="ss-panel-icon">✧</span><div><div class="ss-panel-title" id="desktopMissionTitle">TODAY\'S MISSION</div><div class="ss-panel-sub" id="desktopProtocolState">Complete your daily training routine and log your progress.</div></div></div><span class="ss-priority">YOUR PROTOCOL</span></div><div class="ss-mission-content"><div><div class="ss-task-list" id="desktopTasks"></div></div><div class="ss-reward-box"><div class="ss-reward-title" id="desktopRecordTitle">TODAY\'S RECORD</div><div class="ss-reward-line"><span>MISSIONS</span><b id="desktopRewardMissions">0 / 5</b></div><div class="ss-reward-line"><span>XP EARNED</span><b id="desktopRewardXp">0 XP</b></div><div class="ss-reward-line"><span>LIFETIME MISSIONS</span><b id="desktopDone">0 recorded</b></div><button class="control-btn primary ss-start-mission" data-action="focus-toggle" title="Start or pause your focus timer">START MISSION</button><button class="ss-link" data-go="quests">OPEN DAILY PROTOCOL →</button></div></div></section>',
      '    <section class="ss-panel ss-arc-panel"><div class="ss-panel-head"><div class="ss-title-with-icon"><span class="ss-panel-icon">⌖</span><div><div class="ss-panel-title" id="desktopArcTitle">YOUR ARC</div><div class="ss-panel-sub" id="desktopArcSubtitle">A route you define, with progression that continues for life.</div></div></div><button class="ss-link" data-go="arc">VIEW CALENDAR →</button></div><div class="ss-arc-rail" id="desktopChapters"></div><div class="ss-today-progress"><div class="ss-progress-label"><span id="desktopProgressLabel">SELECTED DAY</span><b id="desktopTodayCount">0/5</b></div><div class="ss-progress"><i id="desktopTodayProgress"></i></div><div class="ss-today-stats"><div><span>MOMENTUM</span><b id="desktopMomentum">0%</b></div><div><span>TRAINING</span><b id="desktopTraining">0%</b></div><div><span>LEARNING</span><b id="desktopLearning">0%</b></div></div></div></section>',
      '  </div>',
      '  <div class="ss-lower-row">',
      '    <section class="ss-panel ss-quests-panel"><div class="ss-panel-head"><div class="ss-title-with-icon"><span class="ss-panel-icon">◇</span><div><div class="ss-panel-title">ACTIVE QUESTS</div><div class="ss-panel-sub">Daily and personal objectives from your saved record.</div></div></div><button class="ss-link" data-go="dungeon">VIEW ALL →</button></div><div id="desktopSideQuests"></div><form class="ss-quest-form" id="desktopQuestForm"><input id="desktopQuestInput" class="text-input" maxlength="60" aria-label="New side quest" placeholder="Add a personal quest"><select id="desktopQuestCadence" aria-label="Quest schedule"><option value="once">Once</option><option value="daily">Daily</option><option value="weekly">Weekly</option><option value="monthly">Monthly</option></select><input id="desktopQuestReward" type="number" min="0" max="10000" step="1" value="20" aria-label="Quest XP reward"><button class="control-btn primary" type="submit">ADD QUEST</button></form></section>',
      '    <section class="ss-panel ss-achievements-panel"><div class="ss-panel-head"><div class="ss-title-with-icon"><span class="ss-panel-icon">♜</span><div><div class="ss-panel-title">RECENT ACHIEVEMENTS</div><div class="ss-panel-sub" id="desktopAchievementCount">Earned through recorded progress.</div></div></div><button class="ss-link" data-go="more">VIEW ALL →</button></div><div id="desktopAchievements"></div></section>',
      '    <section class="ss-panel ss-journal-panel"><div class="ss-panel-head"><div class="ss-title-with-icon"><span class="ss-panel-icon">▤</span><div><div class="ss-panel-title">LATEST JOURNAL ENTRY</div><div class="ss-panel-sub">Your private reflection, saved locally.</div></div></div><button class="ss-link" data-go="vault">VIEW ALL →</button></div><div class="ss-journal-entry"><div class="ss-journal-meta"><span class="ss-journal-mark">▤</span><div><b id="desktopJournalTitle">Today\'s Reflection</b><small id="desktopJournalDate">Not saved yet</small></div><button class="ss-journal-edit" type="button" data-action="journal-edit" aria-label="Edit journal entry" title="Edit journal entry">✎</button></div><textarea class="ss-journal" id="desktopJournalDraft" maxlength="3000" placeholder="Write today\'s reflection here…"></textarea><div class="ss-journal-tags"><button type="button" data-journal-tag="Focus">Focus</button><button type="button" data-journal-tag="Progress">Progress</button><button type="button" data-journal-tag="Gratitude">Gratitude</button></div><div class="ss-journal-actions"><span class="ss-kpi-sub" id="desktopJournalStatus">Not saved yet</span><button class="control-btn" data-action="journal-save">SAVE</button></div></div></section>',
      '  </div>',
      '  <footer class="ss-quote-footer"><span>“Progress is not a matter of luck, but of consistent effort.”</span><button class="control-btn primary" data-action="level-up">LEVEL UP →</button></footer>',
      '</div>'
    ].join('');
    main.insertBefore(section, main.firstChild);
  }

  function addVaultJournal() {
    var vault = document.querySelector('.shadow-screen[data-shadow-screen="vault"]');
    if (!vault || document.getElementById('desktopVaultJournal')) return;
    var panel = document.createElement('section');
    panel.id = 'desktopVaultJournal';
    panel.className = 'card section ss-vault-journal';
    panel.innerHTML = '<div class="section-head"><div><div class="section-title">PRIVATE JOURNAL</div><div class="section-sub">Your note is saved with the Change 19 local state and included in the normal data export.</div></div><span class="system-chip">LOCAL SAVE</span></div><textarea id="desktopVaultJournalText" maxlength="3000" rows="7" placeholder="Write a reflection or record the next step."></textarea><div class="note-actions"><span class="small" id="desktopVaultJournalStatus">Not saved yet</span><button class="control-btn primary" data-action="vault-journal-save">SAVE JOURNAL</button></div>';
    vault.appendChild(panel);
  }

  function installNavigation() {
    var nav = document.querySelector('.screen-nav');
    if (!nav) return;
    var visibleOrder = ['home', 'quests', 'dungeon', 'character', 'skills', 'inventory', 'vault', 'more'];
    visibleOrder.forEach(function (route) {
      var button = nav.querySelector('.nav-item[data-screen="' + route + '"]');
      if (!button) return;
      button.dataset.desktopRoute = route;
      var label = button.querySelector('.nav-label');
      if (label) label.textContent = routeLabels[route];
      nav.appendChild(button);
    });
    ['world', 'arc', 'ascension'].forEach(function (route) {
      var button = nav.querySelector('.nav-item[data-screen="' + route + '"]');
      if (button) button.remove();
    });
    if (!nav.querySelector('[data-desktop-action="settings"]')) {
      var settingsButton = document.createElement('button');
      settingsButton.className = 'nav-item ss-settings-nav';
      settingsButton.type = 'button';
      settingsButton.dataset.action = 'settings';
      settingsButton.setAttribute('aria-label', 'Open system settings');
      settingsButton.innerHTML = '<span class="nav-icon">⚙</span><span class="nav-label">SETTINGS</span>';
      nav.appendChild(settingsButton);
    }
    if (!document.getElementById('desktopSidebarSummary')) {
      var summary = document.createElement('aside');
      summary.id = 'desktopSidebarSummary';
      summary.className = 'ss-sidebar-summary';
      summary.innerHTML = '<div class="ss-sidebar-art" role="img" aria-label="Shadow System character artwork"></div><div class="ss-sidebar-copy"><div class="ss-sidebar-kicker" id="desktopSidebarArc">⌘ &nbsp; YOUR ARC</div><div class="ss-sidebar-chapter" id="desktopSidebarChapter">Stage 1 · Awakening</div><div class="ss-sidebar-day" id="desktopSidebarDay">Lifetime Day 1</div><div class="ss-progress"><i id="desktopSidebarArcProgress"></i></div><div class="ss-sidebar-rank"><span>RANK</span><b id="desktopSidebarRank">E Grade</b><span id="desktopSidebarLevel">Lv. 1</span></div><div class="ss-progress"><i id="desktopSidebarXpProgress"></i></div><div class="ss-sidebar-links"><button type="button" data-go="arc">ARC CALENDAR</button><button type="button" data-go="world">LIVING WORLD</button><button type="button" data-go="ascension">LIFETIME RECORD</button></div><p class="ss-sidebar-motto">“Small steps build monsters.”</p></div>';
      nav.appendChild(summary);
    }
    var original = window.switchSystemScreen;
    if (typeof original !== 'function') return;
    window.switchSystemScreen = function (route) {
      var baseRoute = route === 'analytics' ? 'more' : route;
      original(baseRoute);
      if (route === 'more' || route === 'analytics') activateTab('analytics');
      var activeRoute = route === 'journal' ? 'vault' : route === 'analytics' ? 'more' : route;
      document.querySelectorAll('.screen-nav .nav-item').forEach(function (button) {
        button.classList.toggle('active', button.dataset.desktopRoute === activeRoute);
      });
      renderDesktopDashboard();
    };
  }

  function activateTab(name) {
    var tab = document.querySelector('.tab[data-tab="' + name + '"]');
    if (tab) tab.click();
  }

  function renderChapters(dayNo) {
    var box = document.getElementById('desktopChapters');
    if (!box) return;
    var current = Math.max(1, dayNo);
    box.innerHTML = CHAPTERS.map(function (chapter, index) {
      var past = dayNo > chapter.to;
      var active = dayNo >= chapter.from && dayNo <= chapter.to;
      var width = active ? progress(dayNo - chapter.from + 1, chapter.to - chapter.from + 1) : (past ? 100 : 0);
      return '<button type="button" class="ss-chapter ' + (active ? 'is-current ' : '') + (past ? 'is-past' : '') + '" data-go="arc" aria-label="Open chapter ' + (index + 1) + ': ' + esc(chapter.name) + '"><b>' + (index + 1) + '</b><span>' + esc(chapter.name) + '</span><small>Day ' + chapter.from + '–' + chapter.to + '</small><div class="ss-mini-progress"><i style="width:' + width + '%"></i></div></button>';
    }).join('');
  }

  function renderTasks(dayNo, dayIndex) {
    var box = document.getElementById('desktopTasks');
    if (!box) return;
    var locked = dayIsLocked(dayIndex), active = TASKS.filter(function (task) { return task.enabled !== false; });
    box.innerHTML = TASKS.map(function (task, index) {
      var done = dayRecordValue(dayIndex, index), unavailable = locked || task.enabled === false;
      return '<button class="ss-task ' + (done ? 'is-done' : '') + '" type="button" data-task-index="' + index + '" ' + (unavailable ? 'disabled' : '') + ' aria-pressed="' + done + '"><span class="ss-task-check">' + (done ? '✓' : '') + '</span><span><span class="ss-task-name">' + esc(task.name) + '</span><span class="ss-task-desc">' + esc(task.desc) + '</span></span><span class="ss-task-reward">' + (task.enabled === false ? 'PAUSED' : done ? 'RECORDED' : '+' + Math.round(task.xp * (Number(state.settings.multiplier) || 1)) + ' XP') + '</span></button>';
    }).join('');
    var message = locked ? 'This date is read-only.' : 'Select a routine to record or undo progress for this date.';
    setText('desktopProtocolState', message);
    setText('desktopTodayCount', dayCount(dayIndex) + '/' + active.length);
    var todayFill = document.getElementById('desktopTodayProgress');
    if (todayFill) todayFill.style.width = progress(dayCount(dayIndex), active.length) + '%';
    var categories = [
      { name: 'Training', ids: ['str'] },
      { name: 'Learning', ids: ['int', 'per', 'wil'] },
      { name: 'Deep work', ids: ['foc'] }
    ];
    var stats = document.getElementById('desktopCategoryProgress');
    if (stats) stats.innerHTML = categories.map(function (category) {
      var tasks = TASKS.map(function (task, index) { return { task: task, index: index }; }).filter(function (entry) { return entry.task.enabled !== false && category.ids.indexOf(entry.task.id) >= 0; });
      var done = tasks.filter(function (entry) { return dayRecordValue(dayIndex, entry.index); }).length;
      var percent = progress(done, tasks.length);
      return '<div class="ss-progress-item"><span>' + category.name + '</span><div class="ss-progress"><i style="width:' + percent + '%"></i></div><b>' + done + '/' + tasks.length + '</b></div>';
    }).join('');
  }

  function renderSideQuests() {
    var box = document.getElementById('desktopSideQuests');
    if (!box) return;
    var dayIndex = protocolDay(), today = dayCount(dayIndex), activeCount = TASKS.filter(function (task) { return task.enabled !== false; }).length;
    var learningTasks = TASKS.map(function (task, index) { return { task: task, index: index }; }).filter(function (entry) { return entry.task.enabled !== false && ['int', 'per', 'wil'].indexOf(entry.task.id) >= 0; });
    var learning = learningTasks.filter(function (entry) { return dayRecordValue(dayIndex, entry.index); }).length;
    var quests = (state.customQuests || []).map(function (quest, index) { return { quest: quest, index: index }; }).filter(function (entry) { return entry.quest.enabled !== false && !isCustomQuestDone(entry.quest, dayIndex); }).slice(0, 2);
    var rows = [
      '<div class="ss-quest-row"><span class="ss-quest-badge purple">✧</span><span><span class="ss-row-name">Daily Mission</span><span class="ss-row-meta">' + esc(dayDate(dayIndex)) + ' · ' + (state.viewDay == null ? 'current date' : 'selected date') + '</span></span><button class="ss-quest-count" type="button" data-go="quests">' + today + '/' + activeCount + '</button></div>',
      '<div class="ss-quest-row"><span class="ss-quest-badge cyan">⚔</span><span><span class="ss-row-name">Weekly Boss</span><span class="ss-row-meta">Current boss integrity · ' + Math.max(0, 100 - Number(state.bossDamage || 0)) + '%</span></span><button class="ss-quest-count" type="button" data-go="dungeon">' + Math.min(100, Number(state.bossDamage || 0)) + '%</button></div>',
      '<div class="ss-quest-row"><span class="ss-quest-badge green">✦</span><span><span class="ss-row-name">Learning Protocol</span><span class="ss-row-meta">Your active learning routines</span></span><button class="ss-quest-count" type="button" data-go="quests">' + learning + '/' + learningTasks.length + '</button></div>'
    ];
    quests.forEach(function (entry) {
      var name = entry.quest.text || entry.quest.name || 'Personal Quest';
      rows.push('<div class="ss-quest-row"><span class="ss-quest-badge gold">⌁</span><span><span class="ss-row-name">' + esc(name) + '</span><span class="ss-row-meta">' + esc((entry.quest.cadence || 'one time').toUpperCase()) + ' · +' + esc(entry.quest.xp || 20) + ' XP</span></span><button class="ss-quest-count ss-quest-complete" type="button" data-quest-index="' + entry.index + '" aria-label="Complete ' + esc(name) + '">✓</button></div>');
    });
    if (!quests.length) rows.push('<div class="ss-quest-empty">Your personal quest board is clear. Add a real objective below.</div>');
    box.innerHTML = rows.join('');
  }

  function renderAchievements() {
    var box = document.getElementById('desktopAchievements');
    if (!box) return;
    var source = document.querySelectorAll('#achievementList .achievement');
    var earned = Array.prototype.slice.call(source).filter(function (item) { return !item.classList.contains('locked'); });
    var all = Array.prototype.slice.call(source);
    setText('desktopAchievementCount', earned.length + ' earned from the current saved record');
    var display = (earned.length ? earned.slice(-3).reverse() : all.slice(0, 2));
    box.innerHTML = display.map(function (item) {
      var mark = item.querySelector('.achievement-icon');
      var title = item.querySelector('strong');
      var desc = item.querySelector('p');
      return '<div class="ss-achievement"><span class="ss-achievement-mark">' + esc(mark ? mark.textContent : '✦') + '</span><span><span class="ss-achievement-name">' + esc(title ? title.textContent : 'Achievement') + '</span><span class="ss-achievement-desc">' + esc(desc ? desc.textContent : '') + (earned.length ? '' : ' · not earned yet') + '</span></span></div>';
    }).join('') || '<div class="ss-empty">Achievements will appear as recorded tasks, focus sessions, and journal entries meet their requirements.</div>';
  }

  function renderActivity() {
    var box = document.getElementById('desktopActivity');
    if (!box) return;
    var events = (state.events || []).slice(0, 3);
    box.innerHTML = events.map(function (event) {
      var when = event.time ? new Date(event.time).toLocaleString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'Saved activity';
      return '<div class="ss-event-row"><span class="ss-row-icon">' + esc(event.icon || '✦') + '</span><span><span class="ss-row-name">' + esc(event.text || 'System activity') + '</span><span class="ss-row-meta">' + esc(when) + '</span></span></div>';
    }).join('') || '<div class="ss-empty">No activity has been recorded yet.</div>';
  }

  function renderDashboard() {
    if (!document.getElementById('desktopDashboard') || typeof state === 'undefined') return;
    var dayIndex = protocolDay();
    var dayNo = dayIndex < 0 ? 0 : ((dayIndex % DAYS) + DAYS) % DAYS + 1;
    var lifetimeDay = Math.max(0, dayIndex + 1);
    var selectedDate = dayDate(dayIndex);
    var isToday = selectedDate === todayKey();
    var xp = Number(state.xp) || 0;
    var level = levelFromXP(xp);
    var rank = rankForLevel(level);
    var next = nextLevelXP(level);
    var previous = Math.pow(level - 1, 2) * 5;
    var levelPct = level >= 31 ? 100 : progress(Math.max(0, xp - previous), Math.max(1, next - previous));
    var nextRankGoal = nextRank(level);
    var nextRankXp = nextRankGoal ? Math.pow(nextRankGoal.level - 1, 2) * 5 : null;
    var done = totalDone();
    var name = (state.settings && state.settings.name) || 'Shadow';
    if (name === 'MONARCH') name = 'Shadow';
    var arcName = String(state.arc || 'Personal Arc').trim() || 'Personal Arc';
    var chapter = dayIndex < 0 ? { name: 'Before start' } : chapterForDay(dayNo);
    var today = dayCount(dayIndex);
    var activeTasks = TASKS.filter(function (task) { return task.enabled !== false; });
    var learned = TASKS.map(function (task, index) { return { task: task, index: index }; }).filter(function (entry) { return entry.task.enabled !== false && ['int', 'per', 'wil'].indexOf(entry.task.id) >= 0; });
    var todayXp = TASKS.reduce(function (sum, task, index) { return sum + (task.enabled !== false && dayRecordValue(dayIndex, index) ? Math.round(task.xp * (Number(state.settings.multiplier) || 1)) : 0); }, 0);
    setText('desktopWelcome', 'Welcome back, ' + name + '.');
    setText('desktopKicker', arcName.toUpperCase() + ' // COMMAND CENTER');
    setText('desktopBrandArc', '// ' + arcName.toUpperCase());
    setText('desktopWelcomeSub', (state.arcGoal || 'Another day. Another step towards your true self.') + (isToday ? '' : ' · Viewing ' + new Date(selectedDate + 'T00:00:00').toLocaleDateString()));
    setText('desktopRank', rank + ' GRADE');
    setText('desktopLevel', 'Lv. ' + level);
    var currentEmblem = document.getElementById('desktopRankEmblem');
    if (currentEmblem) currentEmblem.src = 'assets/rank_' + rank.toLowerCase() + '.webp';
    setText('desktopXpText', Math.round(Math.max(0, xp - previous)) + ' / ' + Math.round(Math.max(0, next - previous)) + ' XP');
    var xpBar = document.getElementById('desktopXpProgress'); if (xpBar) xpBar.style.width = levelPct + '%';
    var chapterNumber = dayIndex < 0 ? 0 : CHAPTERS.indexOf(chapter) + 1;
    setText('desktopDay', dayIndex < 0 ? 'Before arc start' : 'Day ' + dayNo + ' / ' + DAYS);
    setText('desktopChapter', dayIndex < 0 ? 'Before start' : chapterNumber + '. ' + chapter.name);
    var arcBar = document.getElementById('desktopArcProgress'); if (arcBar) arcBar.style.width = progress(dayNo, DAYS) + '%';
    setText('desktopArcTitle', String(state.arc || 'YOUR ARC').toUpperCase());
    setText('desktopArcSubtitle', state.arcGoal || 'A route you define, with progression that continues for life.');
    setText('desktopArcText', 'Lifetime day ' + Math.max(1, lifetimeDay) + ' · ' + (state.arcEndDate && selectedDate > state.arcEndDate ? 'Arc complete · progression continues' : 'Route in progress'));
    setText('desktopDone', done + ' recorded');
    setText('desktopNextRank', nextRankGoal ? nextRankGoal.name + ' Grade' : 'Monarch');
    setText('desktopNextRankSub', nextRankGoal ? 'Need ' + Math.max(0, nextRankXp - xp) + ' XP' : 'Highest rank reached');
    var nextEmblem = document.getElementById('desktopNextRankEmblem');
    if (nextEmblem) nextEmblem.src = 'assets/rank_' + (nextRankGoal ? nextRankGoal.name.toLowerCase() : 'monarch') + '.webp';
    setText('desktopRewardMissions', today + ' / ' + activeTasks.length);
    setText('desktopRewardXp', todayXp + ' XP');
    setText('desktopTodayCount', today + '/' + activeTasks.length);
    setText('desktopMomentum', progress(today, activeTasks.length) + '%');
    var trainingTask = TASKS.map(function (task, index) { return { task: task, index: index }; }).find(function (entry) { return entry.task.enabled !== false && entry.task.id === 'str'; });
    setText('desktopTraining', (trainingTask && dayRecordValue(dayIndex, trainingTask.index) ? 100 : 0) + '%');
    setText('desktopLearning', progress(learned.filter(function (entry) { return dayRecordValue(dayIndex, entry.index); }).length, learned.length) + '%');
    setText('desktopMissionTitle', isToday ? 'TODAY\'S MISSION' : 'MISSION · ' + new Date(selectedDate + 'T00:00:00').toLocaleDateString());
    setText('desktopRecordTitle', isToday ? 'TODAY\'S RECORD' : 'SELECTED DAY');
    setText('desktopProgressLabel', isToday ? 'TODAY\'S PROGRESS' : 'SELECTED DAY PROGRESS');
    setText('desktopSidebarArc', '⌘  ' + String(state.arc || 'PERSONAL ARC').toUpperCase());
    setText('desktopSidebarChapter', dayIndex < 0 ? 'Before start' : chapter.name + ' · Stage ' + chapterNumber);
    setText('desktopSidebarDay', dayIndex < 0 ? 'Before arc start · ' + selectedDate : 'Lifetime Day ' + lifetimeDay + ' · Day ' + dayNo + '/' + DAYS);
    setText('desktopSidebarRank', rank + ' Grade');
    setText('desktopSidebarLevel', 'Lv. ' + level);
    var sideArcBar = document.getElementById('desktopSidebarArcProgress'); if (sideArcBar) sideArcBar.style.width = progress(dayNo, DAYS) + '%';
    var sideXpBar = document.getElementById('desktopSidebarXpProgress'); if (sideXpBar) sideXpBar.style.width = levelPct + '%';
    var headerDay = document.getElementById('desktopHeaderDay');
    if (headerDay) headerDay.textContent = dayIndex < 0 ? 'Before arc start · ' + selectedDate : 'Lifetime Day ' + lifetimeDay + '  ·  Day ' + dayNo + '/' + DAYS + ' · ' + chapter.name;
    var headerClock = document.getElementById('desktopHeaderClock');
    if (headerClock) headerClock.textContent = new Date().toLocaleString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    renderTasks(dayNo, dayIndex);
    renderChapters(dayNo);
    renderSideQuests();
    renderAchievements();
    renderActivity();
    var draft = document.getElementById('desktopJournalDraft');
    if (draft && document.activeElement !== draft) draft.value = state.journal || '';
    var vaultDraft = document.getElementById('desktopVaultJournalText');
    if (vaultDraft && document.activeElement !== vaultDraft) vaultDraft.value = state.journal || '';
    setText('desktopJournalStatus', state.journal ? 'Saved in this device profile' : 'No note saved yet');
    setText('desktopVaultJournalStatus', state.journal ? 'Saved in this device profile' : 'No note saved yet');
    setText('desktopJournalTitle', state.journal ? 'Reflection · ' + selectedDate : 'Today\'s Reflection');
    setText('desktopJournalDate', state.journal ? 'Saved locally · ' + new Date(state.lastSave || Date.now()).toLocaleString([], { month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'No reflection recorded yet');
    var mainTimer = document.getElementById('timerDisplay');
    setText('desktopFocusTime', mainTimer ? mainTimer.textContent : '25:00');
    var timerButton = document.getElementById('timerStart');
    var focusButton = document.querySelector('[data-action="focus-toggle"]');
    if (focusButton) focusButton.textContent = timer && timer.running ? 'PAUSE MISSION' : timerButton && timerButton.textContent === 'RESUME' ? 'RESUME MISSION' : 'START MISSION';
    setText('desktopFocusState', timer && timer.running ? 'Focus timer running · keep your attention here' : 'Deep work · timer idle');
    var input = document.getElementById('desktopQuestInput');
    if (input) input.disabled = false;
    var add = document.querySelector('#desktopQuestForm button');
    if (add) add.disabled = false;
    var journalSave = document.querySelector('[data-action="journal-save"]');
    if (journalSave) journalSave.disabled = !state;
  }

  function saveDesktopJournal(source) {
    var draft = document.getElementById(source);
    var canonical = document.getElementById('journalText');
    if (!draft || !canonical || typeof saveJournal !== 'function') return;
    canonical.value = draft.value;
    saveJournal();
    renderDesktopDashboard();
  }

  addDashboard();
  addVaultJournal();
  installNavigation();
  (state.customQuests || []).forEach(function (quest) {
    if (!quest.text && quest.name) quest.text = quest.name;
    if (!quest.name && quest.text) quest.name = quest.text;
  });
  if (typeof renderAll === 'function') {
    var originalRender = window.renderAll;
    window.renderAll = function () {
      originalRender();
      renderDesktopDashboard();
    };
  }
  document.addEventListener('click', function (event) {
    var taskButton = event.target.closest('#desktopTasks [data-task-index]');
    if (taskButton) {
      setTask(protocolDay(), Number(taskButton.dataset.taskIndex));
      return;
    }
    var questButton = event.target.closest('#desktopSideQuests [data-quest-index]');
    if (questButton) { toggleCustomDeep(Number(questButton.dataset.questIndex), protocolDay()); return; }
    var go = event.target.closest('[data-go]');
    if (go) {
      var route = go.dataset.go;
      if (route === 'more') route = 'analytics';
      window.switchSystemScreen(route);
      if (route === 'more' || route === 'analytics') activateTab('achievements');
      return;
    }
    var action = event.target.closest('[data-action]');
    var journalTag = event.target.closest('[data-journal-tag]');
    if (journalTag) {
      var journalInput = document.getElementById('desktopJournalDraft');
      if (journalInput) {
        var tag = '#' + journalTag.dataset.journalTag + ' ';
        var start = journalInput.selectionStart == null ? journalInput.value.length : journalInput.selectionStart;
        var end = journalInput.selectionEnd == null ? start : journalInput.selectionEnd;
        journalInput.setRangeText(tag, start, end, 'end');
        journalInput.focus();
        journalInput.dispatchEvent(new Event('input', { bubbles: true }));
      }
      return;
    }
    if (!action) return;
    if (action.dataset.action === 'settings') { openModal('settingsModal'); return; }
    if (action.dataset.action === 'data') { openModal('dataModal'); return; }
    if (action.dataset.action === 'command') { openCommand(); return; }
    if (action.dataset.action === 'level-up') {
      window.switchSystemScreen('character');
      toast('LEVEL PROGRESSION', 'Levels advance automatically when recorded work earns enough XP.');
      return;
    }
    if (action.dataset.action === 'journal-save') saveDesktopJournal('desktopJournalDraft');
    if (action.dataset.action === 'vault-journal-save') saveDesktopJournal('desktopVaultJournalText');
    if (action.dataset.action === 'focus-toggle') { if (typeof toggleTimer === 'function') toggleTimer(); renderDesktopDashboard(); }
    if (action.dataset.action === 'focus-reset') { if (typeof resetTimer === 'function') resetTimer(); renderDesktopDashboard(); }
    if (action.dataset.action === 'journal-edit') {
      var journal = document.getElementById('desktopJournalDraft');
      if (journal) journal.focus();
    }
  });
  document.addEventListener('submit', function (event) {
    if (event.target.id !== 'desktopQuestForm') return;
    event.preventDefault();
    var input = document.getElementById('desktopQuestInput');
    var legacyInput = document.getElementById('customQuest');
    if (!input || !legacyInput) return;
    legacyInput.value = input.value;
    var cadence = document.getElementById('desktopQuestCadence');
    var reward = document.getElementById('desktopQuestReward');
    var baseCadence = document.getElementById('questCadenceSetting');
    var baseReward = document.getElementById('questRewardSetting');
    if (baseCadence && cadence) baseCadence.value = cadence.value;
    if (baseReward && reward) baseReward.value = reward.value;
    forgeQuestDeep();
    input.value = '';
  });
  document.addEventListener('change', function (event) {
    if (event.target.id === 'desktopVaultJournalText' || event.target.id === 'desktopJournalDraft') {
      state.journal = event.target.value;
      clearTimeout(window.desktopJournalSaveTimer);
      window.desktopJournalSaveTimer = setTimeout(function () { persist(); setText('desktopJournalStatus', 'Autosaved to this device'); setText('desktopVaultJournalStatus', 'Autosaved to this device'); }, 500);
    }
  });
  document.addEventListener('input', function (event) {
    if (event.target.id !== 'desktopVaultJournalText' && event.target.id !== 'desktopJournalDraft') return;
    state.journal = event.target.value;
    clearTimeout(window.desktopJournalSaveTimer);
    window.desktopJournalSaveTimer = setTimeout(function () { persist(); setText('desktopJournalStatus', 'Autosaved to this device'); setText('desktopVaultJournalStatus', 'Autosaved to this device'); }, 500);
  });
  var header = document.querySelector('.system-header');
  if (header) {
    var brand = header.querySelector(':scope > div');
    var nav = header.querySelector('.screen-nav');
    var actions = header.querySelector('.top-actions');
    if (brand) {
      brand.className = 'ss-brand';
      brand.innerHTML = '<span class="ss-brand-mark"><img src="assets/desktop-logo.png" alt="Shadow System emblem"></span><span class="ss-brand-copy"><span class="system-title">SHADOW SYSTEM</span><span class="system-state" id="desktopBrandArc">// WINTER ARC</span></span>';
    }
    if (nav && !document.getElementById('desktopHeaderQuote')) {
      var quote = document.createElement('div');
      quote.id = 'desktopHeaderQuote';
      quote.className = 'ss-headline';
      quote.textContent = '“The only limit is the one you accept.”';
      var meta = document.createElement('div');
      meta.className = 'ss-head-meta';
      meta.innerHTML = '<strong id="desktopHeaderDay">Winter Arc</strong><small id="desktopHeaderClock"></small>';
      header.insertBefore(quote, nav);
      header.insertBefore(meta, nav);
    }
    if (actions) {
      actions.innerHTML = '<button class="pill-btn ss-icon-btn" type="button" data-action="data" title="Open save export and import" aria-label="Open data vault">⇧</button><button class="pill-btn ss-icon-btn" type="button" data-action="settings" title="Open settings" aria-label="Open settings">⚙</button>';
    }
  }
  var appStatus = document.getElementById('pwaStatus'); if (appStatus) appStatus.textContent = 'WINDOWS DESKTOP';
  var appNote = document.querySelector('#pwaStatus + .metric-note'); if (appNote) appNote.textContent = 'Tauri desktop shell';
  if (typeof renderAchievements === 'function') renderAchievements();
  if (typeof window.switchSystemScreen === 'function') window.switchSystemScreen('home');
  renderDesktopDashboard();
  setInterval(function () {
    var clock = document.getElementById('desktopHeaderClock');
    if (clock) clock.textContent = new Date().toLocaleString([], { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    var timerDisplay = document.getElementById('timerDisplay');
    if (timerDisplay) setText('desktopFocusTime', timerDisplay.textContent);
  }, 1000);
})();
