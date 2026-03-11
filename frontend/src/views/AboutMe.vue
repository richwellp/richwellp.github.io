<template>
  <div class="about-me">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background-accent"></div>
      <div class="hero-inner">

        <!-- Circular Profile Photo -->
        <div class="photo-ring">
          <img
            src="/assets/photos/professional_1.jpg"
            alt="Richwell Perez"
            class="hero-photo"
          />
        </div>

        <!-- Name -->
        <h1>{{ personal.name }}</h1>

        <!-- Role tagline -->
        <p class="hero-tagline">
          AI Engineer ·
          BS/MCS @ <a href="https://siebelschool.illinois.edu/" target="_blank" rel="noopener noreferrer">UIUC</a>
        </p>

        <!-- Rotating showcase — slide-container holds arrows + card -->
        <div v-if="showcaseItems.length > 0" class="slide-container">
          <button class="slide-arrow slide-arrow--prev" @click="prevSlide" aria-label="Previous">&#8249;</button>
          <div
            class="rotating-wrapper"
            @pointerdown="onDragStart"
            @pointerup="onDragEnd"
            @pointercancel="onDragEnd"
          >
            <transition :name="slideTransition" mode="out-in">
              <div :key="currentIndex" class="rotating-block">
                <span class="rotating-label">{{ showcaseItems[currentIndex].label }}</span>
                <p class="rotating-title">{{ showcaseItems[currentIndex].title }}</p>
                <p class="rotating-desc">{{ showcaseItems[currentIndex].text }}</p>
              </div>
            </transition>
          </div>
          <button class="slide-arrow slide-arrow--next" @click="nextSlide" aria-label="Next">&#8250;</button>
        </div>

        <!-- Progress dots — click to jump to any item -->
        <div v-if="showcaseItems.length > 0" class="rotating-dots">
          <span
            v-for="(_, i) in showcaseItems"
            :key="i"
            class="rotating-dot"
            :class="{ active: i === currentIndex }"
            @click="goToSlide(i)"
          />
        </div>

        <!-- Brief intro -->
        <p class="hero-bio">{{ content.heroBio }}</p>

        <!-- Chat CTA -->
        <button class="hero-chat-btn" @click="toggleChat">
          <svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          Ask me anything →
        </button>

      </div>
    </section>

    <!-- Personal Story -->
    <section class="story">
      <div class="container">
        <h2>About Me</h2>
        <div class="story-content">
          <div class="story-text">
            <p v-for="(para, i) in content.storyParagraphs" :key="i">{{ para }}</p>
          </div>
          <div class="story-images">
            <img
              src="/assets/photos/professional_0.jpg"
              alt="Graduation"
              class="story-photo"
              :class="{ 'img-loaded': storyImageLoaded }"
              @load="storyImageLoaded = true"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Skills -->
    <section class="skills-section">
      <div class="container">
        <h2>Skills</h2>
        <div class="skills-panel" v-if="orderedSkills.length">
          <div class="panel-bar">
            <span class="panel-dot red"></span>
            <span class="panel-dot yellow"></span>
            <span class="panel-dot green"></span>
            <span class="panel-filename">// skills.json</span>
          </div>
          <div class="panel-body">
            <div
              v-for="{ key, label, items } in orderedSkills"
              :key="key"
              class="skill-row"
            >
              <span class="skill-cat">{{ label }}</span>
              <span class="skill-list">{{ items.join(' · ') }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Background -->
    <section class="background">
      <div class="container">
        <h2>My Journey</h2>
        <div class="timeline">
          <!-- Professional experience entries (RAVE, IL SoS) -->
          <div
            v-for="exp in timelineExperience"
            :key="exp.company"
            class="timeline-item"
          >
            <div class="timeline-header">
              <h3>{{ exp.title }} at {{ exp.company }}</h3>
              <span class="timeline-date">{{ exp.dates }}</span>
            </div>
            <p class="timeline-description">{{ exp.timelineDescription }}</p>
          </div>

          <!-- UIUC compound entry: both degrees + part-time roles -->
          <div v-if="education.length > 0" class="timeline-item">
            <div class="timeline-header">
              <h3>{{ education[1]?.institution || education[0]?.institution }}</h3>
              <span class="timeline-date">{{ education[1]?.dates }}</span>
            </div>
            <div class="timeline-details">
              <template v-for="edu in education" :key="edu.degree">
                <p>
                  <strong>{{ edu.degree }}</strong>
                  ({{ edu.dates }}, GPA: {{ edu.gpa }})
                </p>
                <p v-if="edu.focus">Focused on {{ edu.focus.join(', ') }}.</p>
                <p v-if="edu.specializations">Specialized in {{ edu.specializations.join(' and ') }}.</p>
              </template>
              <template v-for="exp in uiucExperience" :key="exp.title">
                <p>
                  <strong>{{ exp.title }}</strong>
                  (Part-time, {{ exp.dates }})
                </p>
                <p>{{ exp.highlights[0] }}</p>
              </template>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { injectMultipleStructuredData, generatePersonSchema, generateOrganizationSchema } from '../composables/useStructuredData'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'
import { useChatAssistant } from '../composables/useChatAssistant'

const storyImageLoaded = ref(false)

const { personal, skills, education, experience, content, loadProfessionalInfo } = useProfessionalInfo()

// Rotating showcase items — sourced from professionalInfo.json content.showcaseItems
const showcaseItems = computed(() => content.value.showcaseItems || [])

// My Journey — experience entries with a timelineDescription field
const timelineExperience = computed(() =>
  experience.value.filter(e => e.timelineDescription)
)

// UIUC part-time roles (TA + SWE) for the compound education entry
const uiucExperience = computed(() =>
  experience.value.filter(e =>
    e.company === 'University of Illinois Urbana-Champaign' && !e.current
  )
)
const { toggleChat } = useChatAssistant()

// Skills panel — ordered display with readable labels
const categoryOrder = ['languages', 'ai_ml', 'frameworks', 'databases', 'cloud', 'tools']
const categoryLabels = {
  languages:  'LANGUAGES',
  ai_ml:      'AI / ML',
  frameworks: 'FRAMEWORKS',
  databases:  'DATABASES',
  cloud:      'CLOUD',
  tools:      'TOOLS'
}
const orderedSkills = computed(() => {
  if (!skills.value) return []
  return categoryOrder
    .filter(k => skills.value[k])
    .map(k => ({ key: k, label: categoryLabels[k], items: skills.value[k] }))
})

const currentIndex = ref(0)
const direction = ref('next')  // 'next' | 'prev'
const slideTransition = computed(() =>
  direction.value === 'next' ? 'slide-next' : 'slide-prev'
)
let dragStartX = null
let intervalId = null

const nextSlide = () => {
  direction.value = 'next'
  currentIndex.value = (currentIndex.value + 1) % showcaseItems.value.length
  startInterval()
}

const prevSlide = () => {
  direction.value = 'prev'
  currentIndex.value = (currentIndex.value - 1 + showcaseItems.value.length) % showcaseItems.value.length
  startInterval()
}

const startInterval = () => {
  if (intervalId) clearInterval(intervalId)
  intervalId = setInterval(nextSlide, 4000)
}

// Uses >= so clicking the already-active dot resolves to 'next' as a safe tie-breaker
const goToSlide = (i) => {
  direction.value = i >= currentIndex.value ? 'next' : 'prev'
  currentIndex.value = i
  startInterval()
}

const onDragStart = (e) => {
  dragStartX = e.clientX
  e.currentTarget.setPointerCapture(e.pointerId)
}

const onDragEnd = (e) => {
  if (dragStartX === null) return
  const delta = e.clientX - dragStartX
  dragStartX = null
  if (Math.abs(delta) >= 40) {
    delta < 0 ? nextSlide() : prevSlide()
  }
}

onMounted(async () => {
  injectMultipleStructuredData([
    { schema: generatePersonSchema(), id: 'person-schema' },
    { schema: generateOrganizationSchema(), id: 'organization-schema' }
  ])

  await loadProfessionalInfo()

  startInterval()

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) entry.target.classList.add('visible')
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -80px 0px' }
  )

  document.querySelectorAll('.story, .skills-section, .background').forEach((s) => observer.observe(s))
})

