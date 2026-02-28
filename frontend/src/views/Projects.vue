<template>
  <div class="projects">
    <div class="container">
      <h1>Projects</h1>
      <p class="page-intro">{{ content.projectsPageIntro }}</p>

      <div class="projects-grid">
        <div
          v-for="(project, index) in projects"
          :key="index"
          class="project-block"
        >
          <div class="project-header">
            <h3>{{ project.name }}</h3>
            <p class="project-subtitle">{{ project.subtitle }}</p>
            <!-- Links (if any) -->
            <a
              v-for="(link, linkIndex) in project.links"
              :key="linkIndex"
              :href="link"
              target="_blank"
              rel="noopener noreferrer"
              :class="link.includes('github') ? 'github-link' : 'award-badge'"
            >
              {{ link.includes('hackathon-winners') ? '3rd Place, Ashby Prize in Computational Science' : 'View on GitHub →' }}
            </a>
          </div>
          <p class="project-description">{{ project.description }}</p>
          <ul class="project-highlights">
            <li v-for="(highlight, hIndex) in project.highlights" :key="hIndex">
              {{ highlight }}
            </li>
          </ul>
          <div class="tech-stack">
            <span
              v-for="tech in project.technologies"
              :key="tech"
              class="tech-tag"
            >
              {{ tech }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, nextTick } from 'vue'
import { injectStructuredData, generateProjectsListSchema } from '../composables/useStructuredData'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'

// Load professional info
const { projects, content, loadProfessionalInfo } = useProfessionalInfo()

let cardObserver = null

const setupCardObserver = () => {
  if (cardObserver) cardObserver.disconnect()
  cardObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const idx = parseInt(entry.target.dataset.idx || 0)
          entry.target.style.transitionDelay = `${idx * 0.12}s`
          entry.target.classList.add('visible')
          entry.target.addEventListener('transitionend', () => {
            entry.target.style.transitionDelay = '0s'
          }, { once: true })
          cardObserver.unobserve(entry.target)
        }
      })
    },
    { threshold: 0.08, rootMargin: '0px 0px -40px 0px' }
  )
  document.querySelectorAll('.project-block').forEach((el, i) => {
    el.dataset.idx = i
    cardObserver.observe(el)
  })
}

onMounted(async () => {
  await loadProfessionalInfo()

  // Inject structured data for projects list
  if (projects.value) {
    const projectsForSchema = projects.value.map(p => ({
      title: p.name,
      description: p.description
    }))
    const projectsSchema = generateProjectsListSchema(projectsForSchema)
    injectStructuredData(projectsSchema, 'projects-list-schema')
  }

  // Scroll-triggered reveal — double-tick ensures v-for is fully flushed
  await nextTick()
  await nextTick()
  setupCardObserver()
})

onUnmounted(() => {
  cardObserver?.disconnect()
})
</script>

<style scoped>
.projects {
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

@keyframes headingReveal {
  from { opacity: 0; transform: translateY(22px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes lineExpand {
  from { width: 0; opacity: 0; }
  to   { width: 48px; opacity: 1; }
}

h1 {
  font-size: clamp(2.25rem, 4vw, 3rem);
  color: var(--text-primary);
  margin-bottom: 2rem;
  text-align: left;
  font-weight: 800;
  letter-spacing: -0.035em;
  position: relative;
  padding-bottom: 1.25rem;
  opacity: 0;
  animation: headingReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.15s both;
}

h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent-primary) 50%, transparent);
  animation: lineExpand 0.45s cubic-bezier(0.4, 0, 0.2, 1) 0.65s both;
}

.page-intro {
  text-align: left;
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 4rem;
  max-width: 620px;
  font-weight: 400;
  opacity: 0;
  animation: headingReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.35s both;
}

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 2rem;
}

.project-block {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.25rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3),
              0 1px 4px rgba(0, 0, 0, 0.18);
  border: 1px solid var(--border-color);
  transition: opacity 0.65s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.65s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.4s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  opacity: 0;
  transform: translateY(36px) scale(0.965);
}

.project-block.visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.project-block::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 12px 12px 0 0;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.project-block.visible:hover {
  transform: translateY(-8px) scale(1);
  box-shadow: 0 20px 56px rgba(0, 0, 0, 0.55),
              0 8px 20px rgba(0, 0, 0, 0.3),
              0 0 0 1px rgba(129, 140, 248, 0.08),
              0 0 40px rgba(129, 140, 248, 0.06);
  border-color: color-mix(in srgb, var(--accent-primary) 38%, transparent);
}

.project-block.visible:hover::before {
  opacity: 1;
}

.project-header {
  margin-bottom: 1.5rem;
}

.project-header h3 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin-bottom: 0.625rem;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
  transition: color 0.3s ease;
}

.project-block:hover .project-header h3 {
  color: var(--accent-primary);
}

.project-subtitle {
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  color: var(--text-tertiary);
  font-style: italic;
  margin-bottom: 0.75rem;
  line-height: 1.5;
  font-weight: 400;
}

.award-badge,
.github-link {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.5625rem 1.125rem;
  border-radius: 7px;
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: -0.01em;
  border: 1.5px solid color-mix(in srgb, var(--accent-primary) 31%, transparent);
  text-decoration: none;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  margin-top: 0.625rem;
  position: relative;
  overflow: hidden;
}

.award-badge::before,
.github-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.award-badge:hover,
.github-link:hover {
  background: var(--accent-primary);
  color: #05060f;
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4),
              0 0 20px rgba(129, 140, 248, 0.2);
  border-color: var(--accent-primary);
}

.award-badge:hover::before,
.github-link:hover::before {
  left: 100%;
}

.project-description {
  font-size: clamp(1.0625rem, 1.2vw, 1.09375rem);
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.7;
  font-weight: 400;
}

.project-highlights {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.project-highlights li {
  padding-left: 1.75rem;
  margin-bottom: 0.875rem;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.65;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
}

.project-highlights li:last-child {
  margin-bottom: 0;
}

.project-highlights li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.625em;
  width: 6px;
  height: 6px;
  background: var(--accent-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent-primary) 19%, transparent);
}

/* Tech Stack */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-top: 1.75rem;
  padding-top: 1.75rem;
  border-top: 1px solid color-mix(in srgb, var(--border-color) 50%, transparent);
}

.tech-tag {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  padding: 0.4375rem 0.875rem;
  border-radius: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default;
}

.tech-tag:hover {
  background: var(--accent-primary);
  color: #05060f;
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4),
              0 0 14px rgba(129, 140, 248, 0.18);
  border-color: var(--accent-primary);
}

/* Responsive */
@media (max-width: 768px) {
  .projects {
    padding: 3.5rem 1.5rem;
  }

  .page-intro {
    margin-bottom: 3rem;
  }

  .projects-grid {
    grid-template-columns: 1fr;
    gap: 1.75rem;
  }

  .project-block {
    padding: 1.875rem;
  }

  .tech-stack {
    gap: 0.5rem;
  }
}

@media (max-width: 480px) {
  .projects {
    padding: 3rem 1.25rem;
  }

  .project-block {
    padding: 1.5rem;
  }

  .tech-tag {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }
}
</style>
