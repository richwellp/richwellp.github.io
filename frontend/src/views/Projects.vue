<template>
  <div class="projects">
    <div class="container">
      <h1>Projects</h1>
      <p class="page-intro">
        A showcase of my personal and academic projects, demonstrating my expertise in AI, full-stack development, and software engineering.
      </p>

      <div class="projects-grid">
        <!-- UIUC Letter Grades -->
        <div class="project-block">
          <div class="project-header">
            <h3>UIUC Letter Grades</h3>
            <p class="project-subtitle">Full-Stack Web App with AI Integration</p>
          </div>
          <p class="project-description">
            Built a full-stack analytics platform to help students make informed decisions about
            their courses by visualizing historical GPA data and predicting outcomes.
          </p>
          <ul class="project-highlights">
            <li>Built analytics platform with Node.js, MongoDB, and Python to visualize GPA data across 10+ years</li>
            <li>Trained ML models (linear/logistic regression, sequential models) for predictive grade analytics</li>
            <li>Designed interactive data visualizations for tracking performance across semesters</li>
            <li>Implemented user authentication and automated data processing pipelines</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">Node.js</span>
            <span class="tech-tag">MongoDB</span>
            <span class="tech-tag">Python</span>
            <span class="tech-tag">TensorFlow</span>
            <span class="tech-tag">Data Visualization</span>
          </div>
        </div>

        <!-- Video Anomaly Detection -->
        <div class="project-block">
          <div class="project-header">
            <h3>Video Anomaly Detection Model</h3>
            <p class="project-subtitle">Leveraging Weapon Recognition for Enhanced Accuracy</p>
          </div>
          <p class="project-description">
            Developed an AI pipeline for real-time crime detection in surveillance videos, combining
            anomaly detection with weapon recognition.
          </p>
          <ul class="project-highlights">
            <li>Integrated weapon detection with anomaly scores for improved crime classification</li>
            <li>Developed AI pipeline using UCF-Crime anomaly detection & YOLO/Faster R-CNN</li>
            <li>Optimized anomaly detection using Multi-Instance Learning (MIL) & improved loss functions</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">PyTorch</span>
            <span class="tech-tag">YOLO</span>
            <span class="tech-tag">Faster R-CNN</span>
            <span class="tech-tag">Computer Vision</span>
            <span class="tech-tag">MIL</span>
          </div>
        </div>

        <!-- Deep Learning Aerosol Model -->
        <div class="project-block">
          <div class="project-header">
            <h3>Deep Learning Aerosol Model</h3>
            <p class="project-subtitle">NCSA AI Innovation Hackathon</p>
            <a href="https://ai.ncsa.illinois.edu/center-for-ai-innovation-announces-hackathon-winners/" target="_blank" rel="noopener noreferrer" class="award-badge">
              🏆 3rd Place, Ashby Prize in Computational Science
            </a>
          </div>
          <p class="project-description">
            Engineered deep learning models to predict climate-relevant aerosol properties using
            high-performance computing infrastructure.
          </p>
          <ul class="project-highlights">
            <li>Engineered transformer and Encoder/Decoder models to capture temporal patterns in aerosol properties</li>
            <li>Applied advanced preprocessing techniques to handle high-dimensional climate data</li>
            <li>Leveraged HAL 9000 (UIUC's supercomputer) for high-performance training</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">PyTorch</span>
            <span class="tech-tag">Transformers</span>
            <span class="tech-tag">Climate Data</span>
            <span class="tech-tag">HPC</span>
          </div>
        </div>

        <!-- COVID Logging System -->
        <div class="project-block">
          <div class="project-header">
            <h3>COVID Logging System</h3>
            <p class="project-subtitle">Database Systems Project</p>
            <a href="https://github.com/richwellp/CS411_Project" target="_blank" rel="noopener noreferrer" class="github-link">
              View on GitHub →
            </a>
          </div>
          <p class="project-description">
            Built a comprehensive COVID-19 tracking and logging system with database management for monitoring cases and contact tracing.
          </p>
          <ul class="project-highlights">
            <li>Designed relational database schema for COVID case management and contact tracing</li>
            <li>Implemented CRUD operations with complex queries for data analysis</li>
            <li>Built web interface for real-time case logging and reporting</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">SQL</span>
            <span class="tech-tag">Database Design</span>
            <span class="tech-tag">Python</span>
            <span class="tech-tag">Web Development</span>
          </div>
        </div>

        <!-- Not Geoff - Facial Recognition -->
        <div class="project-block">
          <div class="project-header">
            <h3>Not Geoff</h3>
            <p class="project-subtitle">Facial Recognition System</p>
            <a href="https://github.com/richwellp/Not-Geoff" target="_blank" rel="noopener noreferrer" class="github-link">
              View on GitHub →
            </a>
          </div>
          <p class="project-description">
            Developed a facial recognition system using computer vision techniques to identify and verify individuals.
          </p>
          <ul class="project-highlights">
            <li>Implemented face detection and recognition using OpenCV and deep learning models</li>
            <li>Built real-time video processing pipeline for face identification</li>
            <li>Trained custom models for improved accuracy on specific datasets</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">Python</span>
            <span class="tech-tag">OpenCV</span>
            <span class="tech-tag">Computer Vision</span>
            <span class="tech-tag">Deep Learning</span>
          </div>
        </div>

        <!-- Rocket Rollers -->
        <div class="project-block">
          <div class="project-header">
            <h3>Rocket Rollers</h3>
            <p class="project-subtitle">Game Development Project</p>
            <a href="https://github.com/richwellp/Rocket-Rollers" target="_blank" rel="noopener noreferrer" class="github-link">
              View on GitHub →
            </a>
          </div>
          <p class="project-description">
            Created an interactive game featuring physics-based mechanics and dynamic gameplay elements.
          </p>
          <ul class="project-highlights">
            <li>Implemented game physics engine with collision detection and response</li>
            <li>Designed level progression system with increasing difficulty</li>
            <li>Built responsive controls and smooth animation systems</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">Unity</span>
            <span class="tech-tag">C#</span>
            <span class="tech-tag">Game Development</span>
            <span class="tech-tag">Physics</span>
          </div>
        </div>

        <!-- Open Flights -->
        <div class="project-block">
          <div class="project-header">
            <h3>Open Flights</h3>
            <p class="project-subtitle">Flight Data Analysis Platform</p>
            <a href="https://github.com/richwellp/Open-Flights" target="_blank" rel="noopener noreferrer" class="github-link">
              View on GitHub →
            </a>
          </div>
          <p class="project-description">
            Built a data analysis platform for visualizing and analyzing global flight routes and airport data.
          </p>
          <ul class="project-highlights">
            <li>Processed and visualized large-scale flight route datasets</li>
            <li>Implemented interactive maps for exploring flight connections</li>
            <li>Built analytics dashboard for route optimization and statistics</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">Python</span>
            <span class="tech-tag">Data Analysis</span>
            <span class="tech-tag">Visualization</span>
            <span class="tech-tag">Pandas</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
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