onUnmounted(() => {
  if (intervalId) clearInterval(intervalId)
})
</script>

<style scoped>
.about-me {
  width: 100%;
}

/* ── Hero ── */
.hero {
  background: var(--bg-primary);
  background-image:
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 39px,
      rgba(129, 140, 248, 0.03) 39px,
      rgba(129, 140, 248, 0.03) 40px
    ),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 39px,
      rgba(129, 140, 248, 0.03) 39px,
      rgba(129, 140, 248, 0.03) 40px
    );
  padding: 6rem 2rem 5rem;
  min-height: 85vh;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}


/* Teal radial glow */
.hero-background-accent {
  position: absolute;
  top: -20%;
  right: -10%;
  width: 65%;
  height: 120%;
  background: radial-gradient(ellipse at 60% 40%, rgba(129, 140, 248, 0.12) 0%, rgba(129, 140, 248, 0.04) 40%, transparent 70%);
  animation: float 22s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) rotate(0deg) scale(1); }
  25%       { transform: translate(-30px, -60px) rotate(3deg) scale(1.05); }
  50%       { transform: translate(20px, 40px) rotate(-2deg) scale(0.95); }
  75%       { transform: translate(-15px, 50px) rotate(4deg) scale(1.02); }
}

.hero-inner {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 640px;
  width: 100%;
  margin: 0 auto;
}

