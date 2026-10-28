/**
 * AI Engineer Learning OS - Universal API Client & Static Fallback Engine
 * Communicates with backend REST API when available, and seamlessly falls back
 * to in-browser local persistence if deployed on static web hosts (Vercel, Netlify, GitHub Pages).
 */

const API = {
  baseUrl: '',

  async request(endpoint, options = {}) {
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...defaultHeaders,
          ...(options.headers || {})
        }
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return await response.json();
    } catch (err) {
      // Fallback for static hosts (Vercel static / GitHub Pages)
      return this.handleStaticFallback(endpoint, options);
    }
  },

  // In-memory / localStorage fallback when running purely as static frontend
  handleStaticFallback(endpoint, options) {
    const cleanEndpoint = endpoint.split('?')[0].split('#')[0];
    const cachedData = localStorage.getItem('aieos_local_db');
    let localDB = cachedData ? JSON.parse(cachedData) : {
      topics_progress: {},
      quiz_history: {},
      project_progress: {},
      stats: { total_topics: 60, mastered: 0, in_progress: 0, needs_revision: 0, not_started: 60, completion_percentage: 0 }
    };

    if (cleanEndpoint === '/api/health') {
      return { status: 'healthy (static mode)', storage: 'Client LocalStorage' };
    }

    if (cleanEndpoint === '/api/roadmap') {
      return { stages: window.STATIC_STAGES || [], topics: window.STATIC_TOPICS || [] };
    }

    if (cleanEndpoint === '/api/progress') {
      return localDB;
    }

    if (cleanEndpoint === '/api/progress/topic' && options.method === 'POST') {
      const body = JSON.parse(options.body || '{}');
      const tid = body.topic_id;
      if (tid) {
        localDB.topics_progress[tid] = {
          topic_id: tid,
          status: body.status || 'in_progress',
          confidence_rating: body.confidence_rating || 3,
          personal_notes: body.personal_notes || '',
          last_studied_date: new Date().toISOString()
        };
        // Recompute stats
        const allT = window.STATIC_TOPICS || [];
        const m = Object.values(localDB.topics_progress).filter(p => p.status === 'mastered').length;
        const inp = Object.values(localDB.topics_progress).filter(p => p.status === 'in_progress').length;
        const rev = Object.values(localDB.topics_progress).filter(p => p.status === 'needs_revision').length;
        localDB.stats = {
          total_topics: allT.length,
          mastered: m,
          in_progress: inp,
          needs_revision: rev,
          not_started: allT.length - m - inp - rev,
          completion_percentage: Math.round((m / Math.max(allT.length, 1)) * 100)
        };
        localStorage.setItem('aieos_local_db', JSON.stringify(localDB));
      }
      return { success: true };
    }

    if (cleanEndpoint === '/api/recommendation') {
      const allT = window.STATIC_TOPICS || [];
      const first = allT[0] || { id: 'py_syntax', title: 'Python Syntax and Variables', stage_id: 1, difficulty: 'Beginner', estimated_hours: 3 };
      return {
        recommended_topic: first,
        reason: 'Essential foundational starting point for your AI Engineering journey.',
        satisfied_prerequisites: []
      };
    }

    if (cleanEndpoint.startsWith('/api/topic/')) {
      const tid = cleanEndpoint.replace('/api/topic/', '');
      const t = (window.STATIC_TOPICS || []).find(x => x.id === tid) || { id: tid, title: tid, stage_id: 1, key_concepts: [] };
      return {
        topic: t,
        stage: (window.STATIC_STAGES || [])[(t.stage_id || 1) - 1] || { id: 1, name: 'Foundations' },
        lesson: {
          part1_simple_explanation: { what_it_is: t.importance || t.title, why_it_exists: 'Essential for AI engineering workflows.', problem_it_solves: 'Eliminates errors.', real_world_use: 'Used across production AI systems.' },
          part2_analogy: { analogy_title: 'Intuitive Model', story: 'Think of this like an essential instrument in an engineer toolbox.', technical_difference: 'Executes in software.' },
          part3_visual_diagram: { title: `${t.title} Flow`, nodes: [{ label: 'Input', color: '#38bdf8' }, { label: 'Process', color: '#a855f7' }, { label: 'Output', color: '#22c55e' }], flow_steps: ['1. Data enters.', '2. Core logic executes.', '3. Emitted downstream.'] },
          part4_mechanism: ['Initialize inputs.', 'Execute transformation.', 'Validate output.'],
          part5_code: { beginner_example: { title: `${t.title} Demo`, code: `# Hands on with ${t.title}\nprint('Ready to learn ${t.title}')`, explanation: 'Simple demonstration code.', expected_output: `Ready to learn ${t.title}` } },
          part6_when_to_use: { use_cases: ['Foundation learning', 'Production ML'] },
          part7_problems_engineers_face: [{ problem: 'Configuration errors', symptoms: 'Fails to run', causes: 'Missing parameters', diagnosis: 'Inspect logs', fix: 'Add proper inputs', prevention: 'Unit test' }],
          part8_knowledge_check: {
            beginner_questions: [
              { question: `What is the primary role of ${t.title}?`, options: ['Core foundation for AI workflows', 'Irrelevant', 'Hardware only'], correct_idx: 0, explanation: 'Forms the core foundation.' },
              { question: 'Why is it important?', options: ['Ensures reliability and scalability', 'No reason', 'Just for fun'], correct_idx: 0, explanation: 'Prevents downstream bottlenecks.' }
            ]
          }
        }
      };
    }

    if (cleanEndpoint === '/api/revisions') {
      return { due_today: [], overdue: [], needs_revision: [], weak_concepts: [], counts: { due_today_count: 0, overdue_count: 0, needs_revision_count: 0, weak_concepts_count: 0 } };
    }

    if (cleanEndpoint === '/api/projects') {
      return { projects: [] };
    }

    return {};
  },

  async getHealth() { return this.request('/api/health'); },
  async getRoadmap() { return this.request('/api/roadmap'); },
  async getProgress() { return this.request('/api/progress'); },
  async updateTopicProgress(payload) { return this.request('/api/progress/topic', { method: 'POST', body: JSON.stringify(payload) }); },
  async getRecommendation() { return this.request('/api/recommendation'); },
  async getTopicLesson(topicId) { return this.request(`/api/topic/${encodeURIComponent(topicId.split('#')[0].split('?')[0])}`); },
  async getPrerequisitesTree(topicId) { return this.request(`/api/prerequisites/${encodeURIComponent(topicId.split('#')[0].split('?')[0])}`); },
  async submitQuiz(payload) { return this.request('/api/quiz/submit', { method: 'POST', body: JSON.stringify(payload) }); },
  async getRevisions() { return this.request('/api/revisions'); },
  async getProjects() { return this.request('/api/projects'); },
  async updateProjectStatus(payload) { return this.request('/api/projects/status', { method: 'POST', body: JSON.stringify(payload) }); },
  async uploadStudyMaterial(payload) { return this.request('/api/upload', { method: 'POST', body: JSON.stringify(payload) }); },
  async confirmUploadTopics(payload) { return this.request('/api/upload/confirm', { method: 'POST', body: JSON.stringify(payload) }); },
  async exportData() { return this.request('/api/export'); },
  async importData(payload) { return this.request('/api/import', { method: 'POST', body: JSON.stringify(payload) }); },
  async resetData() { return this.request('/api/reset', { method: 'POST', body: JSON.stringify({}) }); }
};
