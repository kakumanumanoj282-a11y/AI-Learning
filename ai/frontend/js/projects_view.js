/**
 * AI Engineer Learning OS - Hands-On Practical Projects View
 * Production-minded projects linked directly to roadmap stages with
 * problem statements, folder structures, starter code, and testing rubrics.
 */

const ProjectsView = {
  projectsList: [],

  async render(container, state) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px 0;">
        <div style="color: var(--accent-cyan); font-weight: 600;">Loading practical AI engineering projects...</div>
      </div>
    `;

    try {
      const data = await API.getProjects();
      this.projectsList = data.projects || [];
      this.renderContent(container, state);
    } catch (err) {
      container.innerHTML = `<div class="card" style="color: var(--accent-rose);">Failed to load projects: ${err.message}</div>`;
    }
  },

  renderContent(container, state) {
    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Hands-On Engineering Projects</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Theory without execution is ineffective. Build real deployable projects across each roadmap stage to anchor mastery.
        </p>
      </div>

      <div style="display: flex; flex-direction: column; gap: 24px;">
    `;

    this.projectsList.forEach(proj => {
      const isCompleted = proj.status === 'completed';
      const isInProgress = proj.status === 'in_progress';

      html += `
        <div class="card" style="border-left: 4px solid ${isCompleted ? 'var(--accent-green)' : (isInProgress ? 'var(--accent-blue)' : 'var(--border-subtle)')}; padding: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 14px; margin-bottom: 14px;">
            <div>
              <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                <span class="badge" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">Stage ${proj.stage_id}</span>
                <span class="badge" style="background: var(--bg-card-subtle); color: var(--accent-cyan);">${proj.difficulty}</span>
                <span class="badge badge-${proj.status.replace('_', '-')}">${proj.status.toUpperCase()}</span>
              </div>
              <h2 style="font-size: 1.3rem; font-weight: 800; color: #fff;">${proj.title}</h2>
              <p style="font-size: 0.88rem; color: var(--text-muted); margin-top: 4px; max-width: 850px;">${proj.description}</p>
            </div>

            <div style="display: flex; align-items: center; gap: 10px;">
              <select class="btn btn-secondary btn-sm proj-status-select" data-proj-id="${proj.id}">
                <option value="not_started" ${proj.status === 'not_started' ? 'selected' : ''}>Not Started</option>
                <option value="in_progress" ${proj.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                <option value="completed" ${proj.status === 'completed' ? 'selected' : ''}>Completed</option>
              </select>
            </div>
          </div>

          <!-- Project Details Accordion -->
          <div style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; margin-top: 14px;">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 14px; font-size: 0.84rem;">
              <div>
                <strong style="color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">Required Prerequisites:</strong>
                <div style="margin-top: 4px; display: flex; gap: 6px; flex-wrap: wrap;">
                  ${proj.prerequisites.map(pre => `<span class="badge" style="background: var(--bg-card); color: var(--accent-blue);">${pre}</span>`).join('')}
                </div>
              </div>

              <div>
                <strong style="color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">GitHub Repository URL:</strong>
                <input type="url" class="proj-github-input" data-proj-id="${proj.id}" value="${proj.github_url || ''}" placeholder="https://github.com/your-username/repo" style="width: 100%; margin-top: 4px; background: var(--bg-card); border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 6px 10px; color: var(--text-main); font-size: 0.8rem;">
              </div>
            </div>

            <div style="margin-top: 12px; display: flex; justify-content: flex-end;">
              <button class="btn btn-primary btn-sm btn-save-proj" data-proj-id="${proj.id}">
                Save Project State & Notes
              </button>
            </div>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
    this.attachEventListeners(container);
  },

  attachEventListeners(container) {
    container.querySelectorAll('.btn-save-proj').forEach(btn => {
      btn.addEventListener('click', async () => {
        const pid = btn.getAttribute('data-proj-id');
        const statusSelect = container.querySelector(`.proj-status-select[data-proj-id="${pid}"]`);
        const githubInput = container.querySelector(`.proj-github-input[data-proj-id="${pid}"]`);

        const newStatus = statusSelect ? statusSelect.value : 'not_started';
        const githubUrl = githubInput ? githubInput.value.trim() : '';

        try {
          btn.disabled = true;
          btn.textContent = 'Saving...';
          await API.updateProjectStatus({
            project_id: pid,
            status: newStatus,
            github_url: githubUrl,
            notes: `Updated on ${new Date().toLocaleDateString()}`
          });
          App.showToast(`Saved project: ${pid}`);
          await App.refreshGlobalState();
        } catch (err) {
          alert(`Failed to save project: ${err.message}`);
        } finally {
          btn.disabled = false;
          btn.textContent = 'Save Project State & Notes';
        }
      });
    });
  }
};