/* ── Circular photo ── */
.photo-ring {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  margin: 0 auto 2rem;
  padding: 3px;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  box-shadow: 0 0 0 6px color-mix(in srgb, var(--accent-primary) 10%, transparent),
              0 16px 48px rgba(0, 0, 0, 0.5);
  animation: photoReveal 0.75s cubic-bezier(0.4, 0, 0.2, 1) 0.1s both,
             ringPulse 4s ease-in-out 1s infinite;
}

@keyframes ringPulse {
  0%, 100% {
    box-shadow: 0 0 0 6px color-mix(in srgb, var(--accent-primary) 10%, transparent),
                0 16px 48px rgba(0, 0, 0, 0.5);
  }
  50% {
    box-shadow: 0 0 0 10px color-mix(in srgb, var(--accent-primary) 5%, transparent),
                0 20px 56px rgba(0, 0, 0, 0.6);
  }
}

.hero-photo {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  object-position: center top;
  border: 3px solid var(--bg-primary);
  display: block;
}

@keyframes photoReveal {
  from { opacity: 0; transform: scale(0.88); }
  to   { opacity: 1; transform: scale(1); }
}

/* ── Name ── */
h1 {
  font-size: clamp(1.625rem, 3.2vw, 2.125rem);
  font-weight: 800;
  letter-spacing: -0.035em;
  line-height: 1.15;
  margin-bottom: 0.625rem;
  color: var(--text-primary);
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
}

/* ── Role tagline ── */
.hero-tagline {
  font-size: clamp(0.875rem, 1.2vw, 1rem);
  color: var(--text-secondary);
  margin-bottom: 1.5rem;
  line-height: 1.5;
  font-weight: 400;
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.3s both;
}

.hero-tagline a {
  color: var(--accent-primary);
  font-weight: 600;
  text-decoration: none;
  transition: color 0.2s ease;
}

.hero-tagline a:hover {
  color: var(--accent-hover);
}

/* ── Rotating showcase ── */
/* Outer wrapper holds stable height so Vue out-in transition has no layout shift */
.rotating-wrapper {
  flex: 1;
  min-width: 0;
  min-height: 82px;
  display: flex;
  align-items: stretch;
  overflow: hidden;
  touch-action: pan-y;
  cursor: grab;
  user-select: none;
}

.rotating-wrapper:active {
  cursor: grabbing;
}

/* Slide container — replaces rotating-wrapper's own width/margin/animation */
.slide-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  width: 100%;
  max-width: 480px;
  margin: 0 auto;
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
}

.slide-arrow {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: color-mix(in srgb, var(--accent-primary) 8%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent-primary) 22%, transparent);
  color: var(--accent-primary);
  font-size: 1.125rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: opacity 0.2s ease, background 0.2s ease, border-color 0.2s ease;
  padding: 0;
}

@media (hover: hover) {
  .slide-arrow { opacity: 0; }
  .slide-container:hover .slide-arrow { opacity: 1; }
  .slide-arrow:hover { background: color-mix(in srgb, var(--accent-primary) 18%, transparent); }
}

@media (hover: none) {
  .slide-arrow { opacity: 1; }
}

