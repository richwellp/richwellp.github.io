<template>
  <div class="about-me">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <img src="/assets/photos/professional/professional_1.jpg" alt="Richwell Perez" class="hero-image" />
        <h1>Richwell Cyrille Santos Perez</h1>
        <p class="subtitle">BS/MCS @ UIUC | AI Engineer</p>

        <!-- Animated Subtitle -->
        <transition name="slide-fade" mode="out-in">
          <div :key="currentIndex" class="animated-subtitle">
            <p class="animated-title">{{ timelineItems[currentIndex].title }}</p>
            <p class="animated-description">{{ timelineItems[currentIndex].description }}</p>
          </div>
        </transition>

        <p class="intro">
          I design AI systems that solve real problems. Currently building RAG chatbots and
          predictive models that serve hundreds of users at Safran.
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
              I'm an introvert who opens up once you know me. Born in the Philippines, I've always
              been fascinated by how technology can transform the way we work and live.
            </p>
            <p>
              My interest in AI grew stronger when I watched OpenAI play Dota 2 in 2017. Seeing AI
              defeat pro players in a 1v1 game—and eventually master 5v5 matches—sparked something
              in me. I realized AI wasn't just about algorithms; it was about eliminating manual
              labor and building the future.
            </p>
            <p>
              Today, I work with cutting-edge technology every day. There's something incredibly
              satisfying about watching a model correctly interpret an image, understand a sentence,
              or learn a pattern on its own. It's rewarding to constantly learn new ideas and see AI
              systems perform in real-world scenarios.
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
              creating AI solutions to eliminate manual labor.
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
              <h3>University of Illinois Urbana-Champaign</h3>
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

    <!-- Interests -->
    <section class="interests">
      <div class="container">
        <h2>Beyond Computer Science</h2>
        <div class="interests-grid">
          <div class="interest-card">
            <h3>🏐 Volleyball</h3>
            <p>I love <span class="dashed-strike">spiking</span> the strategy and teamwork that goes into every match.</p>
          </div>
          <div class="interest-card">
            <h3>💪 Powerlifting</h3>
            <p>Building strength and discipline, one rep at a time.</p>
          </div>
          <div class="interest-card">
            <h3>🎮 Gaming</h3>
            <p>Dota 2, Valorant, and some anime games—where my AI interest began.</p>
          </div>
          <div class="interest-card">
            <h3>✈️ Traveling</h3>
            <p>Exploring new places and experiencing different cultures.</p>
          </div>
        </div>
        <div class="personal-photos">
          <img src="/assets/photos/travel/wyoming/personal.JPG" alt="Travel" class="personal-photo" />
          <img src="/assets/photos/travel/colorado/personal_emlake.jpg" alt="Nature" class="personal-photo" />
        </div>
      </div>
    </section>

    <!-- Visitor Map -->
    <section class="visitor-map">
      <div class="container">
        <h2>Visitors</h2>
        <div id="map-container">
          <!-- Clustrmaps widget will be inserted here -->
          <a href="https://clustrmaps.com/site/1c5wm" title="Visit tracker">
            <img
              src="//www.clustrmaps.com/map_v2.png?d=YOUR_CLUSTER_ID&cl=ffffff&w=a"
              alt="Visitor map"
            />
          </a>
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
    description: 'Full-stack Development, RAG, and Applied Machine Learning.'
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

/* Interests */
.interests {
  background: var(--bg-secondary);
}

.interests-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.interest-card {
  background: var(--bg-card);
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  text-align: center;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.dashed-strike {
  text-decoration: line-through;
  text-decoration-style: dashed;
}

.interest-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
  border-color: var(--accent-primary);
}

.interest-card h3 {
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  color: var(--text-primary);
}

.interest-card p {
  color: var(--text-secondary);
  line-height: 1.6;
}

.personal-photos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.personal-photo {
  width: 100%;
  border-radius: 12px;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border-color);
}

/* Visitor Map */
.visitor-map {
  background: var(--bg-primary);
}

#map-container {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

#map-container img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border-color);
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .story-content {
    grid-template-columns: 1fr;
  }

  .interests-grid {
    grid-template-columns: 1fr;
  }

  .personal-photos {
    grid-template-columns: 1fr;
  }
}
</style>
