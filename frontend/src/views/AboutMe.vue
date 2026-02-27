<template>
  <div class="about-me">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-background-accent"></div>
      <div class="hero-content">
        <div class="hero-text">
          <h1>Richwell Cyrille Santos Perez</h1>
          <p class="subtitle">
            BS/MCS @ <a href="https://siebelschool.illinois.edu/" target="_blank" rel="noopener noreferrer">UIUC</a> |
            AI Engineer at <a href="https://www.linkedin.com/company/rave-aerospace" target="_blank" rel="noopener noreferrer">RAVE Aerospace</a>
          </p>

          <!-- Animated Subtitle -->
          <transition name="slide-fade" mode="out-in">
            <div :key="currentIndex" class="animated-subtitle">
              <p class="animated-title">{{ timelineItems[currentIndex].title }}</p>
              <p class="animated-description">{{ timelineItems[currentIndex].description }}</p>
            </div>
          </transition>

          <p class="intro">
            I build software, data, and AI systems that solve real-world problems, actively seeking opportunities to continuously learn, grow, and apply my expertise.
            I thrive in collaborative, fast-paced environments where I can make a meaningful, positive impact.
          </p>
        </div>

        <div class="hero-image-container">
          <img
            src="/assets/photos/professional_1.jpg"
            alt="Richwell Perez"
            class="hero-image"
          />
        </div>
      </div>
    </section>

    <!-- Personal Story -->
    <section class="story">
      <div class="container">
        <h2>About Me</h2>
        <div class="story-content">
          <div class="story-text">
            <p>
              Hello and welcome! I am Richwell Perez, and I earned a BS and MCS in Computer Science from UIUC, specializing in Data and Artificial Intelligence.
              My background includes teaching assistantships, software engineering, database systems, data science, and AI engineering. 
            </p>
            <p>
              I am drawn to building technology that solves real-world problems and have pursued opportunities into hands-on experience. 
              I have developed full-stack applications, ML and deep learning models, explored data analytics, built retrieval-augmented generation (RAG) systems, worked with cloud platforms, and delivered AI-powered applications,
              all to create solutions that make a real difference.
            </p>
            <p>
              My journey in Computer Science started with curiosity about computers, the internet, software and how they could connect people, provide entertainment, and solve problems. 
              Through school and early projects, I focused on roles that matched my strengths in critical thinking and problem-solving, which led me to specialize in software, data, and AI. 
              I enjoy building systems that learn from information, analyze data, and provide actionable insights, and I am always seeking practical ways to apply my skills.
            </p>
            <p>
              I am passionate about developing technologies that improve lives and deliver meaningful impact through software, data insights, and intelligent AI systems. 
              To pursue this passion, I have taken on projects and roles that challenge me and expand my skills in designing scalable applications, building ML models, developing data pipelines, and deploying cloud-based AI solutions. 
              I stay current with new tools and frameworks, thrive in fast-paced, collaborative environments, and aim to contribute to making the world a better place.
            </p>
          </div>
          <div class="story-images">
            <img
              src="/assets/photos/professional_0.jpg"
              alt="Graduation"
              class="story-photo"
            />
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
              <h3>AI Engineer at RAVE Aerospace</h3>
              <span class="timeline-date">June 2025 - Present</span>
            </div>
            <p class="timeline-description">
              Building full-stack applications with RAG, developing predictive maintenance systems for in-flight entertainment and connectivity (IFEC) systems, and
              creating AI solutions to minimize manual labor.
            </p>
          </div>

          <div class="timeline-item">
            <div class="timeline-header">
              <h3>Database Administrator at Illinois Secretary of State</h3>
              <span class="timeline-date">February 2025 - June 2025</span>
            </div>
            <p class="timeline-description">
              Managed and optimized high-throughput DB2 databases on z/OS mainframe systems and supported statewide digital initiatives, including the database systems for Apple Wallet mobile driver's license.
            </p>
          </div>

          <div class="timeline-item">
            <div class="timeline-header">
              <h3>University of Illinois at Urbana-Champaign</h3>
              <span class="timeline-date">August 2018 - May 2023</span>
            </div>
            <div class="timeline-details">
              <p><strong>Master of Computer Science</strong> (August 2022 - May 2023, GPA: 3.52)</p>
              <p>Focused on Computer Vision, Deep Learning, Data Mining, and Web Programming.</p>
              <p><strong>Bachelor of Science in Computer Science with Honors</strong> (August 2018 - May 2023, GPA: 3.81)</p>
              <p>Specialized in Intelligence and Data.</p>
              <p><strong>Graduate Teaching Assistant</strong> (Part-time, August 2022 - May 2023)</p>
              <p>Led discussions and labs for Software Design & Database Systems, teaching design patterns and databases to 800+ students.</p>
              <p><strong>Software Engineer</strong> (Part-time, July 2021 - August 2021)</p>
              <p>Developed and deployed LabWindows/CVI embedded software interfacing with new magnet-mapping hardware, enabling real-time data acquisition, control logic, and optimized system performance.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { injectMultipleStructuredData, generatePersonSchema, generateOrganizationSchema } from '../composables/useStructuredData'

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
  // Inject structured data for homepage
  injectMultipleStructuredData([
    { schema: generatePersonSchema(), id: 'person-schema' },
    { schema: generateOrganizationSchema(), id: 'organization-schema' }
  ])

  intervalId = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % timelineItems.length
  }, 4000)

  // Scroll-triggered animations for sections
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible')
        }
      })
    },
    { threshold: 0.15, rootMargin: '0px 0px -80px 0px' }
  )

  // Observe story and background sections
  const sections = document.querySelectorAll('.story, .background')
  sections.forEach((section) => observer.observe(section))
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
  background: var(--bg-primary);
  color: var(--text-primary);
  padding: 8rem 2rem 6rem;
  min-height: 88vh;
  display: flex;
  align-items: center;
  justify-content: center;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Animated gradient background */