/* Direction-aware slide transitions */
.slide-next-enter-active {
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-next-leave-active {
  transition: opacity 0.22s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-next-enter-from { opacity: 0; transform: translateX(32px); }
.slide-next-leave-to   { opacity: 0; transform: translateX(-32px); }

.slide-prev-enter-active {
  transition: opacity 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-prev-leave-active {
  transition: opacity 0.22s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.22s cubic-bezier(0.4, 0, 0.2, 1);
}
.slide-prev-enter-from { opacity: 0; transform: translateX(-32px); }
.slide-prev-leave-to   { opacity: 0; transform: translateX(32px); }

.rotating-block {
  width: 100%;
  padding: 0.875rem 1.25rem;
  background: color-mix(in srgb, var(--accent-primary) 3%, var(--bg-card));
  border: 1px solid color-mix(in srgb, var(--accent-primary) 14%, var(--border-color));
  border-left: 3px solid var(--accent-primary);
  border-radius: 8px;
  text-align: left;
}

.rotating-label {
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--accent-primary);
  opacity: 0.7;
  font-weight: 500;
  margin-bottom: 0.3rem;
}

.rotating-title {
  font-size: clamp(0.9375rem, 1.4vw, 1rem);
  font-weight: 700;
  color: var(--text-primary);
  font-family: 'Urbanist', sans-serif;
  letter-spacing: -0.02em;
  line-height: 1.25;
  margin-bottom: 0.25rem;
}

.rotating-desc {
  font-size: clamp(0.8125rem, 1vw, 0.875rem);
  color: var(--text-tertiary);
  font-weight: 400;
  line-height: 1.4;
}


/* Progress dots */
.rotating-dots {
  display: flex;
  justify-content: center;
  gap: 0.375rem;
  margin: 0.75rem auto 1.375rem;
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.5s both;
}

.rotating-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: color-mix(in srgb, var(--accent-primary) 22%, var(--border-color));
  transition: all 0.3s ease;
  cursor: pointer;
  display: block;
}

.rotating-dot.active {
  background: var(--accent-primary);
  transform: scale(1.4);
  box-shadow: 0 0 6px rgba(129, 140, 248, 0.4);
}

/* ── Hero bio ── */
.hero-bio {
  font-size: clamp(0.9375rem, 1.2vw, 1rem);
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 520px;
  margin: 0 auto 0;
  font-weight: 400;
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.62s both;
}

@keyframes slideInUp {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Chat CTA button ── */
.hero-chat-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1.5rem;
  padding: 0.625rem 1.25rem;
  background: color-mix(in srgb, var(--accent-primary) 8%, transparent);
  border: 1px solid color-mix(in srgb, var(--accent-primary) 30%, transparent);
  border-radius: 100px;
  color: var(--accent-primary);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8125rem;
  font-weight: 500;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  animation: slideInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.72s both;
}

@media (hover: hover) {
  .hero-chat-btn:hover {
    background: var(--accent-primary);
    color: #05060f;
    border-color: var(--accent-primary);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(129, 140, 248, 0.3);
  }
}

/* ── Story & Background sections ── */
section {
  padding: 4rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-primary);
  text-align: left;
}

.story {
  background: var(--bg-primary);
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.9s cubic-bezier(0.4, 0, 0.2, 1);
}

.story.visible {
  opacity: 1;
  transform: translateY(0);
}

.story-content {
  display: grid;
  grid-template-columns: 1.8fr 1fr;
  gap: 4rem;
  align-items: start;
}

.story-text p {
  font-size: clamp(1.0625rem, 1.3vw, 1.125rem);
  line-height: 1.8;
  margin-bottom: 1.75rem;
  color: var(--text-secondary);
  font-weight: 400;
}

:deep(.story-photo) {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4),
              0 4px 12px rgba(0, 0, 0, 0.25),
              0 0 0 1px rgba(129, 140, 248, 0.1),
              0 0 30px rgba(129, 140, 248, 0.06);
  border: 1px solid var(--border-color);
  opacity: 0;
  transition: opacity 0.5s ease,
              transform 0.5s cubic-bezier(0.4, 0, 0.2, 1),
              box-shadow 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.story-photo.img-loaded) {
  opacity: 1;
}

@media (hover: hover) {
  :deep(.story-photo):hover {
    transform: translateY(-6px);
    box-shadow: 0 20px 55px rgba(0, 0, 0, 0.5),
                0 8px 20px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(129, 140, 248, 0.18),
                0 0 50px rgba(129, 140, 248, 0.1);
  }
}

.background {
  background: var(--bg-primary);
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.9s cubic-bezier(0.4, 0, 0.2, 1);
}

.background.visible {
  opacity: 1;
  transform: translateY(0);
}

.container h2 {
  margin-bottom: 3rem;
  font-size: clamp(2rem, 3.5vw, 2.5rem);
  font-weight: 700;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  position: relative;
  padding-bottom: 1rem;
  text-align: left;
}

