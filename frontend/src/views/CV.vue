<template>
  <div class="cv">
    <div class="container">
      <h1>Curriculum Vitae</h1>
      <p class="page-intro">
        My one-page resume, optimized for job applications. You can view it below or download it
        using your browser's built-in PDF controls (right-click → Save).
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

.pdf-container {
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 4px 20px var(--shadow);
  border: 1px solid var(--border-color);
  overflow: hidden;
  margin-bottom: 2rem;
}

.pdf-embed {
  display: block;
  border: none;
}

.note {
  text-align: center;
  background: var(--bg-card);
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.note p {
  color: var(--text-secondary);
  margin: 0;
}

.note a {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
}

.note a:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
  .cv {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .pdf-embed {
    height: 800px;
  }
}
</style>
