<template>
  <div class="experience">
    <div class="container">
      <h1>Experience</h1>
      <p class="page-intro">{{ content.experiencePageIntro }}</p>

      <section class="entries">
        <div
          v-for="(exp, index) in experience"
          :key="index"
          class="entry-card"
          :class="{ expanded: isExpanded(index) }"
          :style="{ '--idx': index }"
        >
          <!-- Header: always visible, click to toggle -->
          <div class="entry-header" @click="toggleCard(index)" role="button" :aria-expanded="isExpanded(index)">
            <div class="title-group">
              <h3>{{ exp.title }}</h3>
              <p class="company">{{ exp.company }}<span class="sep"> · </span>{{ exp.location }}</p>
            </div>
            <div class="header-right">
              <span class="date">{{ exp.dates }}</span>
              <span class="expand-btn" :class="{ open: isExpanded(index) }">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6 9 12 15 18 9"></polyline>
                </svg>
              </span>
            </div>
          </div>

          <!-- Expandable: description + highlights + tech stack -->
          <div class="entry-expandable" :class="{ open: isExpanded(index) }">
            <div class="expandable-inner">
              <p class="description">{{ exp.description }}</p>
              <ul class="achievements">
                <li v-for="(highlight, hIndex) in exp.highlights" :key="hIndex">
                  <template v-if="highlight.includes(': ')">
                    <strong>{{ highlight.split(': ')[0] }}:</strong>
                    {{ highlight.slice(highlight.indexOf(': ') + 2) }}
                  </template>
                  <template v-else>{{ highlight }}</template>
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

        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { injectStructuredData, generateWorkExperienceSchema } from '../composables/useStructuredData'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'

const { experience, content, loadProfessionalInfo } = useProfessionalInfo()

// Tracks which cards are expanded. First card (index 0) starts expanded.
const expandedCards = ref(new Set([0]))

const isExpanded = (index) => expandedCards.value.has(index)

const toggleCard = (index) => {
  const updated = new Set(expandedCards.value)
  if (updated.has(index)) {
    updated.delete(index)
  } else {
    updated.add(index)
  }
  expandedCards.value = updated
}

onMounted(async () => {
  await loadProfessionalInfo()
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
  max-width: 900px;
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

@keyframes cardReveal {
  from { opacity: 0; transform: translateY(24px) scale(0.98); }
  to   { opacity: 1; transform: translateY(0) scale(1); }
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

/* ── Entry list ── */
.entries {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

/* ── Entry card ── */
.entry-card {
  background: var(--bg-card);
  border-radius: 12px;
  padding: 0;
  border: 1px solid var(--border-color);
  border-left: 3px solid color-mix(in srgb, var(--accent-primary) 30%, transparent);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.28), 0 1px 4px rgba(0, 0, 0, 0.15);
  animation: cardReveal 0.55s cubic-bezier(0.4, 0, 0.2, 1) both;
  animation-delay: calc(var(--idx, 0) * 0.1s + 0.3s);
  transition: box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  overflow: hidden;
}

.entry-card:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.38), 0 2px 8px rgba(0, 0, 0, 0.18);
  border-left-color: var(--accent-primary);
}

.entry-card.expanded {
  border-left-color: var(--accent-primary);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.38), 0 2px 8px rgba(0, 0, 0, 0.18),
              0 0 0 1px rgba(129, 140, 248, 0.05);
}

/* ── Card header (clickable) ── */
.entry-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1.875rem 2rem 0;
  cursor: pointer;
  user-select: none;
  border-radius: 12px 12px 0 0;
  transition: background-color 0.2s ease;
}

.entry-header:hover {
  background: color-mix(in srgb, var(--accent-primary) 3%, transparent);
}

.entry-header:hover .title-group h3 {
  color: var(--accent-primary);
}

/* Left side: title + company — allowed to shrink/wrap naturally */
.title-group {
  flex: 1;
  min-width: 0;
}

.title-group h3 {
  font-size: clamp(1.125rem, 1.7vw, 1.375rem);
  color: var(--text-primary);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.25;
  margin: 0 0 0.3rem;
  transition: color 0.25s ease;
}

.company {
  font-size: clamp(0.875rem, 1.05vw, 0.9375rem);
  color: var(--text-tertiary);
  font-weight: 500;
  letter-spacing: -0.01em;
  margin: 0;
}