.hero-background-accent {
  position: absolute;
  top: -50%;
  right: -15%;
  width: 70%;
  height: 140%;
  background: var(--gradient-subtle);
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.7;
  animation: float 25s ease-in-out infinite;
  z-index: 0;
  pointer-events: none;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) rotate(0deg) scale(1);
  }
  25% {
    transform: translate(-30px, -60px) rotate(3deg) scale(1.05);
  }
  50% {
    transform: translate(20px, 40px) rotate(-2deg) scale(0.95);
  }
  75% {
    transform: translate(-15px, 50px) rotate(4deg) scale(1.02);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1.4fr 1fr;
  gap: 5rem;
  align-items: center;
}

.hero-text {
  text-align: left;
}

.hero h1 {
  font-size: clamp(2.5rem, 5.5vw, 4.25rem);
  font-weight: 700;
  line-height: 1.08;
  margin-bottom: 1.25rem;
  font-style: italic;
  letter-spacing: -0.03em;
  background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: slideInUp 0.9s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: 0.15s;
}

.hero .subtitle {
  font-size: clamp(1rem, 1.8vw, 1.125rem);
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.6;
  font-weight: 500;
  animation: slideInUp 0.9s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: 0.3s;
}

.hero .subtitle a {
  color: var(--accent-primary);
  font-weight: 600;
  transition: all 0.25s ease;
}

.hero .subtitle a:hover {
  color: var(--accent-hover);
}

.hero .intro {
  font-size: clamp(1.05rem, 1.5vw, 1.15rem);
  line-height: 1.75;
  color: var(--text-secondary);
  margin-top: 2rem;
  max-width: 580px;
  font-weight: 400;
  animation: slideInUp 0.9s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: 0.6s;
}

.hero-image-container {
  position: relative;
  animation: slideInRight 1s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: 0.4s;
}

.hero-image {
  width: 100%;
  height: auto;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25),
              0 8px 20px rgba(0, 0, 0, 0.15);
  transform: perspective(1200px) rotateY(-4deg);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.hero-image:hover {
  transform: perspective(1200px) rotateY(0deg) scale(1.02);
  box-shadow: 0 25px 70px rgba(0, 0, 0, 0.3),
              0 10px 25px rgba(0, 0, 0, 0.2);
}

/* Animated Subtitle */
.animated-subtitle {
  margin: 1.75rem 0;
  min-height: 110px;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: center;
  animation: slideInUp 0.9s cubic-bezier(0.4, 0, 0.2, 1) backwards;
  animation-delay: 0.45s;
}

