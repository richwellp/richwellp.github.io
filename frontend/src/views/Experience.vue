<template>
  <div class="experience">
    <div class="container">
      <h1>Experience</h1>
      <p class="page-intro">
        A chronological overview of my professional work experience, showcasing my journey
        in AI and software engineering.
      </p>

      <!-- Timeline -->
      <section class="timeline">
        <div
          v-for="(exp, index) in experience"
          :key="index"
          class="experience-card"
          :class="{ collapsed: !expandedCards[index] }"
        >
          <div class="timeline-marker"></div>
          <div class="card-header" @click="toggleCard(index)">
            <div>
              <h3>{{ exp.title }}</h3>
              <p class="company">{{ exp.company }} | {{ exp.location }}</p>
            </div>
            <div class="header-right">
              <span class="date">{{ exp.dates }}</span>
              <button class="collapse-btn" aria-label="Toggle details">
                <span class="collapse-icon">{{ expandedCards[index] ? '▼' : '▶' }}</span>
              </button>
            </div>
          </div>
          <div class="card-content" v-show="expandedCards[index]">
            <p class="description">{{ exp.description }}</p>
            <ul class="achievements">
              <li v-for="(highlight, hIndex) in exp.highlights" :key="hIndex">
                {{ highlight }}
              </li>
            </ul>
            <div class="tech-stack">
              <span
                v-for="tech in exp.technologies"
                :key="tech"
                class="tech-tag"
              >
                {{ tech }}
              </span>
            </div>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted, watch } from 'vue'
import { injectStructuredData, generateWorkExperienceSchema } from '../composables/useStructuredData'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'

// Load professional info
const { experience, loadProfessionalInfo } = useProfessionalInfo()

// Card expansion state - dynamically managed
const expandedCards = reactive({})

// Initialize expanded state when experience loads
watch(experience, (newExperience) => {
  if (newExperience) {
    newExperience.forEach((_, index) => {
      if (!(index in expandedCards)) {
        expandedCards[index] = true // All cards start expanded
      }
    })
  }
}, { immediate: true })

const toggleCard = (cardIndex) => {
  expandedCards[cardIndex] = !expandedCards[cardIndex]
}

onMounted(async () => {
  await loadProfessionalInfo()

  // Inject work experience schema
  const workExperienceSchema = generateWorkExperienceSchema()
  injectStructuredData(workExperienceSchema, 'work-experience-schema')
})
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

/* Timeline */
.timeline {
  position: relative;
  padding-left: 2rem;
  margin-top: 2rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 2rem;
  bottom: 2rem;
  width: 3px;
  background: linear-gradient(to bottom, var(--accent-primary), var(--border-color));
}

/* Experience Card */
.experience-card {
  position: relative;
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2rem;
  margin-bottom: 2rem;
  margin-left: 1rem;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
}

.experience-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.timeline-marker {
  position: absolute;
  left: -2.65rem;
  top: 2rem;
  width: 16px;
  height: 16px;
  background: var(--accent-primary);
  border: 3px solid var(--bg-primary);
  border-radius: 50%;
  z-index: 1;
  box-shadow: 0 0 0 4px var(--bg-card);
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

  .timeline {
    padding-left: 1.5rem;
  }

  .timeline::before {
    width: 2px;
  }

  .timeline-marker {
    left: -2.1rem;
    width: 12px;
    height: 12px;
  }

  .experience-card {
    margin-left: 0.5rem;
    padding: 1.5rem;
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