.sep {
  opacity: 0.4;
}

/* Right side: date + expand btn — never shrinks, always stays on the right */
.header-right {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  flex-shrink: 0;
}

.date {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--accent-secondary);
  font-weight: 500;
  white-space: nowrap;
  letter-spacing: 0.01em;
  opacity: 0.9;
}

/* ── Expand icon button ── */
.expand-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  background: color-mix(in srgb, var(--accent-primary) 8%, var(--bg-tertiary));
  border: 1px solid color-mix(in srgb, var(--accent-primary) 22%, transparent);
  color: var(--accent-primary);
  flex-shrink: 0;
  user-select: none;
  transition: background 0.25s ease, border-color 0.25s ease;
}

.expand-btn svg {
  transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.expand-btn.open {
  background: color-mix(in srgb, var(--accent-primary) 18%, var(--bg-tertiary));
  border-color: color-mix(in srgb, var(--accent-primary) 45%, transparent);
}

.expand-btn.open svg {
  transform: rotate(180deg);
}

.entry-header:hover .expand-btn {
  background: color-mix(in srgb, var(--accent-primary) 15%, var(--bg-tertiary));
  border-color: color-mix(in srgb, var(--accent-primary) 38%, transparent);
}

/* ── Description (inside expandable) ── */
.description {
  font-size: clamp(0.9375rem, 1.15vw, 1rem);
  color: var(--text-secondary);
  margin: 0 0 1.125rem;
  padding-bottom: 1.125rem;
  border-bottom: 1px solid color-mix(in srgb, var(--border-color) 50%, transparent);
  line-height: 1.7;
  font-weight: 400;
}

/* ── Expandable content (highlights + tech) ── */
.entry-expandable {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.entry-expandable.open {
  grid-template-rows: 1fr;
}

.expandable-inner {
  overflow: hidden;
  /* Static padding — grid-template-rows handles all height animation */
  padding: 1.25rem 2rem 1.875rem;
  position: relative;
}

/* Gradient separator — teal-tinted, fades at both ends, visible in both themes */
.expandable-inner::before {
  content: '';
  position: absolute;
  top: 0;
  left: 2rem;
  right: 2rem;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    color-mix(in srgb, var(--accent-primary) 45%, var(--border-color)) 20%,
    color-mix(in srgb, var(--accent-primary) 45%, var(--border-color)) 80%,
    transparent 100%
  );
  opacity: 0;
  transition: opacity 0.4s ease;
}

.entry-expandable.open .expandable-inner::before {
  opacity: 1;
}

/* ── Achievements ── */
.achievements {
  list-style: none;
  padding: 0;
  margin: 0 0 1.5rem;
}

.achievements li {
  padding-left: 1.375rem;
  margin-bottom: 0.625rem;
  position: relative;
  color: var(--text-secondary);
  line-height: 1.65;
  font-size: clamp(0.875rem, 1.05vw, 0.9375rem);
}

.achievements li:last-child {
  margin-bottom: 0;
}

.achievements li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.6em;
  width: 5px;
  height: 5px;
  background: var(--accent-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--accent-primary) 18%, transparent);
}

.achievements li strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* ── Tech stack ── */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4375rem;
  padding-top: 1.25rem;
  border-top: 1px solid color-mix(in srgb, var(--border-color) 40%, transparent);
}

.tech-tag {
  background: var(--bg-tertiary);
  color: var(--text-primary);
  padding: 0.3125rem 0.6875rem;
  border-radius: 5px;
  font-size: 0.75rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  border: 1px solid var(--border-color);
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: default;
  font-family: 'JetBrains Mono', monospace;
}

@media (hover: hover) {
  .tech-tag:hover {
    background: var(--accent-primary);
    color: #05060f;
    border-color: var(--accent-primary);
    transform: translateY(-1px);
    box-shadow: 0 3px 10px rgba(129, 140, 248, 0.22);
  }
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .experience {
    padding: 3.5rem 1.5rem;
  }

  .page-intro {
    margin-bottom: 3rem;
  }
}

@media (max-width: 480px) {
  .experience {
    padding: 3rem 1.25rem;
  }

  .entry-header,
  .description {
    padding-left: 1.375rem;
    padding-right: 1.375rem;
  }

  .expandable-inner {
    padding-left: 1.375rem;
    padding-right: 1.375rem;
  }
}
</style>
