/**
 * AI Engineer Learning OS - 9-Part Topic Lesson View
 * Strictly renders the 9 comprehensive parts specified in Section 8
 * with interactive SVG diagrams, runnable code examples, problem-solving, and knowledge checks.
 */

const LessonView = {
  currentTopicId: null,
  lessonData: null,
  activeDiagramStep: 0,

  async render(container, topicId, state) {
    let cleanId = topicId;
    let anchor = null;
    if (cleanId.includes('#')) {
      const parts = cleanId.split('#');
      cleanId = parts[0];
      anchor = parts[1];
    }
    this.currentTopicId = cleanId;
    container.innerHTML = `
      <div style="text-align: center; padding: 60px 0;">
        <div style="font-size: 1.1rem; color: var(--cy); font-weight: 600;">Loading structured lesson...</div>
        <p style="color: var(--mu); font-size: 0.85rem; margin-top: 6px;">Preparing visual diagrams, runnable code, and quizzes.</p>
      </div>
    `;

    try {
      const data = await API.getTopicLesson(cleanId);
      this.lessonData = data;
      this.renderContent(container, state);
      if (anchor) {
        setTimeout(() => {
          const el = document.getElementById(anchor);
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }, 100);
      }
    } catch (err) {
      container.innerHTML = `
        <div class="card" style="border-color: var(--accent-rose); padding: 30px; text-align: center;">
          <h2 style="color: var(--accent-rose);">Failed to load lesson</h2>
          <p style="color: var(--text-muted); margin: 10px 0 20px;">${err.message}</p>
          <button class="btn btn-secondary" onclick="App.navigate('roadmap')">← Return to Roadmap</button>
        </div>
      `;
    }
  },

  renderContent(container, state) {
    const { topic, stage, lesson } = this.lessonData;
    const progressMap = state?.progress?.topics_progress || {};
    const userProgress = progressMap[topic.id] || { status: 'not_started', confidence_rating: 1, personal_notes: '' };

    const p1 = lesson.part1_simple_explanation || {};
    const p2 = lesson.part2_analogy || {};
    const p3 = lesson.part3_visual_diagram || {};
    const p4 = lesson.part4_mechanism || [];
    const p5 = lesson.part5_code || {};
    const p6 = lesson.part6_when_to_use || {};
    const p7 = lesson.part7_problems_engineers_face || [];
    const p8 = lesson.part8_knowledge_check || {};

    let html = `
      <!-- Breadcrumb & Topic Header -->
      <div style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 8px; font-size: 0.8rem; color: var(--text-dim); margin-bottom: 8px;">
          <a href="#" onclick="event.preventDefault(); App.navigate('roadmap');" style="color: var(--text-muted); text-decoration: none;">Roadmap</a>
          <span>/</span>
          <span>Stage ${stage.id}: ${stage.name}</span>
          <span>/</span>
          <span style="color: var(--accent-blue);">${topic.title}</span>
        </div>

        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 16px;">
          <div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
              <span class="badge badge-${userProgress.status.replace('_', '-')}">${userProgress.status.replace('_', ' ').toUpperCase()}</span>
              <span class="badge" style="background: var(--bg-card-subtle); color: var(--accent-cyan); font-family: var(--font-mono);">${topic.difficulty}</span>
              <span class="badge" style="background: var(--bg-card-subtle); color: var(--text-dim); font-family: var(--font-mono);">${topic.estimated_hours} Hours Est.</span>
            </div>
            <h1 style="font-size: 2rem; font-weight: 800; letter-spacing: -0.02em; color: #fff;">${topic.title}</h1>
            <p style="font-size: 0.95rem; color: var(--text-muted); max-width: 900px; margin-top: 6px;">${topic.what_you_will_do}</p>
          </div>

          <div style="display: flex; gap: 10px; align-items: center;">
            <button class="btn btn-secondary btn-sm" onclick="App.showPrerequisitesModal('${topic.id}')">
              Review Prerequisites (${topic.prerequisites.length})
            </button>
            <button class="btn btn-primary btn-sm" onclick="document.getElementById('part9-completion').scrollIntoView({behavior: 'smooth'})">
              Update Status & Notes ↓
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation Tabs across 9 Parts -->
      <div style="display: flex; gap: 8px; overflow-x: auto; padding-bottom: 12px; margin-bottom: 24px; border-bottom: 1px solid var(--border-subtle);">
        <a href="#part1-explanation" class="btn btn-outline btn-sm">1. Simple Explanation</a>
        <a href="#part2-analogy" class="btn btn-outline btn-sm">2. Real-World Analogy</a>
        <a href="#part3-visual" class="btn btn-outline btn-sm">3. Visual Diagram</a>
        <a href="#part4-mechanism" class="btn btn-outline btn-sm">4. Step-by-Step Mechanism</a>
        <a href="#part5-code" class="btn btn-outline btn-sm">5. Code Demonstration</a>
        <a href="#part6-when" class="btn btn-outline btn-sm">6. When & Why to Use</a>
        <a href="#part7-problems" class="btn btn-outline btn-sm">7. Problems Engineers Face</a>
        <a href="#part8-quiz" class="btn btn-outline btn-sm">8. Knowledge Check</a>
        <a href="#part9-completion" class="btn btn-outline btn-sm">9. Completion & Evidence</a>
      </div>

      <div style="display: flex; flex-direction: column; gap: 32px;">

        <!-- PART 1: Simple Explanation -->
        <section id="part1-explanation" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">PART 1</span>
              <h2 class="card-title" style="margin-top: 4px;">Simple English Explanation</h2>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 18px; margin-bottom: 20px;">
            <div style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-blue);">
              <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-blue); text-transform: uppercase;">What It Is</div>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 4px;">${p1.what_it_is || ''}</p>
            </div>
            <div style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-violet);">
              <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-violet); text-transform: uppercase;">Why It Exists</div>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 4px;">${p1.why_it_exists || ''}</p>
            </div>
            <div style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-cyan);">
              <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Problem It Solves</div>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 4px;">${p1.problem_it_solves || ''}</p>
            </div>
            <div style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-green);">
              <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-green); text-transform: uppercase;">Where Used in Real AI</div>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 4px;">${p1.real_world_use || ''}</p>
            </div>
          </div>

          ${p1.glossary && p1.glossary.length > 0 ? `
            <div style="border-top: 1px solid var(--border-subtle); padding-top: 16px;">
              <h3 style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 10px;">Progressive Technical Glossary</h3>
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${p1.glossary.map(g => `
                  <div style="font-size: 0.85rem;">
                    <strong style="color: var(--accent-cyan); font-family: var(--font-mono);">${g.term}:</strong>
                    <span style="color: var(--text-muted); margin-left: 6px;">${g.definition}</span>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}
        </section>

        <!-- PART 2: Real-World Analogy -->
        <section id="part2-analogy" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(139, 92, 246, 0.15); color: #c084fc;">PART 2</span>
              <h2 class="card-title" style="margin-top: 4px;">Real-World Analogy</h2>
            </div>
          </div>
          <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.08), rgba(59, 130, 246, 0.05)); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: var(--radius-lg); padding: 22px;">
            <h3 style="font-size: 1.1rem; font-weight: 700; color: #fff; margin-bottom: 8px;">${p2.analogy_title || 'Mental Model'}</h3>
            <p style="font-size: 0.92rem; color: var(--text-main); line-height: 1.65; margin-bottom: 16px;">${p2.story || ''}</p>
            <div style="background-color: var(--bg-card); border-left: 3px solid var(--accent-amber); padding: 12px 16px; border-radius: var(--radius-sm);">
              <span style="font-size: 0.72rem; font-weight: 700; color: var(--accent-amber); text-transform: uppercase;">Clear Technical Difference:</span>
              <p style="font-size: 0.85rem; color: var(--text-muted); margin-top: 4px;">${p2.technical_difference || ''}</p>
            </div>
          </div>
        </section>

        <!-- PART 3: Visual Explanation (Interactive Diagram) -->
        <section id="part3-visual" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(6, 182, 212, 0.15); color: #22d3ee;">PART 3</span>
              <h2 class="card-title" style="margin-top: 4px;">Interactive Visual Diagram</h2>
              <div class="card-subtitle">${p3.title || 'Data Flow Architecture'}</div>
            </div>
          </div>

          <div class="interactive-diagram-box">
            <!-- Dynamic SVG Rendering -->
            <svg id="lesson-dynamic-svg" width="100%" height="220" viewBox="0 0 800 220" style="max-width: 900px; margin: 0 auto; display: block;">
              <defs>
                <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#64748b" />
                </marker>
                <marker id="arrow-active" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#3b82f6" />
                </marker>
              </defs>

              ${this.generateDiagramSvg(p3.nodes || [])}
            </svg>

            <!-- Step by Step Revealer / Data Flow Player -->
            ${p3.flow_steps && p3.flow_steps.length > 0 ? `
              <div style="margin-top: 20px; text-align: left; background-color: var(--bg-card); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
                  <span style="font-size: 0.75rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Data Movement Step-by-Step</span>
                  <div style="display: flex; gap: 8px;">
                    <button class="btn btn-secondary btn-sm" id="btn-prev-diagram-step">← Prev</button>
                    <button class="btn btn-primary btn-sm" id="btn-next-diagram-step">Next Step →</button>
                  </div>
                </div>
                <div id="diagram-active-step-text" style="font-size: 0.88rem; color: var(--text-main); font-weight: 500; min-height: 40px; display: flex; align-items: center;">
                  ${p3.flow_steps[0]}
                </div>
              </div>
            ` : ''}

            <!-- Misconceptions Box -->
            ${p3.misconceptions && p3.misconceptions.length > 0 ? `
              <div style="margin-top: 14px; text-align: left; background-color: rgba(245, 158, 11, 0.08); border-left: 3px solid var(--accent-amber); padding: 12px 16px; border-radius: var(--radius-sm);">
                <div style="font-size: 0.72rem; font-weight: 700; color: var(--accent-amber); text-transform: uppercase;">Common Architecture Misconceptions</div>
                ${p3.misconceptions.map(m => `<p style="font-size: 0.82rem; color: var(--text-main); margin-top: 4px;">${m}</p>`).join('')}
              </div>
            ` : ''}
          </div>
        </section>

        <!-- PART 4: Step-by-Step Mechanism -->
        <section id="part4-mechanism" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">PART 4</span>
              <h2 class="card-title" style="margin-top: 4px;">Step-by-Step Technical Mechanism</h2>
            </div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 12px;">
            ${p4.map((step, idx) => `
              <div style="display: flex; align-items: flex-start; gap: 14px; background-color: var(--bg-card-subtle); padding: 14px 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
                <span style="width: 28px; height: 28px; border-radius: 50%; background-color: var(--accent-blue-subtle); color: var(--accent-blue); font-weight: 800; font-family: var(--font-mono); font-size: 0.85rem; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                  ${idx + 1}
                </span>
                <span style="font-size: 0.9rem; color: var(--text-main); padding-top: 3px; line-height: 1.5;">${step}</span>
              </div>
            `).join('')}
          </div>
        </section>

        <!-- PART 5: Code Demonstration -->
        <section id="part5-code" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa;">PART 5</span>
              <h2 class="card-title" style="margin-top: 4px;">Runnable Code Demonstrations</h2>
            </div>
          </div>

          ${p5.beginner_example ? `
            <div style="margin-bottom: 22px;">
              <h3 style="font-size: 0.95rem; font-weight: 700; color: var(--accent-cyan);">${p5.beginner_example.title}</h3>
              <div class="code-container">
                <div class="code-header">
                  <span>Python 3.15</span>
                  <span>Beginner Walkthrough</span>
                </div>
                <pre class="code-pre"><code>${this.escapeHtml(p5.beginner_example.code)}</code></pre>
                <div class="code-output">
                  <strong style="color: var(--text-dim); font-size: 0.72rem; text-transform: uppercase;">Expected Output:</strong>
                  <div style="margin-top: 4px;">${this.escapeHtml(p5.beginner_example.expected_output)}</div>
                </div>
              </div>
              <p style="font-size: 0.84rem; color: var(--text-muted); margin-top: 6px;">${p5.beginner_example.explanation}</p>
            </div>
          ` : ''}

          ${p5.production_example ? `
            <div style="margin-bottom: 20px;">
              <h3 style="font-size: 0.95rem; font-weight: 700; color: var(--accent-violet);">${p5.production_example.title}</h3>
              <div class="code-container">
                <div class="code-header">
                  <span>Python 3.15</span>
                  <span>Production-Grade Architecture</span>
                </div>
                <pre class="code-pre"><code>${this.escapeHtml(p5.production_example.code)}</code></pre>
                <div class="code-output">
                  <strong style="color: var(--text-dim); font-size: 0.72rem; text-transform: uppercase;">Expected Output:</strong>
                  <div style="margin-top: 4px;">${this.escapeHtml(p5.production_example.expected_output)}</div>
                </div>
              </div>
              <p style="font-size: 0.84rem; color: var(--text-muted); margin-top: 6px;">${p5.production_example.explanation}</p>
            </div>
          ` : ''}

          ${p5.common_errors && p5.common_errors.length > 0 ? `
            <div style="background-color: var(--bg-card-subtle); padding: 14px 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); margin-top: 14px;">
              <h4 style="font-size: 0.75rem; font-weight: 700; color: var(--accent-rose); text-transform: uppercase; margin-bottom: 8px;">Common Syntax & Runtime Errors</h4>
              ${p5.common_errors.map(err => `
                <div style="margin-bottom: 8px; font-size: 0.82rem;">
                  <code style="color: var(--accent-rose); font-family: var(--font-mono);">${err.error}</code>
                  <div style="color: var(--text-muted); margin-top: 2px;">Fix: ${err.fix}</div>
                </div>
              `).join('')}
            </div>
          ` : ''}
        </section>

        <!-- PART 6: When and Why to Use It -->
        <section id="part6-when" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(139, 92, 246, 0.15); color: #c084fc;">PART 6</span>
              <h2 class="card-title" style="margin-top: 4px;">When & Why to Use It</h2>
            </div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 18px;">
            <div style="background-color: var(--bg-card-subtle); padding: 18px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-green);">
              <h3 style="font-size: 0.82rem; font-weight: 700; color: var(--accent-green); text-transform: uppercase;">Ideal Use Cases</h3>
              <ul style="margin: 10px 0 0 18px; font-size: 0.88rem; color: var(--text-main); display: flex; flex-direction: column; gap: 6px;">
                ${(p6.use_cases || []).map(u => `<li>${u}</li>`).join('')}
              </ul>
            </div>

            <div style="background-color: var(--bg-card-subtle); padding: 18px; border-radius: var(--radius-md); border-left: 3px solid var(--accent-amber);">
              <h3 style="font-size: 0.82rem; font-weight: 700; color: var(--accent-amber); text-transform: uppercase;">When It Is Unnecessary</h3>
              <ul style="margin: 10px 0 0 18px; font-size: 0.88rem; color: var(--text-main); display: flex; flex-direction: column; gap: 6px;">
                ${(p6.unnecessary_cases || []).map(u => `<li>${u}</li>`).join('')}
              </ul>
            </div>
          </div>
          <div style="margin-top: 16px; background-color: var(--bg-card-subtle); padding: 14px 18px; border-radius: var(--radius-md);">
            <strong style="color: var(--text-muted); font-size: 0.82rem; text-transform: uppercase;">Cost & Complexity Trade-Offs:</strong>
            <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 4px;">${p6.tradeoffs || ''}</p>
          </div>
        </section>

        <!-- PART 7: Problems Engineers Face -->
        <section id="part7-problems" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(244, 63, 94, 0.15); color: #fb7185;">PART 7</span>
              <h2 class="card-title" style="margin-top: 4px;">Problems Engineers Face</h2>
              <div class="card-subtitle">Realistic troubleshooting playbooks and failure diagnosis</div>
            </div>
          </div>
          <div style="display: flex; flex-direction: column; gap: 16px;">
            ${p7.map(item => `
              <div style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
                <h3 style="font-size: 1rem; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
                  <span style="color: var(--accent-rose);">⚠️</span> ${item.problem}
                </h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; margin-top: 12px; font-size: 0.84rem;">
                  <div>
                    <strong style="color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">Symptoms:</strong>
                    <div style="color: var(--text-main); margin-top: 2px;">${item.symptoms}</div>
                  </div>
                  <div>
                    <strong style="color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">Likely Causes:</strong>
                    <div style="color: var(--text-main); margin-top: 2px;">${item.causes}</div>
                  </div>
                  <div>
                    <strong style="color: var(--text-dim); text-transform: uppercase; font-size: 0.7rem;">How to Diagnose:</strong>
                    <div style="color: var(--text-main); margin-top: 2px;">${item.diagnosis}</div>
                  </div>
                </div>
                <div style="margin-top: 14px; background: rgba(16, 185, 129, 0.08); border-left: 3px solid var(--accent-green); padding: 10px 14px; border-radius: var(--radius-sm); font-size: 0.84rem;">
                  <strong style="color: var(--accent-green); font-size: 0.72rem; text-transform: uppercase;">Step-by-Step Fix:</strong>
                  <div style="color: var(--text-main); margin-top: 2px;">${item.fix}</div>
                  <div style="color: var(--text-muted); font-size: 0.78rem; margin-top: 4px;">Prevention: ${item.prevention}</div>
                </div>
              </div>
            `).join('')}
          </div>
        </section>

        <!-- PART 8: Knowledge Check (Interactive) -->
        <section id="part8-quiz" class="card">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24;">PART 8</span>
              <h2 class="card-title" style="margin-top: 4px;">Knowledge Check & Quizzes</h2>
              <div class="card-subtitle">3 Beginner, 2 Application, 1 Debugging Scenario & 1 Practical Exercise</div>
            </div>
            <button class="btn btn-primary btn-sm" id="btn-submit-lesson-quiz">
              Submit Quiz & Verify Score
            </button>
          </div>

          <!-- Beginner Questions -->
          <h3 style="font-size: 0.85rem; font-weight: 700; color: var(--accent-blue); text-transform: uppercase; margin-bottom: 12px;">Beginner Questions</h3>
          <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
            ${(p8.beginner_questions || []).map((q, idx) => `
              <div class="quiz-question-box" data-qid="beg_${idx}" style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
                <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 10px; color: var(--text-main);">${idx + 1}. ${q.question}</div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  ${q.options.map((opt, oIdx) => `
                    <label style="display: flex; align-items: center; gap: 10px; padding: 8px 12px; background-color: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); cursor: pointer; font-size: 0.85rem;">
                      <input type="radio" name="q_beg_${idx}" value="${oIdx}">
                      <span>${opt}</span>
                    </label>
                  `).join('')}
                </div>
                <div class="quiz-feedback" id="feedback_beg_${idx}" style="display: none; margin-top: 10px; font-size: 0.82rem; padding: 8px 12px; border-radius: var(--radius-sm);"></div>
              </div>
            `).join('')}
          </div>

          <!-- Application Questions -->
          <h3 style="font-size: 0.85rem; font-weight: 700; color: var(--accent-violet); text-transform: uppercase; margin-bottom: 12px;">Application Questions</h3>
          <div style="display: flex; flex-direction: column; gap: 16px; margin-bottom: 24px;">
            ${(p8.application_questions || []).map((q, idx) => `
              <div class="quiz-question-box" data-qid="app_${idx}" style="background-color: var(--bg-card-subtle); padding: 16px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
                <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 10px; color: var(--text-main);">${idx + 1}. ${q.question}</div>
                <div style="display: flex; flex-direction: column; gap: 6px;">
                  ${q.options.map((opt, oIdx) => `
                    <label style="display: flex; align-items: center; gap: 10px; padding: 8px 12px; background-color: var(--bg-card); border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); cursor: pointer; font-size: 0.85rem;">
                      <input type="radio" name="q_app_${idx}" value="${oIdx}">
                      <span>${opt}</span>
                    </label>
                  `).join('')}
                </div>
                <div class="quiz-feedback" id="feedback_app_${idx}" style="display: none; margin-top: 10px; font-size: 0.82rem; padding: 8px 12px; border-radius: var(--radius-sm);"></div>
              </div>
            `).join('')}
          </div>

          <!-- Debugging Scenario -->
          ${p8.debugging_scenario ? `
            <div style="background-color: var(--bg-card-subtle); border-left: 3px solid var(--accent-cyan); padding: 18px; border-radius: var(--radius-md); margin-bottom: 20px;">
              <h3 style="font-size: 0.85rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase;">Debugging Scenario</h3>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 6px; line-height: 1.5;">${p8.debugging_scenario.scenario}</p>
              <div style="margin-top: 12px; display: flex; gap: 10px;">
                <button class="btn btn-secondary btn-sm" id="btn-toggle-debug-hint">Show Hint</button>
                <button class="btn btn-secondary btn-sm" id="btn-toggle-debug-sol">Show Solution</button>
              </div>
              <div id="debug-hint-box" style="display: none; margin-top: 10px; font-size: 0.82rem; color: var(--accent-amber);">
                💡 Hint: ${p8.debugging_scenario.hint}
              </div>
              <div id="debug-sol-box" style="display: none; margin-top: 10px; font-size: 0.84rem; background: var(--bg-card); padding: 12px; border-radius: var(--radius-sm); color: var(--accent-green);">
                ✅ Solution: ${p8.debugging_scenario.solution}
              </div>
            </div>
          ` : ''}

          <!-- Practical Exercise -->
          ${p8.practical_exercise ? `
            <div style="background-color: var(--bg-card-subtle); border-left: 3px solid var(--accent-green); padding: 18px; border-radius: var(--radius-md);">
              <h3 style="font-size: 0.85rem; font-weight: 700; color: var(--accent-green); text-transform: uppercase;">Short Practical Exercise</h3>
              <p style="font-size: 0.88rem; color: var(--text-main); margin-top: 6px;">${p8.practical_exercise.prompt}</p>
              <div class="code-container" style="margin-top: 10px;">
                <pre class="code-pre"><code>${this.escapeHtml(p8.practical_exercise.starter_code)}</code></pre>
              </div>
              <button class="btn btn-secondary btn-sm" id="btn-toggle-exercise-sol">Reveal Solution Code</button>
              <div id="exercise-sol-box" style="display: none; margin-top: 10px;">
                <div class="code-container">
                  <pre class="code-pre" style="color: #a7f3d0;"><code>${this.escapeHtml(p8.practical_exercise.solution_code)}</code></pre>
                </div>
              </div>
            </div>
          ` : ''}
        </section>

        <!-- PART 9: Completion & User Progress Update -->
        <section id="part9-completion" class="card" style="border: 2px solid var(--accent-blue);">
          <div class="card-header">
            <div>
              <span class="badge" style="background: rgba(59, 130, 246, 0.2); color: #60a5fa;">PART 9</span>
              <h2 class="card-title" style="margin-top: 4px;">Update Topic Status & Save Personal Notes</h2>
              <div class="card-subtitle">Mark as studied, adjust confidence rating, or flag for revision</div>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 20px;">
            <div>
              <label style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                Topic Learning Status
              </label>
              <select id="update-topic-status-select" class="btn btn-secondary" style="width: 100%; padding: 10px 14px; text-align: left;">
                <option value="not_started" ${userProgress.status === 'not_started' ? 'selected' : ''}>Not Started</option>
                <option value="in_progress" ${userProgress.status === 'in_progress' ? 'selected' : ''}>In Progress</option>
                <option value="needs_revision" ${userProgress.status === 'needs_revision' ? 'selected' : ''}>Needs Revision</option>
                <option value="mastered" ${userProgress.status === 'mastered' ? 'selected' : ''}>Mastered (Confirmed by Practice & Quiz)</option>
              </select>
            </div>

            <div>
              <label style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
                Confidence Rating: <span id="conf-val-display" style="color: var(--accent-blue);">${userProgress.confidence_rating || 1} / 5</span>
              </label>
              <input type="range" id="update-confidence-range" min="1" max="5" value="${userProgress.confidence_rating || 1}" style="width: 100%; margin-top: 10px; cursor: pointer;">
              <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: var(--text-dim); margin-top: 4px;">
                <span>1 - Shaky</span>
                <span>3 - Working</span>
                <span>5 - Mastered</span>
              </div>
            </div>
          </div>

          <div style="margin-bottom: 20px;">
            <label style="font-size: 0.78rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; display: block; margin-bottom: 6px;">
              Personal Study Notes & Key Takeaways
            </label>
            <textarea id="update-personal-notes-input" rows="4" style="width: 100%; background: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 12px; color: var(--text-main); font-family: inherit; font-size: 0.88rem; resize: vertical;" placeholder="Add your code snippets, mental models, or points to review later...">${userProgress.personal_notes || ''}</textarea>
          </div>

          <!-- Existing Evidence Log -->
          ${userProgress.evidence && userProgress.evidence.length > 0 ? `
            <div style="background-color: var(--bg-card-subtle); padding: 14px 18px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle); margin-bottom: 20px;">
              <h4 style="font-size: 0.75rem; font-weight: 700; color: var(--accent-cyan); text-transform: uppercase; margin-bottom: 8px;">Audit Evidence Trail (${userProgress.evidence.length} items)</h4>
              <div style="display: flex; flex-direction: column; gap: 6px; font-size: 0.8rem;">
                ${userProgress.evidence.map(ev => `
                  <div style="display: flex; justify-content: space-between; color: var(--text-muted);">
                    <span>✔ <strong style="color: var(--text-main);">${ev.type.replace('_', ' ')}</strong>: ${ev.source_ref}</span>
                    <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-dim);">${new Date(ev.created_at).toLocaleDateString()}</span>
                  </div>
                `).join('')}
              </div>
            </div>
          ` : ''}

          <div style="display: flex; gap: 12px; justify-content: flex-end; flex-wrap: wrap;">
            <button class="btn btn-secondary" onclick="App.navigate('roadmap')">← Back to Roadmap</button>
            <button class="btn btn-primary" id="btn-save-topic-progress">Save Progress & Evidence</button>
          </div>
        </section>

      </div>
    `;

    container.innerHTML = html;
    this.attachEventListeners(container, topic);
  },

  generateDiagramSvg(nodes) {
    if (!nodes || nodes.length === 0) return '';
    const nodeWidth = 160;
    const nodeHeight = 70;
    const spacing = 45;
    const startX = 20;
    const startY = 75;

    let svgHtml = '';
    nodes.forEach((node, i) => {
      const x = startX + i * (nodeWidth + spacing);
      const y = startY;

      // Draw connection arrow to next node
      if (i < nodes.length - 1) {
        const arrowStartX = x + nodeWidth;
        const arrowEndX = arrowStartX + spacing;
        svgHtml += `
          <line x1="${arrowStartX}" y1="${y + nodeHeight / 2}" x2="${arrowEndX - 5}" y2="${y + nodeHeight / 2}"
                stroke="#64748b" stroke-width="2" marker-end="url(#arrow)" />
        `;
      }

      // Draw Node Box
      svgHtml += `
        <g class="diagram-svg-node" id="svg-node-${i}" style="cursor: pointer;">
          <rect x="${x}" y="${y}" width="${nodeWidth}" height="${nodeHeight}" rx="8"
                fill="#111827" stroke="${node.color}" stroke-width="2" />
          <text x="${x + nodeWidth / 2}" y="${y + 28}" fill="#f8fafc" font-size="11" font-weight="700" text-anchor="middle" font-family="Plus Jakarta Sans">
            ${this.truncate(node.label, 22)}
          </text>
          <text x="${x + nodeWidth / 2}" y="${y + 48}" fill="#94a3b8" font-size="9" text-anchor="middle" font-family="Plus Jakarta Sans">
            ${this.truncate(node.desc, 26)}
          </text>
        </g>
      `;
    });

    return svgHtml;
  },

  truncate(str, max) {
    if (!str) return '';
    return str.length > max ? str.substring(0, max - 3) + '...' : str;
  },

  escapeHtml(str) {
    if (!str) return '';
    return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  },

  attachEventListeners(container, topic) {
    // Confidence slider display
    const confSlider = container.querySelector('#update-confidence-range');
    const confDisplay = container.querySelector('#conf-val-display');
    if (confSlider && confDisplay) {
      confSlider.addEventListener('input', (e) => {
        confDisplay.textContent = `${e.target.value} / 5`;
      });
    }

    // Save topic progress button
    const saveBtn = container.querySelector('#btn-save-topic-progress');
    if (saveBtn) {
      saveBtn.addEventListener('click', async () => {
        const newStatus = container.querySelector('#update-topic-status-select').value;
        const newConfidence = parseInt(container.querySelector('#update-confidence-range').value);
        const newNotes = container.querySelector('#update-personal-notes-input').value;

        try {
          saveBtn.disabled = true;
          saveBtn.textContent = 'Saving...';
          await API.updateTopicProgress({
            topic_id: topic.id,
            status: newStatus,
            confidence_rating: newConfidence,
            personal_notes: newNotes,
            mark_studied_now: true,
            evidence_type: newStatus === 'mastered' ? 'mastery_confirmed' : 'user_confirmed',
            evidence_ref: `Status set to ${newStatus}`
          });
          App.showToast(`Saved progress for ${topic.title}`);
          await App.refreshGlobalState();
          this.renderContent(container, App.state);
        } catch (err) {
          alert(`Error saving progress: ${err.message}`);
        } finally {
          saveBtn.disabled = false;
          saveBtn.textContent = 'Save Progress & Evidence';
        }
      });
    }

    // Diagram Step Player
    const steps = this.lessonData.lesson.part3_visual_diagram?.flow_steps || [];
    const prevBtn = container.querySelector('#btn-prev-diagram-step');
    const nextBtn = container.querySelector('#btn-next-diagram-step');
    const stepText = container.querySelector('#diagram-active-step-text');

    if (steps.length > 0 && prevBtn && nextBtn && stepText) {
      this.activeDiagramStep = 0;
      prevBtn.addEventListener('click', () => {
        if (this.activeDiagramStep > 0) {
          this.activeDiagramStep--;
          stepText.textContent = steps[this.activeDiagramStep];
        }
      });
      nextBtn.addEventListener('click', () => {
        if (this.activeDiagramStep < steps.length - 1) {
          this.activeDiagramStep++;
          stepText.textContent = steps[this.activeDiagramStep];
        }
      });
    }

    // Toggle hint and solutions
    const hintBtn = container.querySelector('#btn-toggle-debug-hint');
    const hintBox = container.querySelector('#debug-hint-box');
    if (hintBtn && hintBox) {
      hintBtn.addEventListener('click', () => {
        hintBox.style.display = hintBox.style.display === 'none' ? 'block' : 'none';
      });
    }

    const solBtn = container.querySelector('#btn-toggle-debug-sol');
    const solBox = container.querySelector('#debug-sol-box');
    if (solBtn && solBox) {
      solBtn.addEventListener('click', () => {
        solBox.style.display = solBox.style.display === 'none' ? 'block' : 'none';
      });
    }

    const exSolBtn = container.querySelector('#btn-toggle-exercise-sol');
    const exSolBox = container.querySelector('#exercise-sol-box');
    if (exSolBtn && exSolBox) {
      exSolBtn.addEventListener('click', () => {
        exSolBox.style.display = exSolBox.style.display === 'none' ? 'block' : 'none';
      });
    }

    // Quiz Submission Button
    const quizBtn = container.querySelector('#btn-submit-lesson-quiz');
    if (quizBtn) {
      quizBtn.addEventListener('click', async () => {
        const p8 = this.lessonData.lesson.part8_knowledge_check || {};
        const begQ = p8.beginner_questions || [];
        const appQ = p8.application_questions || [];
        let totalQuestions = begQ.length + appQ.length;
        let score = 0;

        // Evaluate Beginner
        begQ.forEach((q, idx) => {
          const selected = container.querySelector(`input[name="q_beg_${idx}"]:checked`);
          const fb = container.querySelector(`#feedback_beg_${idx}`);
          if (fb) {
            fb.style.display = 'block';
            if (selected && parseInt(selected.value) === q.correct_idx) {
              score++;
              fb.style.background = 'rgba(16, 185, 129, 0.15)';
              fb.style.color = '#34d399';
              fb.innerHTML = `<strong>Correct!</strong> ${q.explanation}`;
            } else {
              fb.style.background = 'rgba(244, 63, 94, 0.15)';
              fb.style.color = '#fb7185';
              fb.innerHTML = `<strong>Incorrect.</strong> Correct answer: "${q.options[q.correct_idx]}". ${q.explanation}`;
            }
          }
        });

        // Evaluate Application
        appQ.forEach((q, idx) => {
          const selected = container.querySelector(`input[name="q_app_${idx}"]:checked`);
          const fb = container.querySelector(`#feedback_app_${idx}`);
          if (fb) {
            fb.style.display = 'block';
            if (selected && parseInt(selected.value) === q.correct_idx) {
              score++;
              fb.style.background = 'rgba(16, 185, 129, 0.15)';
              fb.style.color = '#34d399';
              fb.innerHTML = `<strong>Correct!</strong> ${q.explanation}`;
            } else {
              fb.style.background = 'rgba(244, 63, 94, 0.15)';
              fb.style.color = '#fb7185';
              fb.innerHTML = `<strong>Incorrect.</strong> Correct answer: "${q.options[q.correct_idx]}". ${q.explanation}`;
            }
          }
        });

        // Submit to API
        try {
          const res = await API.submitQuiz({
            topic_id: topic.id,
            score: score,
            total_questions: totalQuestions
          });
          const percent = Math.round((score / totalQuestions) * 100);
          App.showToast(`Quiz Submitted: ${score}/${totalQuestions} (${percent}%) - ${res.passed ? 'PASSED' : 'NEEDS REVISION'}`);
          await App.refreshGlobalState();
        } catch (err) {
          alert(`Failed to save quiz result: ${err.message}`);
        }
      });
    }
  }
};