.animated-title {
  font-size: clamp(1.375rem, 2.2vw, 1.625rem);
  font-weight: 700;
  color: var(--accent-primary);
  margin-bottom: 0.5rem;
  font-family: 'Playfair Display', Georgia, serif;
  font-style: italic;
  letter-spacing: -0.02em;
}

.animated-description {
  font-size: clamp(0.9375rem, 1.3vw, 1.0625rem);
  color: var(--text-tertiary);
  opacity: 0.95;
  line-height: 1.5;
  font-weight: 400;
}

.slide-fade-enter-active {
  transition: all 0.75s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

/* Scroll-triggered animations */
@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
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

:deep(.hero-image) {
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
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.12),
              0 3px 10px rgba(0, 0, 0, 0.08);
  border: 1px solid var(--border-color);
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.story-photo):hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 45px rgba(0, 0, 0, 0.15),
              0 5px 15px rgba(0, 0, 0, 0.1);
}

/* Background Section */
.background {
  background: var(--bg-secondary);
  opacity: 0;
  transform: translateY(50px);
  transition: all 0.9s cubic-bezier(0.4, 0, 0.2, 1);
}

.background.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Section container */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem;
}

.container h2 {
  margin-bottom: 3rem;
  font-size: clamp(2rem, 3.5vw, 2.5rem);
  font-weight: 700;
  font-style: italic;
  letter-spacing: -0.025em;
  color: var(--text-primary);
  position: relative;
  padding-bottom: 1rem;
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
}

/* Background/Timeline */
.timeline {
  max-width: 820px;
  margin: 0 auto;
  position: relative;
  padding-left: 3.5rem;
}

/* Timeline vertical line */
.timeline::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 2px;
  background: linear-gradient(180deg,
    var(--accent-primary) 0%,
    var(--accent-secondary) 50%,
    var(--accent-tertiary) 100%
  );
  opacity: 0.6;
}

.timeline-item {
  position: relative;
  margin-bottom: 3.5rem;
  padding: 2.25rem 2.5rem;
  background: var(--bg-card);
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06),
              0 1px 3px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Timeline dot indicator */
.timeline-item::before {
  content: '';
  position: absolute;
  left: -3.5rem;
  top: 2.25rem;
  width: 18px;
  height: 18px;
  background: var(--accent-primary);
  border: 4px solid var(--bg-primary);
  border-radius: 50%;
  box-shadow: 0 0 0 4px var(--accent-primary)30;
  z-index: 1;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.timeline-item:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1),
              0 4px 8px rgba(0, 0, 0, 0.06);
  border-color: var(--accent-primary)40;
}

.timeline-item:hover::before {
  transform: scale(1.35);
  box-shadow: 0 0 0 8px var(--accent-primary)40;
  background: var(--accent-hover);
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.125rem;
  gap: 1.25rem;
  flex-wrap: wrap;
}

.timeline-item h3 {
  color: var(--text-primary);
  margin: 0;
  font-size: clamp(1.25rem, 2vw, 1.5rem);
  font-weight: 700;
  letter-spacing: -0.02em;
  line-height: 1.3;
}

.timeline-date {
  color: var(--accent-primary);
  font-size: 0.9375rem;
  font-weight: 600;
  white-space: nowrap;
  letter-spacing: -0.01em;
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

/* Responsive */
@media (max-width: 968px) {
  .hero {
    padding: 6rem 2rem 4rem;
    min-height: 75vh;
  }

  .hero-content {
    grid-template-columns: 1fr;
    gap: 3.5rem;
  }

  .hero-text {
    text-align: center;
  }

  .hero .intro {
    max-width: 100%;
  }

  .animated-subtitle {
    align-items: center;
  }

  .hero-image {
    transform: perspective(1200px) rotateY(0deg);
    max-width: 400px;
    margin: 0 auto;
  }

  .story-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .timeline {
    padding-left: 2.5rem;
  }

  .timeline-item::before {
    left: -2.5rem;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 4rem 1.5rem 3rem;
  }

  .container {
    padding: 3.5rem 1.5rem;
  }

  .timeline {
    padding-left: 2rem;
  }

  .timeline-item {
    padding: 1.75rem 1.5rem;
  }

  .timeline-item::before {
    left: -2rem;
    width: 14px;
    height: 14px;
  }

  .timeline-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
}
</style>
