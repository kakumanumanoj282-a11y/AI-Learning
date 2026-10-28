/**
 * AI Engineer Learning OS - Core SPA Application Engine
 * State management, view router, modals, global search, and data binding.
 */

const App = {
  currentView: 'dashboard',
  state: {
    stages: (typeof window !== 'undefined' && window.STATIC_STAGES) ? window.STATIC_STAGES : [],
    topics: (typeof window !== 'undefined' && window.STATIC_TOPICS) ? window.STATIC_TOPICS : [],
    progress: null,
    recommendation: null,
    revisions: null
  },

  async init() {
    this.setupTheme();
    this.setupNavigation();
    this.setupGlobalSearch();
    this.setupShortcuts();

    await this.refreshGlobalState();
    this.navigate('dashboard');
  },

  async refreshGlobalState() {
    try {
      const [roadmapData, progressData, recData, revData] = await Promise.all([
        API.getRoadmap(),
        API.getProgress(),
        API.getRecommendation(),
        API.getRevisions()
      ]);

      this.state.stages = roadmapData.stages;
      this.state.topics = roadmapData.topics;
      this.state.progress = progressData;
      this.state.recommendation = recData;
      this.state.revisions = revData;

      // Update revision badges
      const revBadge = document.getElementById('header-rev-count');
      if (revBadge) {
        const revCount = (revData.counts?.due_today_count || 0) + (revData.counts?.needs_revision_count || 0);
        revBadge.textContent = revCount;
        revBadge.style.display = revCount > 0 ? 'inline-block' : 'none';
      }
    } catch (err) {
      console.error('[App] State initialization error:', err);
      this.showToast('Connecting to local storage database...');
    }
  },

  navigate(viewId, params = {}) {
    this.currentView = viewId;

    // Update active nav item
    document.querySelectorAll('.header-nav .nav-btn').forEach(item => {
      item.classList.toggle('active', item.getAttribute('data-view') === viewId);
    });

    // Hide all view panels
    document.querySelectorAll('.view-panel').forEach(panel => {
      panel.classList.remove('active');
    });

    // Show target view panel
    const targetPanel = document.getElementById(`view-${viewId}`);
    if (targetPanel) {
      targetPanel.classList.add('active');
      this.renderView(viewId, targetPanel, params);
    }

    // Scroll to top
    const scrollArea = document.querySelector('.content-scroll-area');
    if (scrollArea) scrollArea.scrollTop = 0;
  },

  renderView(viewId, container, params) {
    switch (viewId) {
      case 'dashboard':
        this.renderDashboard(container);
        break;
      case 'roadmap':
        RoadmapView.render(container, this.state);
        break;
      case 'learn':
        const topicId = params.topicId || this.state.recommendation?.recommended_topic?.id || 'py_syntax';
        LessonView.render(container, topicId, this.state);
        break;
      case 'topics':
        this.renderTopicsDirectory(container);
        break;
      case 'upload':
        UploadView.render(container, this.state);
        break;
      case 'practice':
        PracticeView.render(container, this.state);
        break;
      case 'projects':
        ProjectsView.render(container, this.state);
        break;
      case 'revision':
        this.renderRevisionCenter(container);
        break;
      case 'analytics':
        this.renderAnalytics(container);
        break;
      case 'settings':
        this.renderSettings(container);
        break;
      default:
        this.renderDashboard(container);
    }
  },

  openTopicLesson(topicId) {
    let cleanId = topicId;
    let anchor = null;
    if (cleanId && cleanId.includes('#')) {
      const parts = cleanId.split('#');
      cleanId = parts[0];
      anchor = parts[1];
    }
    this.navigate('learn', { topicId: cleanId, anchor: anchor });
  },

  /* =========================================================================
     1. DASHBOARD VIEW (User-Friendly, Engaging, Clear & Beautiful)
     ========================================================================= */
  renderDashboard(container) {
    try {
      const stages = (this.state.stages && this.state.stages.length > 0)
        ? this.state.stages
        : (window.STATIC_STAGES || []);
      const topics = (this.state.topics && this.state.topics.length > 0)
        ? this.state.topics
        : (window.STATIC_TOPICS || []);
      const progress = this.state.progress || {};
      const recommendation = this.state.recommendation || {};
      const progressMap = progress?.topics_progress || {};

      const stats = progress?.stats || {
        total_topics: topics.length,
        mastered: 0,
        in_progress: 0,
        needs_revision: 0,
        not_started: topics.length,
        completion_percentage: 0,
        last_studied_id: null
      };

      const rec = recommendation?.recommended_topic || topics[0] || {
        id: 'py_syntax',
        stage_id: 1,
        stage_name: 'Programming Foundations',
        title: 'Python Syntax and Variables',
        difficulty: 'Beginner',
        estimated_hours: 3,
        importance: 'The fundamental building block of all AI engineering code. Python is the lingua franca of machine learning.',
        what_you_will_do: 'Write clean, idiomatic Python scripts, declare variables with explicit types, and execute your first AI scripts.'
      };
      const lastStudied = topics.find(t => t.id === stats.last_studied_id) || null;

      // Current learning stage: earliest stage with unmastered topics
      let currentStage = stages[0] || { id: 1, name: 'Programming Foundations' };
      for (const st of stages) {
        const stTopics = topics.filter(t => t.stage_id === st.id);
        const allMastered = stTopics.length > 0 && stTopics.every(t => progressMap[t.id]?.status === 'mastered');
        if (!allMastered) {
          currentStage = st;
          break;
        }
      }

      // Pending topics list (unmastered topics)
      const pendingTopics = topics.filter(t => {
        const p = progressMap[t.id]?.status;
        return p !== 'mastered';
      });

      let html = `
        <!-- A. Welcome Banner & Overall Progress -->
        <div class="dash-welcome-card">
          <div class="dash-header-row">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span class="badge" style="background: rgba(76, 141, 255, 0.15); color: var(--ac); font-weight: 700;">AI LEARNING OS</span>
                <span style="font-size: 0.78rem; color: var(--mu);">Personal Engineering Mentor</span>
              </div>
              <h1 style="color: #fff; font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em;">Welcome back, kakumanu-manoj</h1>
              <p style="color: var(--tx-dim); font-size: 0.92rem; margin-top: 4px;">
                Goal: <strong style="color: var(--cy);">Become an AI Engineer</strong> &bull; Active Milestone: <strong style="color: #fff;">Stage ${currentStage.id} &mdash; ${currentStage.name}</strong>
              </p>
            </div>
            <div style="text-align: right; min-width: 160px;">
              <div style="font-size: 0.72rem; color: var(--mu); text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Roadmap Progress</div>
              <div style="font-size: 2.2rem; font-weight: 800; font-family: var(--font-mono); color: var(--ac); line-height: 1.1;">
                ${stats.completion_percentage}%
              </div>
              <div style="font-size: 0.78rem; color: var(--mu); margin-top: 2px;">${stats.mastered} of ${stats.total_topics} Mastered</div>
            </div>
          </div>

          <div class="progress-bar-wrap">
            <div class="progress-bar">
              <i class="progress-bar-fill" style="width: ${Math.max(stats.completion_percentage, 2)}%;"></i>
            </div>
          </div>

          <!-- 4-Stat Metric Boxes -->
          <div class="stat-grid">
            <div class="stat-box" style="border-left: 3px solid var(--gn);">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="color: var(--gn);">${stats.mastered}</b>
                <span style="font-size: 1.2rem;">🎓</span>
              </div>
              <span>Mastered Topics</span>
              <small style="color: var(--mu); font-size: 0.7rem; margin-top: 4px;">Verified by practice & quizzes</small>
            </div>
            <div class="stat-box" style="border-left: 3px solid var(--bl);">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="color: var(--bl);">${stats.in_progress}</b>
                <span style="font-size: 1.2rem;">⚡</span>
              </div>
              <span>In Progress</span>
              <small style="color: var(--mu); font-size: 0.7rem; margin-top: 4px;">Active lessons & code</small>
            </div>
            <div class="stat-box" style="border-left: 3px solid var(--gr);">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="color: var(--tx-dim);">${stats.not_started}</b>
                <span style="font-size: 1.2rem;">⏳</span>
              </div>
              <span>Pending in Roadmap</span>
              <small style="color: var(--mu); font-size: 0.7rem; margin-top: 4px;">Upcoming learning modules</small>
            </div>
            <div class="stat-box" style="border-left: 3px solid var(--am);">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <b style="color: var(--am);">${stats.needs_revision}</b>
                <span style="font-size: 1.2rem;">🔄</span>
              </div>
              <span>Needs Revision</span>
              <small style="color: var(--mu); font-size: 0.7rem; margin-top: 4px;">Spaced repetition queue</small>
            </div>
          </div>

          <div style="font-size: 0.82rem; color: var(--mu); display: flex; justify-content: space-between; flex-wrap: wrap; gap: 10px; border-top: 1px solid var(--bd); padding-top: 14px; margin-top: 6px;">
            <span>Last studied: <strong style="color: var(--tx);">${lastStudied ? lastStudied.title : 'None yet (Start below)'}</strong></span>
            <span>Recommended next: <strong style="color: #c084fc;">${rec.title}</strong></span>
          </div>
        </div>

        <!-- Interactive 12-Stage Milestones Stepper -->
        <div class="card" style="padding: 18px 22px; margin-bottom: 22px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; flex-wrap: wrap; gap: 8px;">
            <div>
              <span style="font-size: 0.72rem; font-weight: 700; color: var(--mu); text-transform: uppercase; letter-spacing: 0.05em;">
                Your 12-Stage AI Engineering Pathway
              </span>
              <p style="font-size: 0.8rem; color: var(--tx-dim); margin-top: 2px;">Click any stage to browse and filter lessons</p>
            </div>
            <button class="btn btn-outline btn-sm" onclick="App.navigate('roadmap')" style="font-size: 0.78rem; padding: 4px 10px;">
              View Connected Visual Graph →
            </button>
          </div>
          <div class="stage-stepper">
            ${stages.map((st, i) => {
              const icons = ["⚡", "📐", "📊", "🤖", "🧠", "🔮", "💬", "🔍", "🦾", "🚀", "📈", "🛡️"];
              const stTopics = topics.filter(t => t.stage_id === st.id);
              const mCount = stTopics.filter(t => progressMap[t.id]?.status === 'mastered').length;
              const isCur = (st.id === currentStage.id);

              return `
                <div class="stage-step-pill ${isCur ? 'current-step' : ''}" onclick="App.topicsFilterState.stage='${st.id}'; App.navigate('topics');" title="Click to view Stage ${st.id} topics">
                  <span style="font-size: 1.1rem;">${icons[i] || '•'}</span>
                  <div>
                    <div style="font-weight: 700; font-size: 0.82rem; color: ${isCur ? 'var(--ac)' : '#fff'};">
                      Stage ${st.id}
                    </div>
                    <div style="font-size: 0.68rem; color: var(--mu);">
                      ${mCount}/${stTopics.length} done
                    </div>
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>

        <!-- B. Continue Learning Hero Card (Next Recommended Topic) -->
        <div class="continue-learning-card">
          <div class="tag-row">
            <span class="badge badge-recommended">★ RECOMMENDED NEXT TOPIC</span>
            <span class="tag">Stage ${rec.stage_id}: ${rec.stage_name || 'Programming Foundations'}</span>
            <span class="tag">${rec.difficulty}</span>
            <span class="tag">~${rec.estimated_hours || 3} Hours</span>
            <span class="badge badge-${(rec.status || 'not_started').replace('_', '-')}">${(rec.status || 'Not Started').replace('_', ' ')}</span>
          </div>

          <h2 class="continue-title">${rec.title}</h2>
          <p style="color: var(--tx); font-size: 0.95rem; line-height: 1.6; max-width: 900px; margin-bottom: 14px;">
            ${rec.importance}
          </p>

          <div style="background: var(--sf-card); border: 1px solid var(--bd); border-radius: var(--radius-md); padding: 14px 18px; margin-bottom: 18px; font-size: 0.86rem; display: flex; flex-direction: column; gap: 8px;">
            <div><strong style="color: var(--mu);">What you will be able to do:</strong> <span style="color: var(--tx);">${rec.what_you_will_do}</span></div>
            <div><strong style="color: var(--mu);">Prerequisites:</strong> <span style="color: var(--gn);">${(rec.prerequisites && rec.prerequisites.length > 0) ? `✓ ${rec.prerequisites.length} prerequisites met` : '✓ No prerequisites needed &mdash; foundational entry point'}</span></div>
          </div>

          <div class="tag-row" style="margin-bottom: 0;">
            <button class="btn btn-primary" onclick="App.openTopicLesson('${rec.id}')">
              Continue Learning →
            </button>
            <button class="btn btn-secondary" onclick="App.toggleWhyNext()">
              Why This Topic Next?
            </button>
            <button class="btn btn-secondary" onclick="App.showPrerequisitesModal('${rec.id}')">
              Review Prerequisites
            </button>
          </div>

          <!-- Inline Toggleable Explanation -->
          <div id="dash-why-next" style="display: none;" class="why-box">
            <p><strong style="color: #c084fc;">Prerequisite Recommendation Rationale:</strong></p>
            <p style="margin-top: 4px; color: var(--tx);">${recommendation?.reason || 'All prerequisites are satisfied. This is the optimal next foundational step in your roadmap.'}</p>
            <p style="margin-top: 8px; color: var(--mu); font-size: 0.82rem;">
              💡 <em>Mastering this lesson unlocks downstream Machine Learning, Neural Network, and Large Language Model architectures.</em>
            </p>
          </div>
        </div>

        <!-- Quick Learning Actions -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-bottom: 22px;">
          <div class="card" onclick="App.navigate('roadmap')" style="cursor: pointer; padding: 16px; border-left: 3px solid var(--pu);">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">🗺️</div>
            <strong style="color: #fff; font-size: 0.95rem;">Interactive Roadmap</strong>
            <p style="color: var(--mu); font-size: 0.78rem; margin-top: 4px;">Explore all 12 stages with curved bezier connection arrows.</p>
          </div>
          <div class="card" onclick="App.navigate('upload')" style="cursor: pointer; padding: 16px; border-left: 3px solid var(--cy);">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">📂</div>
            <strong style="color: #fff; font-size: 0.95rem;">Upload Study Notes</strong>
            <p style="color: var(--mu); font-size: 0.78rem; margin-top: 4px;">Scan PDF/Markdown notes to match learned topics and find gaps.</p>
          </div>
          <div class="card" onclick="App.navigate('practice')" style="cursor: pointer; padding: 16px; border-left: 3px solid var(--am);">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">🎯</div>
            <strong style="color: #fff; font-size: 0.95rem;">Practice & Quizzes</strong>
            <p style="color: var(--mu); font-size: 0.78rem; margin-top: 4px;">Take interactive knowledge checks to earn verified mastery.</p>
          </div>
          <div class="card" onclick="App.navigate('projects')" style="cursor: pointer; padding: 16px; border-left: 3px solid var(--gn);">
            <div style="font-size: 1.4rem; margin-bottom: 6px;">💻</div>
            <strong style="color: #fff; font-size: 0.95rem;">Hands-on Projects</strong>
            <p style="color: var(--mu); font-size: 0.78rem; margin-top: 4px;">Build calculators, classifiers, RAG bots, and autonomous agents.</p>
          </div>
        </div>

        <!-- C. Pending Topics Section with Search and Filters -->
        <div class="card">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
            <div>
              <h2 style="font-size: 1.15rem; font-weight: 700; color: #fff;">Pending Topics in Roadmap (${pendingTopics.length})</h2>
              <p style="font-size: 0.82rem; color: var(--mu);">Topics ready or upcoming in your AI Engineering journey</p>
            </div>
            <div style="display: flex; gap: 8px; flex-wrap: wrap;">
              <input type="text" id="pending-search-input" placeholder="Search pending topics..." style="width: 200px;">
              <select id="pending-stage-filter">
                <option value="all">All Stages</option>
                ${stages.map(s => `<option value="${s.id}">Stage ${s.id}: ${s.name}</option>`).join('')}
              </select>
              <select id="pending-diff-filter">
                <option value="all">All Levels</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>
          </div>

          <div id="pending-topics-list-container">
            ${this.renderPendingRows(pendingTopics)}
          </div>
        </div>
      `;

      container.innerHTML = html;
      this.attachDashboardListeners(container);
    } catch (err) {
      console.error('[Dashboard Error]', err);
      container.innerHTML = `
        <div class="card" style="padding: 30px; text-align: center; border-left: 4px solid var(--accent-rose);">
          <h2 style="color: #fff; margin-bottom: 10px;">Dashboard Loading</h2>
          <p style="color: var(--mu); margin-bottom: 16px;">We encountered an issue preparing the dashboard view. Click below to reload.</p>
          <button class="btn btn-primary" onclick="App.init()">Reload Dashboard</button>
        </div>
      `;
    }
  },

  renderPendingRows(pendingList) {
    const { topics, progress } = this.state;
    const progressMap = progress?.topics_progress || {};

    if (pendingList.length === 0) {
      return `<div style="text-align: center; color: var(--gn); padding: 30px; font-size: 0.9rem;">All selected roadmap topics mastered!</div>`;
    }

    return pendingList.slice(0, 15).map((topic, idx) => {
      const p = progressMap[topic.id] || { status: 'not_started' };
      const missing = (topic.prerequisites || []).filter(pid => {
        return progressMap[pid]?.status !== 'mastered';
      });

      const missingNames = missing.map(pid => {
        const pt = topics.find(t => t.id === pid);
        return pt ? pt.title : pid;
      });

      return `
        <div class="item-card" onclick="App.openTopicLesson('${topic.id}')">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 4px;">
            <div style="display: flex; align-items: center; gap: 8px;">
              <strong style="color: #fff; font-size: 0.95rem;">${topic.title}</strong>
              <span class="badge badge-${p.status.replace('_', '-')}">${p.status.replace('_', ' ')}</span>
              <span class="tag">Stage ${topic.stage_id}</span>
              <span class="tag">${topic.difficulty}</span>
              <span class="tag" style="font-family: var(--font-mono);">order ${idx + 1}</span>
            </div>
            <button class="btn btn-outline btn-sm" onclick="event.stopPropagation(); App.openTopicLesson('${topic.id}')">
              Learn →
            </button>
          </div>

          <div style="font-size: 0.8rem; color: var(--mu);">
            ${topic.importance}
            ${missing.length > 0 
              ? `<span style="color: var(--am); margin-left: 6px;">Missing prerequisites: ${missingNames.join(', ')}</span>` 
              : `<span style="color: var(--gn); margin-left: 6px;">Prerequisites met &bull; Ready to learn</span>`}
          </div>
        </div>
      `;
    }).join('');
  },

  toggleWhyNext() {
    const box = document.getElementById('dash-why-next');
    if (box) {
      box.style.display = box.style.display === 'none' ? 'block' : 'none';
    }
  },

  attachDashboardListeners(container) {
    const searchInput = container.querySelector('#pending-search-input');
    const stageFilter = container.querySelector('#pending-stage-filter');
    const diffFilter = container.querySelector('#pending-diff-filter');
    const listContainer = container.querySelector('#pending-topics-list-container');

    const updateFilter = () => {
      const q = (searchInput?.value || '').toLowerCase().trim();
      const sVal = stageFilter?.value || 'all';
      const dVal = diffFilter?.value || 'all';

      const filtered = this.state.topics.filter(t => {
        const pStatus = this.state.progress?.topics_progress?.[t.id]?.status;
        if (pStatus === 'mastered') return false;
        if (sVal !== 'all' && t.stage_id !== parseInt(sVal)) return false;
        if (dVal !== 'all' && !t.difficulty.includes(dVal)) return false;
        if (q && !(t.title + ' ' + t.importance).toLowerCase().includes(q)) return false;
        return true;
      });

      if (listContainer) {
        listContainer.innerHTML = this.renderPendingRows(filtered);
      }
    };

    if (searchInput) searchInput.addEventListener('input', updateFilter);
    if (stageFilter) stageFilter.addEventListener('change', updateFilter);
    if (diffFilter) diffFilter.addEventListener('change', updateFilter);
  },

  /* =========================================================================
     3. MY TOPICS DIRECTORY VIEW (Visually Engaging, Grid Cards & Filter Chips)
     ========================================================================= */
  topicsFilterState: { stage: 'all', status: 'all', diff: 'all', search: '', viewMode: 'grid' },

  renderTopicsDirectory(container) {
    const { stages, topics, progress, recommendation } = this.state;
    const progressMap = progress?.topics_progress || {};
    const recommendedId = recommendation?.recommended_topic?.id;
    const fs = this.topicsFilterState;

    // Filter topics
    const filtered = topics.filter(t => {
      const p = progressMap[t.id] || { status: 'not_started' };
      if (fs.stage !== 'all' && t.stage_id !== parseInt(fs.stage)) return false;
      if (fs.status !== 'all' && p.status !== fs.status) return false;
      if (fs.diff !== 'all' && !t.difficulty.toLowerCase().includes(fs.diff.toLowerCase())) return false;
      if (fs.search && !(t.title + ' ' + (t.importance || '')).toLowerCase().includes(fs.search.toLowerCase())) return false;
      return true;
    });

    const stageIcons = ["⚡", "📐", "📊", "🤖", "🧠", "🔮", "💬", "🔍", "🦾", "🚀", "📈", "🛡️"];

    let html = `
      <div style="margin-bottom: 22px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 14px; margin-bottom: 14px;">
          <div>
            <h1 style="font-size: 1.65rem; font-weight: 800; color: #fff; letter-spacing: -0.02em;">My Topics & Knowledge Base</h1>
            <p style="color: var(--mu); font-size: 0.88rem; margin-top: 3px;">
              Master ${topics.length} industry-standard AI Engineering concepts at your own pace.
            </p>
          </div>

          <div style="display: flex; align-items: center; gap: 10px;">
            <input type="text" id="topics-search-box" value="${fs.search}" placeholder="Search any topic or concept..." style="width: 220px;">
            <div style="display: flex; background: var(--sf); border: 1px solid var(--bd); border-radius: var(--radius-md); overflow: hidden;">
              <button class="btn btn-sm ${fs.viewMode === 'grid' ? 'btn-primary' : 'btn-outline'}" id="btn-toggle-grid" style="border: none; border-radius: 0;">⊞ Grid</button>
              <button class="btn btn-sm ${fs.viewMode === 'table' ? 'btn-primary' : 'btn-outline'}" id="btn-toggle-table" style="border: none; border-radius: 0;">☰ Table</button>
            </div>
          </div>
        </div>

        <!-- Horizontal Scrollable Stage Filter Chips with Icons -->
        <div class="filter-chip-bar" id="stage-filter-chips">
          <button class="filter-chip ${fs.stage === 'all' ? 'active' : ''}" data-stage="all">All Stages (${topics.length})</button>
          ${stages.map((st, i) => `
            <button class="filter-chip ${fs.stage == st.id ? 'active' : ''}" data-stage="${st.id}">
              ${stageIcons[i] || '•'} Stage ${st.id}: ${st.name.split(' ')[0]}
            </button>
          `).join('')}
        </div>

        <!-- Status Filter Chips -->
        <div class="filter-chip-bar" style="margin-bottom: 20px;">
          <button class="filter-chip ${fs.status === 'all' ? 'active' : ''}" data-status="all">All Statuses</button>
          <button class="filter-chip ${fs.status === 'not_started' ? 'active' : ''}" data-status="not_started">⚪ Not Started</button>
          <button class="filter-chip ${fs.status === 'in_progress' ? 'active' : ''}" data-status="in_progress">🔵 In Progress</button>
          <button class="filter-chip ${fs.status === 'needs_revision' ? 'active' : ''}" data-status="needs_revision">🟠 Needs Revision</button>
          <button class="filter-chip ${fs.status === 'mastered' ? 'active' : ''}" data-status="mastered">🟢 Mastered</button>
        </div>
      </div>

      <!-- Topics Content (Grid or Table) -->
      ${fs.viewMode === 'grid' ? `
        <div class="topics-visual-grid" id="topics-grid-container">
          ${filtered.length === 0 ? `
            <div class="card" style="grid-column: 1 / -1; text-align: center; color: var(--mu); padding: 40px;">
              No topics match your current filters. Try selecting "All Stages" or clearing the search.
            </div>
          ` : filtered.map(t => {
            const p = progressMap[t.id] || { status: 'not_started', confidence_rating: 1 };
            const isRec = (t.id === recommendedId);
            const icon = stageIcons[(t.stage_id - 1) % stageIcons.length] || '✦';

            return `
              <div class="topic-visual-card ${isRec ? 'recommended-card' : ''}" onclick="App.openTopicLesson('${t.id}')">
                <div>
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span class="badge" style="background: var(--sf-card); color: var(--ac); border: 1px solid var(--bd);">
                      ${icon} Stage ${t.stage_id}
                    </span>
                    <span class="badge badge-${p.status.replace('_', '-')}">${p.status.replace('_', ' ')}</span>
                  </div>

                  <h3 style="color: #fff; font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; line-height: 1.35;">
                    ${t.title}
                  </h3>

                  <p style="color: var(--mu); font-size: 0.8rem; line-height: 1.45; margin-bottom: 14px; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;">
                    ${t.importance || t.what_you_will_do}
                  </p>
                </div>

                <div style="border-top: 1px solid var(--bd); padding-top: 12px; margin-top: 6px; display: flex; justify-content: space-between; align-items: center;">
                  <div style="display: flex; align-items: center; gap: 4px;" title="Confidence Rating">
                    <span style="font-size: 0.72rem; color: var(--mu); margin-right: 4px;">Conf:</span>
                    ${[1, 2, 3, 4, 5].map(star => `
                      <span style="font-size: 0.8rem; color: ${star <= (p.confidence_rating || 1) ? 'var(--am)' : 'var(--bd)'};">★</span>
                    `).join('')}
                  </div>

                  <button class="btn btn-primary btn-sm" onclick="event.stopPropagation(); App.openTopicLesson('${t.id}')">
                    Learn →
                  </button>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      ` : `
        <!-- Compact Table View -->
        <div class="data-table-wrapper">
          <table class="data-table">
            <thead>
              <tr>
                <th>Topic</th>
                <th>Stage</th>
                <th>Difficulty</th>
                <th>Status</th>
                <th>Confidence</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              ${filtered.map(t => {
                const p = progressMap[t.id] || { status: 'not_started', confidence_rating: 1 };
                return `
                  <tr>
                    <td>
                      <div style="font-weight: 700; color: #fff;">${t.title}</div>
                      <div style="font-size: 0.74rem; color: var(--mu);">${t.what_you_will_do}</div>
                    </td>
                    <td><span class="badge" style="background: var(--sf); color: var(--ac);">Stage ${t.stage_id}</span></td>
                    <td><span class="tag">${t.difficulty}</span></td>
                    <td><span class="badge badge-${p.status.replace('_', '-')}">${p.status.replace('_', ' ')}</span></td>
                    <td><span style="font-family: var(--font-mono); color: var(--ac);">${p.confidence_rating || 1}/5</span></td>
                    <td>
                      <button class="btn btn-outline btn-sm" onclick="App.openTopicLesson('${t.id}')">
                        Learn →
                      </button>
                    </td>
                  </tr>
                `;
              }).join('')}
            </tbody>
          </table>
        </div>
      `}
    `;

    container.innerHTML = html;
    this.attachTopicsDirectoryListeners(container);
  },

  attachTopicsDirectoryListeners(container) {
    const fs = this.topicsFilterState;

    // Search Box
    const searchBox = container.querySelector('#topics-search-box');
    if (searchBox) {
      searchBox.addEventListener('input', (e) => {
        fs.search = e.target.value;
        this.renderTopicsDirectory(container);
      });
    }

    // View Mode Toggle
    const gridBtn = container.querySelector('#btn-toggle-grid');
    const tableBtn = container.querySelector('#btn-toggle-table');
    if (gridBtn) gridBtn.addEventListener('click', () => { fs.viewMode = 'grid'; this.renderTopicsDirectory(container); });
    if (tableBtn) tableBtn.addEventListener('click', () => { fs.viewMode = 'table'; this.renderTopicsDirectory(container); });

    // Stage Filter Chips
    container.querySelectorAll('#stage-filter-chips .filter-chip').forEach(chip => {
      chip.addEventListener('click', () => {
        fs.stage = chip.getAttribute('data-stage');
        this.renderTopicsDirectory(container);
      });
    });

    // Status Filter Chips
    container.querySelectorAll('.filter-chip[data-status]').forEach(chip => {
      chip.addEventListener('click', () => {
        fs.status = chip.getAttribute('data-status');
        this.renderTopicsDirectory(container);
      });
    });
  },

  /* =========================================================================
     8. REVISION CENTER VIEW (Section 11)
     ========================================================================= */
  renderRevisionCenter(container) {
    const rev = Object.assign({
      due_today: [],
      overdue: [],
      needs_revision: [],
      weak_concepts: [],
      recently_mastered: []
    }, this.state.revisions);

    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Revision & Spaced Repetition Center</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Reinforce decay-prone concepts using transparent spaced review intervals (1, 3, 7, 14, and 30 days).
        </p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px;">
        <!-- Needs Revision Section -->
        <div class="card" style="border-left: 4px solid var(--accent-amber);">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24;">HIGH PRIORITY</span>
              <h2 class="card-title" style="margin-top: 4px;">Flagged for Revision (${rev.needs_revision.length})</h2>
            </div>
          </div>
          ${rev.needs_revision.length === 0 ? `
            <p style="color: var(--text-dim); font-size: 0.85rem;">No topics currently flagged for revision.</p>
          ` : `
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${rev.needs_revision.map(t => `
                <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card-subtle); padding: 10px 14px; border-radius: var(--radius-sm);">
                  <div>
                    <div style="font-weight: 600; font-size: 0.88rem; color: #fff;">${t.title}</div>
                    <div style="font-size: 0.72rem; color: var(--text-muted);">Confidence: ${t.confidence_rating}/5</div>
                  </div>
                  <button class="btn btn-outline btn-sm" onclick="App.openTopicLesson('${t.topic_id}')">Revise →</button>
                </div>
              `).join('')}
            </div>
          `}
        </div>

        <!-- Weak Concepts Section -->
        <div class="card" style="border-left: 4px solid var(--accent-rose);">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(244, 63, 94, 0.15); color: #fb7185;">WEAK PERFORMANCE</span>
              <h2 class="card-title" style="margin-top: 4px;">Low Confidence & Failed Quizzes (${rev.weak_concepts.length})</h2>
            </div>
          </div>
          ${rev.weak_concepts.length === 0 ? `
            <p style="color: var(--text-dim); font-size: 0.85rem;">No weak concepts detected. All active topics have solid confidence.</p>
          ` : `
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${rev.weak_concepts.map(t => `
                <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card-subtle); padding: 10px 14px; border-radius: var(--radius-sm);">
                  <div>
                    <div style="font-weight: 600; font-size: 0.88rem; color: #fff;">${t.title}</div>
                    <div style="font-size: 0.72rem; color: var(--accent-rose);">${t.weak_reason}</div>
                  </div>
                  <button class="btn btn-outline btn-sm" onclick="App.openTopicLesson('${t.topic_id}#part8-quiz')">Test Now →</button>
                </div>
              `).join('')}
            </div>
          `}
        </div>

        <!-- Overdue Review Topics -->
        <div class="card" style="border-left: 4px solid var(--accent-cyan);">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">SPACED REPETITION</span>
              <h2 class="card-title" style="margin-top: 4px;">Due Today / Overdue (${rev.overdue.length + rev.due_today.length})</h2>
            </div>
          </div>
          ${(rev.overdue.length + rev.due_today.length) === 0 ? `
            <p style="color: var(--text-dim); font-size: 0.85rem;">All scheduled reviews are up to date.</p>
          ` : `
            <div style="display: flex; flex-direction: column; gap: 8px;">
              ${rev.overdue.map(t => `
                <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card-subtle); padding: 10px 14px; border-radius: var(--radius-sm);">
                  <div>
                    <div style="font-weight: 600; font-size: 0.88rem; color: #fff;">${t.title}</div>
                    <div style="font-size: 0.72rem; color: var(--accent-amber);">${t.days_overdue} days overdue</div>
                  </div>
                  <button class="btn btn-outline btn-sm" onclick="App.openTopicLesson('${t.topic_id}')">Review →</button>
                </div>
              `).join('')}
            </div>
          `}
        </div>
      </div>
    `;

    container.innerHTML = html;
  },

  /* =========================================================================
     9. PROGRESS ANALYTICS VIEW
     ========================================================================= */
  renderAnalytics(container) {
    const { stages, topics, progress } = this.state;
    const progressMap = progress?.topics_progress || {};
    const stats = progress?.stats || { mastered: 0, in_progress: 0, needs_revision: 0, not_started: 0 };

    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Progress Analytics & Mastery Breakdown</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Empirical measurements of roadmap coverage, quiz passing rates, and stage completions.
        </p>
      </div>

      <!-- Stage Mastery Progress Bars -->
      <div class="card" style="margin-bottom: 24px; padding: 24px;">
        <h2 class="card-title" style="margin-bottom: 18px;">12-Stage Mastery Completion</h2>
        <div style="display: flex; flex-direction: column; gap: 14px;">
          ${stages.map(st => {
            const stTopics = topics.filter(t => t.stage_id === st.id);
            const mastered = stTopics.filter(t => progressMap[t.id]?.status === 'mastered').length;
            const inProg = stTopics.filter(t => progressMap[t.id]?.status === 'in_progress').length;
            const percent = Math.round((mastered / stTopics.length) * 100);

            return `
              <div>
                <div style="display: flex; justify-content: space-between; font-size: 0.82rem; margin-bottom: 4px;">
                  <span style="font-weight: 700; color: #fff;">Stage ${st.id}: ${st.name}</span>
                  <span style="font-family: var(--font-mono); color: var(--text-dim);">${mastered} / ${stTopics.length} (${percent}%)</span>
                </div>
                <div style="width: 100%; height: 8px; background: var(--bg-card-subtle); border-radius: 999px; overflow: hidden;">
                  <div style="width: ${percent}%; height: 100%; background: linear-gradient(90deg, var(--accent-blue), var(--accent-cyan)); border-radius: 999px; transition: width 0.3s ease;"></div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      </div>
    `;

    container.innerHTML = html;
  },

  /* =========================================================================
     10. SETTINGS & EXPORT VIEW
     ========================================================================= */
  renderSettings(container) {
    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Settings & Data Backup</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Export and import your complete learning state, manage persistent storage, and view runtime configurations.
        </p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 20px;">
        <!-- Export / Import Card -->
        <div class="card" style="padding: 24px;">
          <h2 class="card-title" style="margin-bottom: 6px;">Backup & Portability</h2>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 18px;">
            Export all topic progress, personal notes, quiz logs, and project links as a portable JSON file.
          </p>

          <div style="display: flex; flex-direction: column; gap: 12px;">
            <button class="btn btn-primary" id="btn-export-backup">
              Export Progress Backup (.json)
            </button>

            <div style="border-top: 1px solid var(--border-subtle); padding-top: 16px; margin-top: 4px;">
              <label style="font-size: 0.75rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase; display: block; margin-bottom: 6px;">
                Restore from JSON Backup
              </label>
              <textarea id="import-json-textarea" rows="4" style="width: 100%; background: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 8px; color: var(--text-main); font-family: var(--font-mono); font-size: 0.75rem;" placeholder="Paste exported JSON payload here..."></textarea>
              <button class="btn btn-secondary btn-sm" id="btn-import-backup" style="margin-top: 8px;">
                Import & Restore Progress
              </button>
            </div>
          </div>
        </div>

        <!-- Reset Data Card -->
        <div class="card" style="padding: 24px; border: 1px solid rgba(244, 63, 94, 0.3);">
          <h2 class="card-title" style="color: var(--accent-rose); margin-bottom: 6px;">Danger Zone: Reset State</h2>
          <p style="font-size: 0.85rem; color: var(--text-muted); margin-bottom: 18px;">
            Clears all evidence logs, quiz scores, project progress, and resets all topics to 'Not Started'.
          </p>
          <button class="btn btn-outline" id="btn-reset-all-data" style="color: var(--accent-rose); border-color: var(--accent-rose);">
            Reset All Learning Progress
          </button>
        </div>
      </div>
    `;

    container.innerHTML = html;

    // Export Handler
    const exportBtn = container.querySelector('#btn-export-backup');
    if (exportBtn) {
      exportBtn.addEventListener('click', async () => {
        try {
          const data = await API.exportData();
          const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `ai_engineer_learning_os_backup_${new Date().toISOString().split('T')[0]}.json`;
          a.click();
          URL.revokeObjectURL(url);
          App.showToast('Downloaded learning state backup.');
        } catch (err) {
          alert(`Export failed: ${err.message}`);
        }
      });
    }

    // Import Handler
    const importBtn = container.querySelector('#btn-import-backup');
    if (importBtn) {
      importBtn.addEventListener('click', async () => {
        const text = container.querySelector('#import-json-textarea').value.trim();
        if (!text) {
          alert('Please paste a valid JSON backup payload first.');
          return;
        }
        try {
          const parsed = JSON.parse(text);
          const res = await API.importData(parsed);
          App.showToast(`Restored ${res.imported_topics} topic records.`);
          await App.refreshGlobalState();
          App.navigate('dashboard');
        } catch (err) {
          alert(`Import failed: ${err.message}`);
        }
      });
    }

    // Reset Handler
    const resetBtn = container.querySelector('#btn-reset-all-data');
    if (resetBtn) {
      resetBtn.addEventListener('click', async () => {
        if (confirm('Are you sure you want to reset all learning progress? This action cannot be undone.')) {
          await API.resetData();
          App.showToast('All learning data reset to initial state.');
          await App.refreshGlobalState();
          App.navigate('dashboard');
        }
      });
    }
  },

  /* =========================================================================
     MODALS: Why This Topic Next? & Review Prerequisites
     ========================================================================= */
  showWhyNextModal(topicId) {
    const rec = this.state.recommendation;
    if (!rec) return;

    const modalOverlay = document.getElementById('global-modal-overlay');
    const modalContent = document.getElementById('global-modal-content');

    const satList = (rec.satisfied_prerequisites || []).map(p => {
      return `<li><strong style="color: var(--accent-green);">${p.title}</strong> (Stage ${p.stage_id} - ${p.status})</li>`;
    }).join('');

    const unlockList = (rec.downstream_unlocked || []).map(u => {
      return `<li><strong style="color: var(--accent-violet);">${u.title}</strong> (Stage ${u.stage_id})</li>`;
    }).join('');

    const altList = (rec.alternative_choices || []).map(alt => {
      return `
        <div style="background: var(--bg-card-subtle); padding: 10px 14px; border-radius: var(--radius-sm); margin-top: 6px;">
          <div style="font-weight: 700; color: #fff;">${alt.title} (Stage ${alt.stage_id})</div>
          <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">${alt.reason}</div>
          <button class="btn btn-outline btn-sm" style="margin-top: 6px;" onclick="App.closeModal(); App.openTopicLesson('${alt.id}')">Switch to this topic →</button>
        </div>
      `;
    }).join('');

    modalContent.innerHTML = `
      <button class="modal-close-btn" onclick="App.closeModal()">✕</button>
      <span class="badge badge-recommended" style="margin-bottom: 8px;">RECOMMENDATION RATIONALE</span>
      <h2 style="font-size: 1.4rem; font-weight: 800; color: #fff; margin-bottom: 12px;">
        Why '${rec.recommended_topic.title}' is Next
      </h2>

      <div style="background: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-violet); margin-bottom: 18px; font-size: 0.92rem; line-height: 1.6; color: var(--text-main);">
        ${rec.reason}
      </div>

      <div style="margin-bottom: 16px;">
        <h4 style="font-size: 0.78rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Satisfied Prerequisites:</h4>
        <ul style="margin: 6px 0 0 18px; font-size: 0.85rem; color: var(--text-muted);">
          ${satList || '<li>No prerequisites required (Foundational topic)</li>'}
        </ul>
      </div>

      <div style="margin-bottom: 18px;">
        <h4 style="font-size: 0.78rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Concepts This Unlocks:</h4>
        <ul style="margin: 6px 0 0 18px; font-size: 0.85rem; color: var(--text-muted);">
          ${unlockList || '<li>Direct stepping stone to subsequent stage topics</li>'}
        </ul>
      </div>

      ${altList ? `
        <div style="border-top: 1px solid var(--border-subtle); padding-top: 14px; margin-top: 16px;">
          <h4 style="font-size: 0.78rem; font-weight: 700; color: var(--text-dim); text-transform: uppercase;">Valid Alternatives Right Now:</h4>
          ${altList}
        </div>
      ` : ''}

      <div style="margin-top: 20px; display: flex; justify-content: flex-end; gap: 10px;">
        <button class="btn btn-secondary" onclick="App.closeModal()">Close</button>
        <button class="btn btn-primary" onclick="App.closeModal(); App.openTopicLesson('${rec.recommended_topic.id}')">Start Learning →</button>
      </div>
    `;

    modalOverlay.classList.add('active');
  },

  async showPrerequisitesModal(topicId) {
    const modalOverlay = document.getElementById('global-modal-overlay');
    const modalContent = document.getElementById('global-modal-content');

    modalContent.innerHTML = `<div style="text-align: center; padding: 30px;">Loading prerequisite tree...</div>`;
    modalOverlay.classList.add('active');

    try {
      const tree = await API.getPrerequisitesTree(topicId);
      const chain = tree.prerequisites_chain || [];

      modalContent.innerHTML = `
        <button class="modal-close-btn" onclick="App.closeModal()">✕</button>
        <span class="badge badge-in-progress" style="margin-bottom: 8px;">DEPENDENCY TREE</span>
        <h2 style="font-size: 1.35rem; font-weight: 800; color: #fff; margin-bottom: 6px;">
          Prerequisites for ${tree.target_topic.title}
        </h2>
        <p style="font-size: 0.82rem; color: var(--text-muted); margin-bottom: 18px;">
          ${chain.length === 0 ? 'This topic has no prerequisites. You can begin immediately!' : `Requires ${chain.length} foundational concept${chain.length > 1 ? 's' : ''}.`}
        </p>

        <div style="display: flex; flex-direction: column; gap: 10px; max-height: 400px; overflow-y: auto;">
          ${chain.map((c, idx) => `
            <div style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-card-subtle); border-left: 3px solid ${c.is_satisfied ? 'var(--accent-green)' : 'var(--accent-amber)'}; padding: 12px 14px; border-radius: var(--radius-sm);">
              <div>
                <div style="font-weight: 700; font-size: 0.88rem; color: #fff;">${idx + 1}. ${c.title}</div>
                <div style="font-size: 0.74rem; color: var(--text-dim); margin-top: 2px;">${c.stage_name} | Status: <strong style="color: ${c.is_satisfied ? 'var(--accent-green)' : 'var(--accent-amber)'}">${c.status}</strong></div>
              </div>
              <button class="btn btn-outline btn-sm" onclick="App.closeModal(); App.openTopicLesson('${c.id}')">
                Open →
              </button>
            </div>
          `).join('')}
        </div>

        <div style="margin-top: 20px; display: flex; justify-content: flex-end;">
          <button class="btn btn-secondary" onclick="App.closeModal()">Close</button>
        </div>
      `;
    } catch (err) {
      modalContent.innerHTML = `<div style="color: var(--accent-rose);">Error: ${err.message}</div>`;
    }
  },

  closeModal() {
    const modalOverlay = document.getElementById('global-modal-overlay');
    if (modalOverlay) modalOverlay.classList.remove('active');
  },

  /* =========================================================================
     GLOBAL SEARCH (with '/' Shortcut)
     ========================================================================= */
  setupGlobalSearch() {
    const searchInput = document.getElementById('global-search-input');
    const resultsBox = document.getElementById('search-results-box');

    if (!searchInput || !resultsBox) return;

    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase().trim();
      if (!q) {
        resultsBox.classList.remove('active');
        return;
      }

      const matches = this.state.topics.filter(t => {
        return t.title.toLowerCase().includes(q) ||
               t.importance.toLowerCase().includes(q) ||
               (t.key_concepts || []).some(k => k.toLowerCase().includes(q));
      }).slice(0, 6);

      if (matches.length === 0) {
        resultsBox.innerHTML = `<div style="padding: 16px; color: var(--text-dim); font-size: 0.85rem;">No topics matching "${q}"</div>`;
      } else {
        resultsBox.innerHTML = matches.map(m => `
          <div class="search-item" onclick="App.openTopicLesson('${m.id}'); document.getElementById('search-results-box').classList.remove('active');">
            <div style="font-weight: 700; font-size: 0.88rem; color: #fff;">${m.title}</div>
            <div style="font-size: 0.72rem; color: var(--text-muted); margin-top: 2px;">Stage ${m.stage_id} - ${m.difficulty}</div>
          </div>
        `).join('');
      }

      resultsBox.classList.add('active');
    });

    document.addEventListener('click', (e) => {
      if (!searchInput.contains(e.target) && !resultsBox.contains(e.target)) {
        resultsBox.classList.remove('active');
      }
    });
  },

  setupShortcuts() {
    document.addEventListener('keydown', (e) => {
      if (e.key === '/' && document.activeElement.tagName !== 'INPUT' && document.activeElement.tagName !== 'TEXTAREA') {
        e.preventDefault();
        const searchInput = document.getElementById('global-search-input');
        if (searchInput) searchInput.focus();
      }
      if (e.key === 'Escape') {
        this.closeModal();
        const resultsBox = document.getElementById('search-results-box');
        if (resultsBox) resultsBox.classList.remove('active');
      }
    });
  },

  setupTheme() {
    const btn = document.getElementById('theme-toggle-btn');
    if (btn) {
      btn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
        const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', nextTheme);
        App.showToast(`Switched to ${nextTheme} theme.`);
      });
    }
  },

  setupNavigation() {
    document.querySelectorAll('.header-nav .nav-btn').forEach(btn => {
      btn.addEventListener('click', () => {
        const view = btn.getAttribute('data-view');
        if (view) this.navigate(view);
      });
    });
  },

  showToast(message) {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerHTML = `<span style="color: var(--accent-cyan);">✦</span> <span>${message}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => toast.remove(), 200);
    }, 3200);
  }
};

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  App.init();
});

