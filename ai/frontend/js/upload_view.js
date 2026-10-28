/**
 * AI Engineer Learning OS - Document & Study Upload View
 * Drag-and-drop analyzer with honest parser fallback and 3-group confirmation review screen.
 */

const UploadView = {
  lastAnalysis: null,

  render(container, state) {
    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Upload & Analyze Study Materials</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Ingest notes, screenshots, research summaries, and PDFs. The analyzer maps concepts to the 12-stage roadmap
          and presents a review screen before any progress is modified.
        </p>
      </div>

      <!-- File Drop Zone -->
      <div class="card" style="margin-bottom: 24px; padding: 32px; text-align: center; border: 2px dashed var(--border-highlight);" id="upload-dropzone">
        <input type="file" id="upload-file-input" style="display: none;" accept=".txt,.md,.py,.json,.csv,.pdf,.png,.jpg,.jpeg">
        
        <div style="width: 52px; height: 52px; margin: 0 auto 16px; border-radius: 50%; background: var(--accent-blue-subtle); display: flex; align-items: center; justify-content: center; color: var(--accent-blue);">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="17 8 12 3 7 8"></polyline><line x1="12" y1="3" x2="12" y2="15"></line></svg>
        </div>

        <h3 style="font-size: 1.15rem; font-weight: 700; color: #fff; margin-bottom: 6px;">Drag and drop your study files here</h3>
        <p style="font-size: 0.85rem; color: var(--text-muted); max-width: 500px; margin: 0 auto 18px;">
          Supports Markdown, Python code, TXT notes, PDFs, and screenshots.
        </p>

        <div style="display: flex; gap: 12px; justify-content: center; align-items: center;">
          <button class="btn btn-primary" onclick="document.getElementById('upload-file-input').click()">
            Browse Files
          </button>
          <button class="btn btn-secondary" id="btn-load-sample-notes">
            Load Sample Notes
          </button>
        </div>

        <div id="upload-status-indicator" style="display: none; margin-top: 18px; font-size: 0.85rem; color: var(--accent-cyan);">
          Processing file and matching concepts against roadmap...
        </div>
      </div>

      <!-- Analysis & Review Screen Container -->
      <div id="upload-review-container">
        ${this.renderReviewSection(this.lastAnalysis)}
      </div>
    `;

    container.innerHTML = html;
    this.attachEventListeners(container);
  },

  renderReviewSection(data) {
    if (!data) {
      return `
        <div class="card" style="padding: 24px; text-align: center; color: var(--text-dim); font-size: 0.85rem;">
          No file analyzed yet. Upload study material or click "Load Sample Notes" above to begin.
        </div>
      `;
    }

    const analysis = data.analysis;
    const groupA = analysis.group_a_found || [];
    const groupB = analysis.group_b_already_learned || [];
    const groupC = analysis.group_c_missing_or_further_study || [];

    return `
      <div class="card" style="border: 2px solid var(--accent-blue); padding: 24px; margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px;">
          <div>
            <span class="badge badge-recommended">Analysis Review Screen</span>
            <h2 style="font-size: 1.3rem; font-weight: 800; color: #fff; margin-top: 4px;">
              Extracted from: ${data.filename}
            </h2>
            <div style="font-size: 0.78rem; color: var(--text-dim); margin-top: 2px;">
              Parser: ${data.parser_type} | Characters: ${analysis.text_length} | Detected Concepts: ${analysis.total_concepts_detected}
            </div>
          </div>

          <div style="display: flex; gap: 10px;">
            <button class="btn btn-primary" id="btn-confirm-upload-changes">
              Confirm & Save Progress Updates
            </button>
          </div>
        </div>

        ${data.diagnostics?.ocr_status ? `
          <div style="background: rgba(245, 158, 11, 0.08); border-left: 3px solid var(--accent-amber); padding: 10px 14px; border-radius: var(--radius-sm); font-size: 0.8rem; margin-bottom: 20px;">
            <strong style="color: var(--accent-amber);">Parser Transparency Note:</strong>
            ${data.diagnostics.ocr_status} ${data.diagnostics.note || ''}
          </div>
        ` : ''}

        <!-- 3 Mandated Groups Display -->
        <div style="display: flex; flex-direction: column; gap: 24px;">

          <!-- GROUP A: Topics Found in Material -->
          <div style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
              <div>
                <span class="badge" style="background: rgba(59, 130, 246, 0.15); color: #60a5fa; font-weight: 700;">GROUP A</span>
                <h3 style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-top: 2px;">
                  Topics Detected in Upload (${groupA.length})
                </h3>
              </div>
              <span style="font-size: 0.75rem; color: var(--text-dim);">Check items you wish to update in your progress</span>
            </div>

            ${groupA.length === 0 ? `
              <p style="color: var(--text-dim); font-size: 0.85rem;">No direct roadmap topic matches identified in this excerpt.</p>
            ` : `
              <div style="display: flex; flex-direction: column; gap: 10px;">
                ${groupA.map((t, idx) => `
                  <div style="display: flex; align-items: flex-start; justify-content: space-between; background: var(--bg-card); padding: 12px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle); flex-wrap: wrap; gap: 10px;">
                    <div style="display: flex; align-items: flex-start; gap: 12px;">
                      <input type="checkbox" class="upload-confirm-checkbox" data-topic-id="${t.topic_id}" checked style="margin-top: 4px; cursor: pointer;">
                      <div>
                        <div style="font-weight: 700; font-size: 0.92rem; color: #fff;">
                          ${t.title}
                          <span style="font-size: 0.72rem; color: var(--accent-cyan); font-weight: 500; margin-left: 8px;">Stage ${t.stage_id}</span>
                        </div>
                        <div style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
                          Matched: <span style="color: var(--text-main); font-family: var(--font-mono);">${t.matched_terms.join(', ')}</span>
                        </div>
                        ${t.context_snippet ? `
                          <div style="font-size: 0.75rem; color: var(--text-dim); margin-top: 4px; font-style: italic;">
                            "${t.context_snippet}"
                          </div>
                        ` : ''}
                      </div>
                    </div>

                    <div style="display: flex; align-items: center; gap: 10px;">
                      <select class="upload-status-select" data-topic-id="${t.topic_id}" style="background: var(--bg-card-subtle); border: 1px solid var(--border-subtle); color: var(--text-main); padding: 4px 8px; border-radius: var(--radius-sm); font-size: 0.78rem;">
                        <option value="in_progress">Set In Progress</option>
                        <option value="needs_revision">Set Needs Revision</option>
                        <option value="mastered">Set Mastered</option>
                      </select>
                      <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; font-family: var(--font-mono);">${t.match_score}% Match</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            `}
          </div>

          <!-- GROUP B: Topics Already Learned -->
          <div style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
            <div style="margin-bottom: 12px;">
              <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399; font-weight: 700;">GROUP B</span>
              <h3 style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-top: 2px;">
                Topics Already Recorded as Learned (${groupB.length})
              </h3>
            </div>

            ${groupB.length === 0 ? `
              <p style="color: var(--text-dim); font-size: 0.85rem;">None of the detected concepts have previously been marked as learned.</p>
            ` : `
              <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 10px;">
                ${groupB.map(t => `
                  <div style="background: var(--bg-card); padding: 10px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                    <div style="font-weight: 600; font-size: 0.86rem; color: var(--text-main);">${t.title}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px; font-size: 0.72rem;">
                      <span class="badge badge-${t.status.replace('_', '-')}">${t.status}</span>
                      <span style="color: var(--text-dim); font-family: var(--font-mono);">${t.confidence_rating}/5 Confidence</span>
                    </div>
                  </div>
                `).join('')}
              </div>
            `}
          </div>

          <!-- GROUP C: Missing or Requiring Further Study -->
          <div style="background-color: var(--bg-card-subtle); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px;">
            <div style="margin-bottom: 12px;">
              <span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24; font-weight: 700;">GROUP C</span>
              <h3 style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-top: 2px;">
                Topics That May Be Missing or Require Further Study (${groupC.length})
              </h3>
              <p style="font-size: 0.78rem; color: var(--text-muted); margin-top: 2px;">
                These foundational prerequisites are required for the uploaded material but have not yet been mastered.
              </p>
            </div>

            ${groupC.length === 0 ? `
              <p style="color: var(--text-dim); font-size: 0.85rem;">No prerequisite gaps detected! Your foundations fully support this material.</p>
            ` : `
              <div style="display: flex; flex-direction: column; gap: 8px;">
                ${groupC.map(t => `
                  <div style="display: flex; align-items: center; justify-content: space-between; background: var(--bg-card); padding: 10px 14px; border-radius: var(--radius-sm); border-left: 3px solid var(--accent-amber); flex-wrap: wrap; gap: 8px;">
                    <div>
                      <div style="font-weight: 600; font-size: 0.88rem; color: #fff;">
                        ${t.title}
                        <span style="font-size: 0.72rem; color: var(--text-dim); margin-left: 6px;">Stage ${t.stage_id}</span>
                      </div>
                      <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 2px;">${t.reason}</div>
                    </div>
                    <button class="btn btn-outline btn-sm" onclick="App.openTopicLesson('${t.topic_id}')">
                      Study Prerequisite →
                    </button>
                  </div>
                `).join('')}
              </div>
            `}
          </div>

        </div>
      </div>
    `;
  },

  attachEventListeners(container) {
    const fileInput = container.querySelector('#upload-file-input');
    const dropzone = container.querySelector('#upload-dropzone');
    const sampleBtn = container.querySelector('#btn-load-sample-notes');

    if (fileInput) {
      fileInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (file) {
          await this.processFile(file, container);
        }
      });
    }

    if (dropzone) {
      dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.style.borderColor = 'var(--accent-blue)';
      });
      dropzone.addEventListener('dragleave', () => {
        dropzone.style.borderColor = 'var(--border-highlight)';
      });
      dropzone.addEventListener('drop', async (e) => {
        e.preventDefault();
        dropzone.style.borderColor = 'var(--border-highlight)';
        const file = e.dataTransfer.files[0];
        if (file) {
          await this.processFile(file, container);
        }
      });
    }

    if (sampleBtn) {
      sampleBtn.addEventListener('click', async () => {
        const sampleText = `
# Comprehensive Machine Learning & Transformer Deep Dive
Today we reviewed:
- Python syntax and variables, type hints, and conditional loops.
- Mathematics for AI: Vectors and matrices, transpose operations, and dot products.
- Linear Regression, Mean Squared Error (MSE), and Gradient Descent weight updates: w = w - eta * grad.
- Transformers and Self-Attention mechanisms: Query, Key, and Value dot-product attention:
  Attention(Q, K, V) = softmax(QK^T / sqrt(d_k))V
- Prompt Engineering: few-shot exemplars and Chain-of-Thought (CoT).
        `;
        await this.analyzeContent(sampleText, 'sample_notes_ml_transformers.md', container);
      });
    }

    this.attachConfirmListener(container);
  },

  async processFile(file, container) {
    const status = container.querySelector('#upload-status-indicator');
    if (status) status.style.display = 'block';

    const reader = new FileReader();
    const ext = file.name.split('.').pop().toLowerCase();

    if (['png', 'jpg', 'jpeg', 'webp', 'pdf'].includes(ext)) {
      reader.onload = async () => {
        const base64 = reader.result.split(',')[1];
        await this.sendUploadPayload({ filename: file.name, base64_content: base64 }, container);
      };
      reader.readAsDataURL(file);
    } else {
      reader.onload = async () => {
        await this.analyzeContent(reader.result, file.name, container);
      };
      reader.readAsText(file);
    }
  },

  async analyzeContent(textContent, filename, container) {
    await this.sendUploadPayload({ filename, text_content: textContent }, container);
  },

  async sendUploadPayload(payload, container) {
    try {
      const result = await API.uploadStudyMaterial(payload);
      this.lastAnalysis = result;
      const reviewBox = container.querySelector('#upload-review-container');
      if (reviewBox) {
        reviewBox.innerHTML = this.renderReviewSection(this.lastAnalysis);
        this.attachConfirmListener(container);
        App.showToast(`Analyzed ${result.filename}: ${result.analysis.total_concepts_detected} concepts detected.`);
      }
    } catch (err) {
      alert(`Upload analysis error: ${err.message}`);
    } finally {
      const status = container.querySelector('#upload-status-indicator');
      if (status) status.style.display = 'none';
    }
  },

  attachConfirmListener(container) {
    const confirmBtn = container.querySelector('#btn-confirm-upload-changes');
    if (confirmBtn && this.lastAnalysis) {
      confirmBtn.addEventListener('click', async () => {
        const checkedBoxes = container.querySelectorAll('.upload-confirm-checkbox:checked');
        const confirmedTopics = [];

        checkedBoxes.forEach(cb => {
          const tid = cb.getAttribute('data-topic-id');
          const select = container.querySelector(`.upload-status-select[data-topic-id="${tid}"]`);
          const status = select ? select.value : 'in_progress';
          confirmedTopics.push({ topic_id: tid, status: status, confidence: 2 });
        });

        if (confirmedTopics.length === 0) {
          alert('Please select at least one topic checkbox to confirm.');
          return;
        }

        try {
          confirmBtn.disabled = true;
          confirmBtn.textContent = 'Saving...';
          const res = await API.confirmUploadTopics({
            upload_id: this.lastAnalysis.upload_id,
            filename: this.lastAnalysis.filename,
            confirmed_topics: confirmedTopics
          });
          App.showToast(res.message);
          await App.refreshGlobalState();
          App.navigate('dashboard');
        } catch (err) {
          alert(`Failed to confirm upload changes: ${err.message}`);
        } finally {
          confirmBtn.disabled = false;
          confirmBtn.textContent = 'Confirm & Save Progress Updates';
        }
      });
    }
  }
};

