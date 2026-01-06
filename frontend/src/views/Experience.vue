<template>
  <div class="experience">
    <div class="container">
      <h1>Experience</h1>
      <p class="page-intro">
        A chronological overview of my professional work experience, showcasing my journey
        in AI and software engineering.
      </p>

      <!-- Work Experience -->
      <section class="work-experience">
        <h2 class="section-title">Work Experience</h2>

        <!-- Safran -->
        <div class="experience-card" :class="{ collapsed: !expandedCards.safran }">
          <div class="card-header" @click="toggleCard('safran')">
            <div>
              <h3>AI Engineer</h3>
              <p class="company">Safran | Laramie, WY; Brea, CA</p>
            </div>
            <div class="header-right">
              <span class="date">June 2025 - Present</span>
              <button class="collapse-btn" aria-label="Toggle details">
                <span class="collapse-icon">{{ expandedCards.safran ? '▼' : '▶' }}</span>
              </button>
            </div>
          </div>
          <div class="card-content" v-show="expandedCards.safran">
            <p class="description">
              Developing AI initiatives in aerospace and in-flight entertainment systems, building
              production-grade RAG solutions with multi-agent architectures and predictive maintenance systems.
            </p>
            <ul class="achievements">
              <li>
                <strong>Multi-Agent RAG System:</strong> Architected and deployed a hierarchical LangGraph-based chatbot for aviation Master Data Management, serving 600+ internal users via Azure App Services. Implemented a supervisor agent orchestrating specialized business knowledge and SQL agents with Server-Sent Events (SSE) streaming for real-time responses.
              </li>
              <li>
                <strong>Full-Stack Development:</strong> Built end-to-end solution with Quart (async Python) backend, Vue 3 + Vuex frontend, dual PostgreSQL databases (operational + knowledge base), and Azure OpenAI integration with embeddings and Azure Dynamic Sessions for secure code execution.
              </li>
              <li>
                <strong>Performance Optimization:</strong> Reduced response latency by 50% (2×faster) through optimization of multi-agent orchestration, prompt engineering (Prompty templates), intelligent caching strategies, and prompt distillation techniques.
              </li>
              <li>
                <strong>Production Infrastructure:</strong> Deployed scalable ASGI APIs with Hypercorn, implemented conversation persistence with message ratings and reasoning trace storage, structured JSONL logging, comprehensive pytest + pytest-asyncio test suites, and Azure OpenTelemetry monitoring.
              </li>
              <li>
                <strong>ML Analytics & Insights:</strong> Applied unsupervised machine learning (K-Means, DBSCAN, UMAP, HDBSCAN) and topic modeling to cluster 10,000+ RAG conversation interactions, built analytical dashboards with matplotlib for usage patterns, and implemented continuous improvement feedback loops.
              </li>
              <li>
                <strong>Predictive Maintenance:</strong> Developing ML-based predictive maintenance
                system to forecast RDU (Removable Display Unit) resets in in-flight entertainment
                (IFE) systems using historical telemetry, operational data, and scikit-learn models to improve reliability
                and minimize downtime.
              </li>
              <li>
                <strong>IFE Log Analysis System:</strong> Developing LLM-powered log analyzer for In-Flight Entertainment systems to process 2GB log bundles (5M+ lines). Implementing 4-stage pipeline with Drain algorithm for template mining (30x compression), vector database for semantic search, and intelligent 2-level query routing to achieve 500-1000x log reduction with comprehensive analysis capabilities.
              </li>
            </ul>
            <div class="tech-stack">
              <span class="tech-tag">Python</span>
              <span class="tech-tag">LangChain</span>
              <span class="tech-tag">Vue.js</span>
              <span class="tech-tag">Quart</span>
              <span class="tech-tag">PostgreSQL</span>
              <span class="tech-tag">Azure OpenAI</span>
              <span class="tech-tag">Azure App Services</span>
              <span class="tech-tag">SSE</span>
              <span class="tech-tag">RAG</span>
              <span class="tech-tag">Scikit-learn</span>
            </div>
          </div>
        </div>

        <!-- Illinois Secretary of State -->
        <div class="experience-card" :class="{ collapsed: !expandedCards.ilsos }">
          <div class="card-header" @click="toggleCard('ilsos')">
            <div>
              <h3>Database Administrator</h3>
              <p class="company">Illinois Secretary of State | Springfield, IL</p>
            </div>
            <div class="header-right">
              <span class="date">February 2025 - June 2025</span>
              <button class="collapse-btn" aria-label="Toggle details">
                <span class="collapse-icon">{{ expandedCards.ilsos ? '▼' : '▶' }}</span>
              </button>
            </div>
          </div>
          <div class="card-content" v-show="expandedCards.ilsos">
            <p class="description">
              Managed high-throughput DB2 databases on z/OS mainframe systems, supporting statewide
              digital initiatives.
            </p>
            <ul class="achievements">
              <li>
                <strong>Database Optimization:</strong> Managed high-throughput DB2 databases (5B+
                records) on z/OS mainframe systems, optimizing queries and schemas to support
                statewide applications.
              </li>
              <li>
                <strong>Performance Tuning:</strong> Improved query performance by designing and
                tuning complex SQL queries and schemas, reducing lookup time from 20 seconds to
                instantaneous for critical backend application queries.
              </li>
              <li>
                <strong>Automation:</strong> Implemented ETL pipelines and automation scripts to
                streamline data migration and significantly reduce manual effort.
              </li>
              <li>
                <strong>Cross-functional Collaboration:</strong> Collaborated with cross-functional
                development teams to design efficient schemas, stored procedures, and to integrate
                Azure-based services for scalable, cloud-connected applications.
              </li>
              <li>
                <strong>Digital Initiatives:</strong> Supported the development and deployment of
                statewide digital initiatives, including mobile driver's licenses and REAL ID.
              </li>
            </ul>
            <div class="tech-stack">
              <span class="tech-tag">DB2</span>
              <span class="tech-tag">SQL</span>
              <span class="tech-tag">z/OS</span>
              <span class="tech-tag">Azure</span>
              <span class="tech-tag">ETL</span>
              <span class="tech-tag">Python</span>
            </div>
          </div>
        </div>

        <!-- UIUC - Teaching Assistant -->
        <div class="experience-card" :class="{ collapsed: !expandedCards.uiucta }">
          <div class="card-header" @click="toggleCard('uiucta')">
            <div>
              <h3>Graduate Teaching Assistant</h3>
              <p class="company">University of Illinois Urbana-Champaign | Urbana, IL</p>
            </div>
            <div class="header-right">
              <span class="date">August 2022 - May 2023</span>
              <button class="collapse-btn" aria-label="Toggle details">
                <span class="collapse-icon">{{ expandedCards.uiucta ? '▼' : '▶' }}</span>
              </button>
            </div>
          </div>
          <div class="card-content" v-show="expandedCards.uiucta">
            <p class="description">
              Led discussions and labs for Software Design & Database Systems courses.
            </p>
            <ul class="achievements">
              <li>
                Led discussions and labs for Software Design & Database Systems, teaching
                object-oriented design, design patterns, and database performance optimization to
                800+ students.
              </li>
            </ul>
            <div class="tech-stack">
              <span class="tech-tag">Java</span>
              <span class="tech-tag">SQL</span>
              <span class="tech-tag">OOP</span>
              <span class="tech-tag">Design Patterns</span>
            </div>
          </div>
        </div>

        <!-- UIUC - Software Engineer -->
        <div class="experience-card" :class="{ collapsed: !expandedCards.uiucse }">
          <div class="card-header" @click="toggleCard('uiucse')">
            <div>
              <h3>Software Engineer</h3>
              <p class="company">University of Illinois Urbana-Champaign | Urbana, IL</p>
            </div>
            <div class="header-right">
              <span class="date">July 2021 - August 2021</span>
              <button class="collapse-btn" aria-label="Toggle details">
                <span class="collapse-icon">{{ expandedCards.uiucse ? '▼' : '▶' }}</span>
              </button>
            </div>
          </div>
          <div class="card-content" v-show="expandedCards.uiucse">
            <p class="description">
              Developed embedded software for magnet mapping hardware systems.
            </p>
            <ul class="achievements">
              <li>
                Developed LabWindows/CVI software to support new magnet mapping hardware,
                implementing real-time data interpretation, control logic, and optimizing
                frontend/backend performance.
              </li>
            </ul>
            <div class="tech-stack">
              <span class="tech-tag">C</span>
              <span class="tech-tag">LabWindows/CVI</span>
              <span class="tech-tag">Embedded Systems</span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'

