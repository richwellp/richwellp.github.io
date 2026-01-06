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
            <li>Built a full-stack analytics platform with Node.js, MongoDB, and Python to visualize
            and analyze GPA data across 10+ years, enabling students to compare instructors and
            predict course outcomes.</li>
            <li>Trained ML models (linear/logistic regression, sequential models) and visualizations
            for predictive grade analytics.</li>
            <li>Analyzed and designed interactive data visualizations for users to track performance
            across semesters and predict future grades.</li>
            <li>Implemented user authentication and automated data processing pipelines for efficient
            data handling.</li>
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
            <li>Integrated weapon detection with anomaly scores, improving crime classification
            accuracy through multi-model decision-making.</li>
            <li>Developed an AI pipeline using UCF-Crime anomaly detection & YOLO/Faster R-CNN for
            real-time crime recognition.</li>
            <li>Optimized anomaly detection using Multi-Instance Learning (MIL) & improved loss
            functions for better predictions.</li>
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
            <li>Engineered a transformer and Encoder/Decoder models to capture temporal patterns in
            climate-relevant aerosol properties.</li>
            <li>Applied advanced data preprocessing techniques to handle high-dimensional climate data
            and reduce the curse of dimensionality.</li>
            <li>Leveraged HAL 9000 (UIUC's supercomputer) for high-performance training, optimizing
            deep learning workload scalability.</li>
          </ul>
          <div class="tech-stack">
            <span class="tech-tag">PyTorch</span>
            <span class="tech-tag">Transformers</span>
            <span class="tech-tag">Climate Data</span>
            <span class="tech-tag">HPC</span>
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
  gap: 2.5rem;
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

.award-badge {
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

.award-badge:hover {
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
