<template>
  <div class="cv">
    <div class="container">
      <h1>Curriculum Vitae</h1>
      <p class="page-intro">
        You can view my one-page resume below or download it
        using your browser's built-in PDF controls.
      </p>

      <div class="pdf-container">
        <embed
          src="/assets/Resume.pdf"
          type="application/pdf"
          width="100%"
          height="1000px"
          class="pdf-embed"
        />
      </div>

      <div class="note">
        <p>
          <strong>Note:</strong> If the PDF doesn't display, you can
          <a href="/assets/Resume.pdf" target="_blank">open it in a new tab</a>.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup></script>

<style scoped>
.cv {
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  opacity: 0;
  animation: fadeInUp 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.2s forwards;
}

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
  margin-bottom: 3.5rem;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.pdf-container {
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1),
              0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border-color);
  overflow: hidden;
  margin-bottom: 2.5rem;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}

.pdf-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  z-index: 1;
}

.pdf-container:hover {
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12),
              0 4px 12px rgba(0, 0, 0, 0.08);
  transform: translateY(-2px);
}

.pdf-embed {
  display: block;
  border: none;
}

.note {
  text-align: center;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
  padding: 1.75rem 2rem;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  border: 1px solid var(--border-color);
  border-left: 5px solid var(--accent-primary);
}

.note p {
  color: var(--text-secondary);
  margin: 0;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.65;
  font-weight: 400;
}

.note strong {
  color: var(--text-primary);
  font-weight: 600;
}

.note a {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  letter-spacing: -0.01em;
}

.note a:hover {
  color: var(--accent-hover);
  text-decoration: underline;
  text-decoration-color: var(--accent-primary);
  text-decoration-thickness: 2px;
  text-underline-offset: 3px;
}

/* Responsive */
@media (max-width: 768px) {
  .cv {
    padding: 3.5rem 1.5rem;
  }

  .page-intro {
    margin-bottom: 3rem;
  }

  .pdf-embed {
    height: 800px;
  }

  .note {
    padding: 1.5rem;
  }
}

@media (max-width: 480px) {
  .cv {
    padding: 3rem 1.25rem;
  }

  .pdf-embed {
    height: 700px;
  }
}
</style>
