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
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
}

h1 {
  font-size: clamp(2.25rem, 4vw, 3rem);
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  text-align: center;
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.025em;
}

.page-intro {
  text-align: center;
  font-size: clamp(1.0625rem, 1.4vw, 1.15rem);
  color: var(--text-secondary);
  line-height: 1.7;
  margin-bottom: 4rem;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

/* Timeline */
.timeline {
  position: relative;
  padding-left: 3rem;
  margin-top: 2.5rem;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 2rem;
  bottom: 2rem;
  width: 2px;
  background: linear-gradient(180deg,
    var(--accent-primary) 0%,
    var(--accent-secondary) 50%,
    var(--border-color) 100%
  );
  opacity: 0.7;
}

/* Experience Card */
.experience-card {
  position: relative;
  background: var(--bg-card);
  border-radius: 12px;
  padding: 2.25rem;
  margin-bottom: 2.5rem;
  margin-left: 1.5rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06),
              0 1px 3px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

/* Staggered entrance */
.experience-card:nth-child(1) { animation-delay: 0.1s; }
.experience-card:nth-child(2) { animation-delay: 0.2s; }
.experience-card:nth-child(3) { animation-delay: 0.3s; }
.experience-card:nth-child(4) { animation-delay: 0.4s; }
.experience-card:nth-child(5) { animation-delay: 0.5s; }

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.experience-card:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1),
              0 4px 8px rgba(0, 0, 0, 0.06);
  border-color: var(--accent-primary)60;
}

.timeline-marker {
  position: absolute;
  left: -3rem;
  top: 2.25rem;
  width: 18px;
  height: 18px;
  background: var(--accent-primary);
  border: 4px solid var(--bg-primary);
  border-radius: 50%;
  z-index: 1;
  box-shadow: 0 0 0 4px var(--accent-primary)30;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.experience-card:hover .timeline-marker {
  transform: scale(1.35);
  box-shadow: 0 0 0 8px var(--accent-primary)40;
  background: var(--accent-hover);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.25rem;
  flex-wrap: wrap;
  gap: 1.25rem;
  cursor: pointer;
  user-select: none;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color)40;
}

.card-header:hover h3 {
  color: var(--accent-primary);
}

.card-header h3 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  transition: color 0.3s ease;
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.company {
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
  color: var(--text-tertiary);
  font-weight: 500;
  letter-spacing: -0.01em;
}

.date {
  font-size: 0.9375rem;
  color: var(--accent-primary);
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: -0.01em;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1.125rem;
}

/* Collapsible Cards */
.collapse-btn {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--accent-primary);
  font-size: 0.875rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 32px;
}

.collapse-btn:hover {
  transform: scale(1.1);
  background: var(--accent-primary);
  color: var(--bg-card);
  border-color: var(--accent-primary);
}

.collapse-icon {
  display: inline-block;
  transition: transform 0.3s ease;
  font-size: 0.75rem;
}

.experience-card.collapsed {
  opacity: 0.7;
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.04);
}

.experience-card.collapsed:hover {
  opacity: 1;
}

.card-content {
  padding-top: 1rem;
}

.card-content .description {
  font-size: clamp(1.0625rem, 1.2vw, 1.09375rem);
  color: var(--text-secondary);
  margin-bottom: 1.25rem;
  line-height: 1.7;
  font-weight: 400;
}

.achievements {
  list-style: none;
  padding: 0;
  margin: 1.25rem 0;
}

.achievements li {
  padding-left: 1.75rem;
  margin-bottom: 0.875rem;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.65;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
}

.achievements li:last-child {
  margin-bottom: 0;
}

.achievements li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.625em;
  width: 6px;
  height: 6px;
  background: var(--accent-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 2px var(--accent-primary)30;
}

.achievements li strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* Tech Stack */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color)60;
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
  color: var(--bg-card);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.12);
  border-color: var(--accent-primary);
}

/* Responsive */
@media (max-width: 768px) {
  .experience {
    padding: 3.5rem 1.5rem;
  }

  .page-intro {
    margin-bottom: 3rem;
  }

  .timeline {
    padding-left: 2.5rem;
  }

  .timeline-marker {
    left: -2.5rem;
    width: 14px;
    height: 14px;
    border: 3px solid var(--bg-primary);
  }

  .experience-card {
    margin-left: 1rem;
    padding: 1.875rem;
  }

  .card-header {
    flex-direction: column;
    gap: 0.75rem;
  }

  .header-right {
    width: 100%;
    justify-content: space-between;
  }

  .date {
    align-self: flex-start;
  }
}

@media (max-width: 480px) {
  .experience {
    padding: 3rem 1.25rem;
  }

  .timeline {
    padding-left: 2rem;
  }

  .timeline-marker {
    left: -2rem;
  }

  .experience-card {
    margin-left: 0.75rem;
    padding: 1.5rem;
  }

  .tech-tag {
    font-size: 0.75rem;
    padding: 0.375rem 0.75rem;
  }
}
</style>