.container h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent-primary) 50%, transparent);
}

/* ── Skills section ── */
.skills-section {
  background: var(--bg-secondary);
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.9s cubic-bezier(0.4, 0, 0.2, 1);
}

.skills-section.visible {
  opacity: 1;
  transform: translateY(0);
}

.skills-panel {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 1px 4px rgba(0, 0, 0, 0.2);
  max-width: 820px;
  margin: 0 auto;
}

.panel-bar {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.75rem 1.25rem;
  background: var(--bg-tertiary);
  border-bottom: 1px solid var(--border-color);
}

.panel-dot {
  width: 11px;
  height: 11px;
  border-radius: 50%;
  flex-shrink: 0;
}
.panel-dot.red    { background: #ff5f56; }
.panel-dot.yellow { background: #ffbd2e; }
.panel-dot.green  { background: #27c93f; }

.panel-filename {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-tertiary);
  letter-spacing: 0.04em;
  margin-left: 0.625rem;
}

.panel-body {
  padding: 0.5rem 0;
}

.skill-row {
  display: grid;
  grid-template-columns: 130px 1fr;
  gap: 1.5rem;
  padding: 0.75rem 1.75rem;
  border-bottom: 1px solid color-mix(in srgb, var(--border-color) 45%, transparent);
  align-items: baseline;
}

.skill-row:last-child {
  border-bottom: none;
}

.skill-cat {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  font-weight: 600;
  color: var(--accent-secondary);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  white-space: nowrap;
  opacity: 0.9;
}

.skill-list {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--text-secondary);
  line-height: 1.75;
  letter-spacing: 0.01em;
}

/* Timeline */
.timeline {
  max-width: 820px;
  margin: 0 auto;
}

.timeline-item {
  position: relative;
  margin-bottom: 1.25rem;
  padding: 2.25rem 2.5rem;
  background: var(--bg-card);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3), 0 1px 4px rgba(0, 0, 0, 0.18);
  border: 1px solid var(--border-color);
  border-left: 3px solid color-mix(in srgb, var(--accent-primary) 28%, transparent);
  transition: box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              border-color 0.35s cubic-bezier(0.4, 0, 0.2, 1),
              transform 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-item:first-child {
  border-left-color: var(--accent-primary);
}

@media (hover: hover) {
  .timeline-item:hover {
    transform: translateX(6px);
    border-left-color: var(--accent-primary);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5), 0 6px 16px rgba(0, 0, 0, 0.28),
                0 0 0 1px rgba(129, 140, 248, 0.06);
  }
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.125rem;
  gap: 1.25rem;
}

.timeline-item h3 {
  flex: 1;
  min-width: 0;
  color: var(--text-primary);
  margin: 0;
  font-size: clamp(1.25rem, 2vw, 1.5rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.timeline-date {
  flex-shrink: 0;
  color: var(--accent-secondary);
  font-size: 0.9375rem;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: -0.01em;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8125rem;
  opacity: 0.9;
}

.timeline-description {
  color: var(--text-secondary);
  line-height: 1.75;
  margin: 0;
  font-size: clamp(1rem, 1.2vw, 1.0625rem);
}

.timeline-details {
  margin-top: 1.25rem;
}

.timeline-details p {
  color: var(--text-secondary);
  line-height: 1.75;
  margin-bottom: 0.875rem;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
}

.timeline-details p strong {
  color: var(--text-primary);
  font-weight: 600;
}

.timeline-details p:last-child {
  margin-bottom: 0;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .hero {
    padding: 4.5rem 1.5rem 4rem;
    min-height: auto;
  }

  .photo-ring {
    width: 170px;
    height: 170px;
  }

  .story-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

}


@media (max-width: 640px) {
  .hero {
    padding: 4rem 1.5rem 3.5rem;
  }

  .container {
    padding: 3.5rem 1.5rem;
  }

  .timeline-item {
    padding: 1.75rem 1.5rem;
  }

  .timeline-header {
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 3.5rem 1.25rem 3rem;
  }

  .photo-ring {
    width: 150px;
    height: 150px;
  }

  .container {
    padding: 3rem 1.25rem;
  }

  .timeline-item {
    padding: 1.5rem 1.25rem;
  }

  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.375rem;
  }

  .skill-row {
    grid-template-columns: 1fr;
    gap: 0.25rem;
    padding: 0.625rem 1rem;
  }

  .skill-cat {
    white-space: normal;
  }
}
</style>