// Card expansion state - all cards start expanded
const expandedCards = reactive({
  safran: true,
  ilsos: true,
  uiucta: true,
  uiucse: true
})

const toggleCard = (cardId) => {
  expandedCards[cardId] = !expandedCards[cardId]
}
</script>

<style scoped>
.experience {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
  text-align: center;
}

.page-intro {
  text-align: center;
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.section-title {
  font-size: 2rem;
  color: var(--text-primary);
  margin: 3rem 0 2rem 0;
  padding-bottom: 0.5rem;
  border-bottom: 3px solid var(--accent-primary);
}

/* Experience Card */
.experience-card,
.project-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.experience-card:hover,
.project-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  flex-wrap: wrap;
  gap: 1rem;
  cursor: pointer;
  user-select: none;
}

.card-header:hover h3 {
  color: var(--accent-primary);
}

.card-header h3 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  transition: color 0.3s ease;
}

.company {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.date {
  font-size: 1rem;
  color: var(--accent-primary);
  font-weight: 600;
  white-space: nowrap;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Collapsible Cards */
.collapse-btn {
  background: transparent;
  border: none;
  color: var(--accent-primary);
  font-size: 1.2rem;
  cursor: pointer;
  padding: 0.25rem 0.5rem;
  transition: transform 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 30px;
}

.collapse-btn:hover {
  transform: scale(1.2);
}

.collapse-icon {
  display: inline-block;
  transition: transform 0.3s ease;
}

.experience-card.collapsed,
.project-card.collapsed {
  opacity: 0.8;
}

.experience-card.collapsed:hover,
.project-card.collapsed:hover {
  opacity: 1;
}

.card-content .description {
  font-size: 1.05rem;
  color: var(--text-secondary);
  margin-bottom: 1rem;
  line-height: 1.6;
}

.achievements {
  list-style: none;
  padding: 0;
  margin: 1rem 0;
}

.achievements li {
  padding-left: 1.5rem;
  margin-bottom: 0.75rem;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.6;
}

.achievements li:before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--accent-primary);
  font-weight: bold;
}

.achievements li strong {
  color: var(--text-primary);
}

/* Tech Stack */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1.5rem;
}

.tech-tag {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid var(--border-color);
}

/* Responsive */
@media (max-width: 768px) {
  .experience {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .card-header {
    flex-direction: column;
  }

  .header-right {
    width: 100%;
    justify-content: space-between;
  }

  .date {
    align-self: flex-start;
  }
}
</style>
