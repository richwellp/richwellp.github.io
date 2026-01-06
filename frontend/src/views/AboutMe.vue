<template>
  <div class="about-me">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <img src="/assets/photos/professional/professional_1.jpg" alt="Richwell Perez" class="hero-image" />
        <h1>Richwell Cyrille Santos Perez</h1>
        <p class="subtitle">BS/MCS @ <a href="https://siebelschool.illinois.edu/" target="_blank" rel="noopener noreferrer">UIUC</a> | AI Engineer</p>

        <!-- Animated Subtitle -->
        <transition name="slide-fade" mode="out-in">
          <div :key="currentIndex" class="animated-subtitle">
            <p class="animated-title">{{ timelineItems[currentIndex].title }}</p>
            <p class="animated-description">{{ timelineItems[currentIndex].description }}</p>
          </div>
        </transition>

        <p class="intro">
          I build AI systems, data pipelines, and software that solve real problems. I'm passionate
          about using technology to make the world a better place, from machine learning to full-stack applications.
        </p>
      </div>
    </section>

    <!-- Personal Story -->
    <section class="story">
      <div class="container">
        <h2>About Me</h2>
        <div class="story-content">
          <div class="story-text">
            <p>
              I graduated with a BS and MCS in Computer Science from UIUC, specializing in the field of Data and Artificial intelligence. 
              My background spans teaching assistantship, full-stack development, database systems, and AI engineering. I've worked on machine learning models, 
              RAG systems, cloud platforms, and data pipelines. I like building things that solve real world problems.
            </p>
            <p>
              My interest in AI started with watching OpenAI dominate professional Dota 2 players back in 2017.
              Seeing it master a complex game with millions of possible moves showed me what AI could really do. 
              As I study AI deeper, I learned its strength in handling the repetitive, data-heavy work
              so people could focus on the creative and strategic parts that actually need human thinking.
            </p>
            <p>
              That's what gets me excited about this field. I want to build technologies that actually improve
              people's lives: whether it's through intelligent systems, data-driven insights, or reliable engineering. 
              I stay curious about new tools and approaches, and I do my best work in teams that value learning and building things that matter.
            </p>
          </div>
          <div class="story-images">
            <img src="/assets/photos/professional/professional_0.jpg" alt="Graduation" class="story-photo" />
          </div>
        </div>
      </div>
    </section>

    <!-- Background -->
    <section class="background">
      <div class="container">
        <h2>My Journey</h2>
        <div class="timeline">
          <div class="timeline-item">
            <div class="timeline-header">
              <h3>AI Engineer at Safran</h3>
              <span class="timeline-date">June 2025 - Present</span>
            </div>
            <p class="timeline-description">
              Building full-stack applications with RAG, developing predictive maintenance systems, and
              creating AI solutions to minimize manual labor.
            </p>
          </div>

          <div class="timeline-item">
            <div class="timeline-header">
              <h3>Database Administrator at Illinois Secretary of State</h3>
              <span class="timeline-date">February 2025 - June 2025</span>
            </div>
            <p class="timeline-description">
              Managed and optimized high-throughput DB2 databases on z/OS mainframe systems and supported statewide digital initiatives.
            </p>
          </div>

          <div class="timeline-item">
            <div class="timeline-header">
              <h3>University of Illinois at Urbana-Champaign</h3>
              <span class="timeline-date">August 2018 - May 2023</span>
            </div>
            <div class="timeline-details">
              <p><strong>Master of Computer Science</strong> (August 2022 - May 2023, GPA: 3.52)</p>
              <p><strong>Bachelor of Science in Computer Science with Honors</strong> (August 2018 - May 2023, GPA: 3.81)</p>
              <p><strong>Graduate Teaching Assistant</strong> (August 2022 - May 2023)</p>
              <p><strong>Software Engineer</strong> (July 2021 - August 2021)</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const timelineItems = [
  {
    title: 'AI Engineer',
    description: 'Full-stack Development, RAG, and Applied Machine Learning'
  },
  {
    title: 'Master of Computer Science',
    description: 'University of Illinois Urbana-Champaign (2022-2023, GPA: 3.52)'
  },
  {
    title: 'B.S. in Computer Science',
    description: 'University of Illinois Urbana-Champaign (2018-2023, GPA: 3.81)'
  }
]

const currentIndex = ref(0)
let intervalId = null

onMounted(() => {
  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % timelineItems.length
  }, 4000)
})

onUnmounted(() => {
  if (intervalId) {
    clearInterval(intervalId)
  }
})
</script>

<style scoped>
.about-me {
  width: 100%;
}

/* Hero Section */
.hero {
  background: var(--bg-secondary);
  color: var(--text-primary);
  padding: 4rem 2rem;
  text-align: center;
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Animated Subtitle */
.animated-subtitle {
  margin: 1.5rem 0;
  min-height: 120px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.animated-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--accent-primary);
  margin-bottom: 0.5rem;
}

.animated-description {
  font-size: 1rem;
  color: var(--text-secondary);
  opacity: 0.9;
}

.slide-fade-enter-active {
  transition: all 0.8s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.6s ease-in;
}

.slide-fade-enter-from {
  transform: translateY(30px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateY(-30px);
  opacity: 0;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
  position: relative;
  z-index: 1;
}

.hero-image {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  object-fit: cover;
  border: 5px solid var(--border-color);
  margin-bottom: 1.5rem;
  box-shadow: 0 10px 30px var(--shadow);
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.3rem;
  margin-bottom: 1.5rem;
  opacity: 0.95;
  font-weight: 300;
}

.subtitle a {
  color: var(--link-color);
  text-decoration: none;
  transition: color 0.3s ease;
}

.subtitle a:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.intro {
  font-size: 1.1rem;
  line-height: 1.6;
  max-width: 600px;
  margin: 0 auto;
  opacity: 0.9;
}

/* Sections */
section {
  padding: 4rem 2rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

h2 {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: var(--text-primary);
  text-align: center;
}

/* Story Section */
.story {
  background: var(--bg-primary);
}

.story-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 3rem;
  align-items: start;
}

.story-text p {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  color: var(--text-secondary);
}

.story-photo {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border-color);
}

/* Background/Timeline */
.timeline {
  max-width: 800px;
  margin: 0 auto;
}

.timeline-item {
  margin-bottom: 3rem;
  padding: 2rem;
  background: var(--bg-card);
  border-left: 4px solid var(--accent-primary);
  border-radius: 8px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.timeline-item h3 {
  color: var(--text-primary);
  margin: 0;
  font-size: 1.4rem;
  font-weight: 600;
}

.timeline-date {
  color: var(--accent-primary);
  font-size: 0.95rem;
  font-weight: 500;
  white-space: nowrap;
}

.timeline-description {
  color: var(--text-secondary);
  line-height: 1.8;
  margin: 0;
  font-size: 1.05rem;
}

.timeline-details {
  margin-top: 1rem;
}

.timeline-details p {
  color: var(--text-secondary);
  line-height: 1.8;
  margin-bottom: 0.75rem;
  font-size: 1rem;
}

.timeline-details p:last-child {
  margin-bottom: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .story-content {
    grid-template-columns: 1fr;
  }
}
</style>
