<template>
  <div class="projects">
    <div class="container">
      <h1>Projects</h1>
      <p class="page-intro">
        A showcase of my personal and academic projects, demonstrating my expertise in AI, full-stack development, and software engineering.
      </p>

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
              {{ link.includes('hackathon-winners') ? '🏆 3rd Place, Ashby Prize in Computational Science' : 'View on GitHub →' }}
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
import { onMounted } from 'vue'
import { injectStructuredData, generateProjectsListSchema } from '../composables/useStructuredData'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'

// Load professional info
const { projects, loadProfessionalInfo } = useProfessionalInfo()

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
})
</script>

<style scoped>
.projects {
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

/* Projects Grid */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2.5rem;
}

@media (max-width: 1200px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .projects-grid {
    grid-template-columns: 1fr;
  }
}

.project-block {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.5rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.project-block:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.project-header {
  margin-bottom: 1.5rem;
}

.project-header h3 {
  font-size: 1.8rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.project-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
  font-style: italic;
  margin-bottom: 0.5rem;
}

.award-badge,
.github-link {
  display: inline-block;
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid var(--accent-primary);
  text-decoration: none;
  transition: all 0.3s ease;
  margin-top: 0.5rem;
}

.award-badge:hover,
.github-link:hover {
  background: var(--accent-primary);
  color: var(--bg-card);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--shadow);
}

.project-description {
  font-size: 1.1rem;
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.7;
}

.project-highlights {
  list-style: none;
  padding: 0;
  margin: 1.5rem 0;
}

.project-highlights li {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.7;
  font-size: 1.05rem;
}

.project-highlights li:before {
  content: '▸';
  position: absolute;
  left: 0;
  color: var(--accent-primary);
  font-weight: bold;
  font-size: 1.2rem;
}

/* Tech Stack */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.tech-tag {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  border: 1px solid var(--border-color);
  transition: all 0.3s ease;
}

.tech-tag:hover {
  background: var(--accent-primary);
  color: var(--bg-card);
  transform: translateY(-2px);
}

/* Responsive */
@media (max-width: 768px) {
  .projects {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .project-block {
    padding: 2rem;
  }

  .project-header h3 {
    font-size: 1.5rem;
  }

  .project-subtitle {
    font-size: 1rem;
  }

  .project-description {
    font-size: 1rem;
  }

  .project-highlights li {
    font-size: 1rem;
  }

  .tech-stack {
    gap: 0.5rem;
  }

  .tech-tag {
    font-size: 0.85rem;
    padding: 0.4rem 0.8rem;
  }
}
</style>
