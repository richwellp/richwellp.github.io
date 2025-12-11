<template>
  <div class="about-me">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <img src="/assets/photos/professional/professional_1.jpg" alt="Richwell Perez" class="hero-image" />
        <h1>Richwell Cyrille Santos Perez</h1>
        <p class="subtitle">Computer Science Enthusiast | AI Engineer</p>
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
            <h3>Engineering Science Background</h3>
            <p>
              I started with an Engineering Science degree at Parkland College, where I gained
              hands-on engineering experience that shaped my problem-solving approach.
            </p>
          </div>
          <div class="timeline-item">
            <h3>University of Illinois Urbana-Champaign</h3>
            <p>
              <strong>Bachelor of Science in Computer Science with Honors</strong> (2018-2023, GPA:
              3.81)
            </p>
            <p><strong>Master of Computer Science</strong> (2022-2023, GPA: 3.52)</p>
          </div>
          <div class="timeline-item">
            <h3>Current: AI Engineer at Safran</h3>
            <p>
              Building full-stack RAG chatbots, developing predictive maintenance systems, and
              creating AI-driven automation tools for enterprise applications.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Interests -->
    <section class="interests">
      <div class="container">
        <h2>Beyond the Code</h2>
        <div class="interests-grid">
          <div class="interest-card">
            <h3>🏐 Volleyball</h3>
            <p>I love the strategy and teamwork that goes into every match.</p>
          </div>
          <div class="interest-card">
            <h3>💪 Powerlifting</h3>
            <p>Building strength and discipline, one rep at a time.</p>
          </div>
          <div class="interest-card">
            <h3>🎮 Gaming</h3>
            <p>Dota 2, Valorant, and anime games—where my AI interest began.</p>
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

<script setup></script>

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
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
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
  margin-bottom: 2.5rem;
  padding: 1.5rem;
  background: var(--bg-card);
  border-left: 4px solid var(--accent-primary);
  border-radius: 8px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.timeline-item h3 {
  color: var(--text-primary);
  margin-bottom: 0.75rem;
  font-size: 1.3rem;
}

.timeline-item p {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 0.5rem;
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
