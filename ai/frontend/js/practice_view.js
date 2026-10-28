/**
 * AI Engineer Learning OS - Practice & Quizzes View
 * Interactive quizzes and scenarios for self-assessment and mastery evidence.
 */

const PracticeView = {
  render(container, state) {
    const { topics, progress } = state;
    const quizHistory = progress?.quiz_history || {};
    const progressMap = progress?.topics_progress || {};

    let html = `
      <div class="view-header" style="margin-bottom: 24px;">
        <h1 style="font-size: 1.6rem; font-weight: 800; letter-spacing: -0.02em;">Practice & Quizzes</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-top: 4px;">
          Assessment evidence guarantees that topics are truly understood before recommending mastery.
        </p>
      </div>

      <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px;">
    `;

    topics.forEach(topic => {
      const attempts = quizHistory[topic.id] || [];
      const hasPassed = attempts.some(a => a.passed);
      const userP = progressMap[topic.id] || { status: 'not_started', confidence_rating: 1 };

      html += `
        <div class="card" style="padding: 18px; display: flex; flex-direction: column; justify-content: space-between;">
          <div>
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span class="badge" style="background: var(--bg-card-subtle); color: var(--accent-cyan);">Stage ${topic.stage_id}</span>
              ${hasPassed ? `
                <span class="badge" style="background: rgba(16, 185, 129, 0.15); color: #34d399;">Quiz Passed</span>
              ` : (attempts.length > 0 ? `
                <span class="badge" style="background: rgba(245, 158, 11, 0.15); color: #fbbf24;">Revision Needed</span>
              ` : `
                <span class="badge badge-not-started">No Attempts</span>
              `)}
            </div>

            <h3 style="font-size: 1.05rem; font-weight: 700; color: #fff; margin-bottom: 4px;">${topic.title}</h3>
            <p style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.4; margin-bottom: 12px;">${topic.importance}</p>

            ${attempts.length > 0 ? `
              <div style="background: var(--bg-card-subtle); padding: 8px 12px; border-radius: var(--radius-sm); font-size: 0.75rem; color: var(--text-dim); margin-bottom: 12px;">
                Last Score: <strong style="color: var(--text-main);">${attempts[0].score}/${attempts[0].total_questions}</strong> on ${new Date(attempts[0].created_at).toLocaleDateString()}
              </div>
            ` : ''}
          </div>

          <div style="border-top: 1px solid var(--border-subtle); padding-top: 12px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 0.75rem; color: var(--text-dim);">Confidence: ${userP.confidence_rating}/5</span>
            <button class="btn btn-primary btn-sm" onclick="App.openTopicLesson('${topic.id}#part8-quiz')">
              Take Quiz →
            </button>
          </div>
        </div>
      `;
    });

    html += `</div>`;
    container.innerHTML = html;
  }
};

