/**
 * AI Engineer Learning OS - Interactive Learning Roadmap View
 * Renders the multi-stage horizontal dependency node graph with smooth curved bezier arrows,
 * status color-coding, interactive hover highlights, and direct navigation to topic lessons.
 */

const RoadmapView = {
  activeHoverId: null,

  render(container, state) {
    const { stages, topics, progress, recommendation } = state;
    const progressMap = progress?.topics_progress || {};
    const recommendedId = recommendation?.recommended_topic?.id;

    // Dimensions & Grid metrics
    const cw = 175; // column width
    const nw = 148; // node width
    const rh = 52;  // row height
    const pos = {};
    const cnt = {};

    // Group topics by stage and compute coordinates
    topics.forEach(t => {
      // stages are 1-indexed in topics (1 to 12), map to 0-indexed column (0 to 11)
      const stageIdx = (t.stage_id ? t.stage_id - 1 : t.stage) || 0;
      const i = cnt[stageIdx] || 0;
      cnt[stageIdx] = i + 1;
      pos[t.id] = {
        x: stageIdx * cw + 16,
        y: 45 + i * rh,
        stageIdx: stageIdx
      };
    });

    const maxRows = Math.max(...Object.values(cnt), 10);
    const H = maxRows * rh + 65;
    const W = 12 * cw + 40;

    // Generate Stage Column Headers
    const stageNames = [
      "1. Programming", "2. Math for AI", "3. Data Analysis",
      "4. Machine Learning", "5. Deep Learning", "6. Specialized Nets",
      "7. NLP & LLMs", "8. RAG", "9. Agents",
      "10. Backend", "11. MLOps", "12. Advanced"
    ];

    let headerSvg = "";
    stageNames.forEach((sName, i) => {
      const x = i * cw + 16;
      headerSvg += `
        <text x="${x}" y="24" font-size="12" font-weight="700" fill="#94a3b8" font-family="'Plus Jakarta Sans', system-ui, sans-serif">
          ${sName}
        </text>
      `;
    });

    // Generate Connecting Arrows (Curved cubic beziers)
    let edgesSvg = "";
    topics.forEach(t => {
      (t.prerequisites || t.pre || []).forEach(pId => {
        const a = pos[pId];
        const b = pos[t.id];
        if (!a || !b) return;

        const y1 = a.y + 17;
        const y2 = b.y + 17;

        let pathD = "";
        if (a.stageIdx === b.stageIdx) {
          // Same column curve out to right and back
          pathD = `M ${a.x + nw} ${y1} C ${a.x + nw + 35} ${y1}, ${b.x + nw + 35} ${y2}, ${b.x + nw} ${y2}`;
        } else {
          // Inter-column cubic bezier
          const midX = (a.x + nw + b.x) / 2;
          pathD = `M ${a.x + nw} ${y1} C ${midX} ${y1}, ${midX} ${y2}, ${b.x} ${y2}`;
        }

        edgesSvg += `
          <path class="roadmap-edge edge-from-${pId} edge-to-${t.id}"
                data-from="${pId}" data-to="${t.id}"
                d="${pathD}"
                fill="none"
                stroke="#64748b"
                stroke-width="1.3"
                stroke-opacity="0.32"
                marker-end="url(#ar)" />
        `;
      });
    });

    // Generate Topic Nodes
    let nodesSvg = "";
    topics.forEach(t => {
      const p = pos[t.id];
      if (!p) return;

      const userProg = progressMap[t.id] || { status: "not_started" };
      const status = userProg.status || "not_started";
      const isRecommended = (t.id === recommendedId);

      // Color mapping matching prompt & reference:
      // Gray=Not started, Blue=In progress, Amber=Needs revision, Green=Mastered, Purple=Recommended next
      let strokeColor = "#475569";
      let fillBg = "rgba(71, 85, 105, 0.16)";
      let textColor = "#f1f5f9";
      let strokeWidth = "1.5";

      if (isRecommended) {
        strokeColor = "#a855f7"; // Purple
        fillBg = "rgba(168, 85, 247, 0.22)";
        strokeWidth = "2.5";
      } else if (status === "mastered") {
        strokeColor = "#22c55e"; // Green
        fillBg = "rgba(34, 197, 94, 0.18)";
      } else if (status === "in_progress") {
        strokeColor = "#3b82f6"; // Blue
        fillBg = "rgba(59, 130, 246, 0.20)";
      } else if (status === "needs_revision") {
        strokeColor = "#f59e0b"; // Amber
        fillBg = "rgba(245, 158, 11, 0.20)";
      }

      const displayName = t.title || t.name || t.id;
      const truncatedName = displayName.length > 21 ? displayName.slice(0, 19) + "…" : displayName;

      nodesSvg += `
        <g class="roadmap-node-g"
           id="node-g-${t.id}"
           data-topic-id="${t.id}"
           tabindex="0"
           role="button"
           style="cursor: pointer;"
           onclick="App.openTopicLesson('${t.id}')">
          <title>${displayName} (${status.replace('_', ' ')})&#10;${t.importance || ''}</title>
          
          <rect id="rect-${t.id}"
                x="${p.x}" y="${p.y}"
                width="${nw}" height="35"
                rx="8" ry="8"
                fill="${fillBg}"
                stroke="${strokeColor}"
                stroke-width="${strokeWidth}"
                style="transition: all 0.2s ease;" />

          <text x="${p.x + 10}" y="${p.y + 22}"
                font-size="12"
                font-weight="500"
                fill="${textColor}"
                font-family="'Plus Jakarta Sans', system-ui, -apple-system, sans-serif"
                pointer-events="none">
            ${truncatedName}
          </text>
        </g>
      `;
    });

    let html = `
      <!-- Header Card matching reference -->
      <div class="card" style="padding: 22px 26px; margin-bottom: 20px;">
        <h1 style="font-size: 1.55rem; font-weight: 800; color: #fff; margin-bottom: 4px;">Learning roadmap</h1>
        <p style="color: var(--text-muted); font-size: 0.88rem; margin-bottom: 14px;">
          Arrows point from a prerequisite to the topic that depends on it. Click a node to open it. Scroll sideways to see all stages.
        </p>

        <!-- Color Legend Row -->
        <div class="leg" style="display: flex; flex-wrap: wrap; align-items: center; gap: 16px; font-size: 0.82rem;">
          <span style="display: inline-flex; align-items: center; gap: 6px;">
            <i style="width: 10px; height: 10px; border-radius: 3px; background: #64748b; display: inline-block;"></i>
            <span>Not Started</span>
          </span>
          <span style="display: inline-flex; align-items: center; gap: 6px;">
            <i style="width: 10px; height: 10px; border-radius: 3px; background: #3b82f6; display: inline-block;"></i>
            <span>In Progress</span>
          </span>
          <span style="display: inline-flex; align-items: center; gap: 6px;">
            <i style="width: 10px; height: 10px; border-radius: 3px; background: #f59e0b; display: inline-block;"></i>
            <span>Needs Revision</span>
          </span>
          <span style="display: inline-flex; align-items: center; gap: 6px;">
            <i style="width: 10px; height: 10px; border-radius: 3px; background: #22c55e; display: inline-block;"></i>
            <span>Mastered</span>
          </span>
          <span style="display: inline-flex; align-items: center; gap: 6px;">
            <i style="width: 10px; height: 10px; border-radius: 3px; background: #a855f7; box-shadow: 0 0 6px #a855f7; display: inline-block;"></i>
            <span style="font-weight: 600; color: #c084fc;">Recommended next</span>
          </span>
        </div>
      </div>

      <!-- Horizontal Side-Scrolling Roadmap Container matching reference -->
      <div class="roadwrap" style="
        overflow-x: auto;
        overflow-y: hidden;
        border: 1px solid var(--border-subtle);
        border-radius: var(--radius-lg);
        background: #0d111a;
        padding: 16px 12px;
        box-shadow: var(--shadow-sm);
        position: relative;
      ">
        <svg width="${W}" height="${H}" role="img" aria-label="Interactive AI Roadmap Graph" style="display: block;">
          <defs>
            <marker id="ar" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="6" markerHeight="6" orient="auto">
              <path d="M 0 0 L 8 4 L 0 8 z" fill="#64748b" opacity="0.6"/>
            </marker>
            <marker id="ar-highlight-in" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M 0 0 L 8 4 L 0 8 z" fill="#38bdf8"/>
            </marker>
            <marker id="ar-highlight-out" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">
              <path d="M 0 0 L 8 4 L 0 8 z" fill="#a855f7"/>
            </marker>
          </defs>

          <!-- Stage Column Headers -->
          ${headerSvg}

          <!-- Prerequisite Curves -->
          <g id="edges-group">
            ${edgesSvg}
          </g>

          <!-- Nodes -->
          <g id="nodes-group">
            ${nodesSvg}
          </g>
        </svg>
      </div>
    `;

    container.innerHTML = html;
    this.attachGraphInteractions(container);
  },

  attachGraphInteractions(container) {
    const nodeGroups = container.querySelectorAll('.roadmap-node-g');
    const edges = container.querySelectorAll('.roadmap-edge');

    nodeGroups.forEach(g => {
      const topicId = g.getAttribute('data-topic-id');
      const rect = g.querySelector('rect');

      g.addEventListener('mouseenter', () => {
        // Dim all edges slightly
        edges.forEach(e => {
          e.style.strokeOpacity = '0.08';
          e.style.strokeWidth = '1';
        });

        // Highlight incoming prerequisite edges (in Cyan)
        const inEdges = container.querySelectorAll(`.edge-to-${topicId}`);
        inEdges.forEach(e => {
          e.style.stroke = '#38bdf8';
          e.style.strokeWidth = '2.5';
          e.style.strokeOpacity = '1';
          e.setAttribute('marker-end', 'url(#ar-highlight-in)');
        });

        // Highlight outgoing dependent edges (in Purple)
        const outEdges = container.querySelectorAll(`.edge-from-${topicId}`);
        outEdges.forEach(e => {
          e.style.stroke = '#a855f7';
          e.style.strokeWidth = '2.5';
          e.style.strokeOpacity = '1';
          e.setAttribute('marker-end', 'url(#ar-highlight-out)');
        });

        if (rect) {
          rect.style.filter = 'drop-shadow(0 0 8px rgba(56, 189, 248, 0.4))';
        }
      });

      g.addEventListener('mouseleave', () => {
        // Reset all edges
        edges.forEach(e => {
          e.style.stroke = '#64748b';
          e.style.strokeWidth = '1.3';
          e.style.strokeOpacity = '0.32';
          e.setAttribute('marker-end', 'url(#ar)');
        });

        if (rect) {
          rect.style.filter = 'none';
        }
      });
    });
  }
};
