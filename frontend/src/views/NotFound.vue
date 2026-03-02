<template>
  <div class="not-found">
    <div class="container">
      <div class="error-display">
        <div class="glitch-wrapper" aria-label="Error 404">
          <span class="glitch" data-text="404">404</span>
        </div>
        <div class="terminal-line">
          <span class="prompt">~/richwellp $</span>
          <span class="cmd"> cd {{ requestedPath }}</span>
          <span class="blink-cursor">▋</span>
        </div>
        <div class="terminal-output">
          <span class="err-prefix">bash:</span> <span class="err-path">{{ requestedPath }}</span>: No such file or directory
        </div>
      </div>

      <h1>Signal Lost</h1>
      <p class="message">
        The page you're looking for has drifted out of range.
        It may have been moved, deleted, or never existed.
      </p>

      <div class="nav-links">
        <router-link to="/" class="nav-btn primary">← Return Home</router-link>
        <router-link to="/experience" class="nav-btn">Experience</router-link>
        <router-link to="/projects" class="nav-btn">Projects</router-link>
        <router-link to="/contact" class="nav-btn">Contact</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, RouterLink } from 'vue-router'

const route = useRoute()
const requestedPath = computed(() => route.path)
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  background: var(--bg-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  position: relative;
  overflow: hidden;
}

/* Subtle radial glow behind content */
.not-found::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: min(700px, 120vw);
  height: min(700px, 120vw);
  background: radial-gradient(circle, color-mix(in srgb, var(--accent-primary) 5%, transparent) 0%, transparent 65%);
  pointer-events: none;
}

.container {
  max-width: 680px;
  width: 100%;
  text-align: center;
  position: relative;
  z-index: 1;
  opacity: 0;
  animation: reveal 0.7s cubic-bezier(0.4, 0, 0.2, 1) 0.1s both;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(28px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ── Glitch 404 ── */
.error-display {
  margin-bottom: 3rem;
}

.glitch-wrapper {
  margin-bottom: 1.75rem;
  line-height: 1;
}

.glitch {
  font-family: 'Urbanist', sans-serif;
  font-size: clamp(6rem, 18vw, 11rem);
  font-weight: 800;
  color: var(--accent-primary);
  letter-spacing: -0.06em;
  position: relative;
  display: inline-block;
  text-shadow: 0 0 40px color-mix(in srgb, var(--accent-primary) 28%, transparent);
  animation: glitch-base 6s ease-in-out infinite;
}

.glitch::before,
.glitch::after {
  content: attr(data-text);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  font-family: inherit;
  font-size: inherit;
  font-weight: inherit;
  letter-spacing: inherit;
}

.glitch::before {
  color: #ff8000;
  clip-path: polygon(0 20%, 100% 20%, 100% 40%, 0 40%);
  animation: glitch-top 6s ease-in-out infinite;
  opacity: 0;
}

.glitch::after {
  color: #ff3860;
  clip-path: polygon(0 60%, 100% 60%, 100% 80%, 0 80%);
  animation: glitch-bot 6s ease-in-out infinite;
  opacity: 0;
}

@keyframes glitch-base {
  0%, 88%, 100% { transform: none; }
  90%           { transform: skewX(-3deg); }
  92%           { transform: skewX(2deg); }
  94%           { transform: none; }
}

@keyframes glitch-top {
  0%, 88%, 100% { opacity: 0; transform: none; }
  89%           { opacity: 0.85; transform: translateX(-6px); }
  91%           { opacity: 0.85; transform: translateX(5px); }
  93%           { opacity: 0; }
}

@keyframes glitch-bot {
  0%, 88%, 100% { opacity: 0; transform: none; }
  90%           { opacity: 0.7; transform: translateX(6px); }
  92%           { opacity: 0.7; transform: translateX(-4px); }
  94%           { opacity: 0; }
}

/* ── Terminal block ── */
.terminal-line {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: clamp(0.8125rem, 1.2vw, 0.9375rem);
  color: var(--text-tertiary);
  text-align: left;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px 8px 0 0;
  padding: 0.75rem 1.25rem;
  border-bottom: none;
  position: relative;
}

.terminal-line::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 8px 8px 0 0;
}

.prompt {
  color: var(--accent-primary);
  font-weight: 600;
}

.cmd {
  color: var(--text-secondary);
}

.blink-cursor {
  color: var(--accent-primary);
  animation: blink 1s step-end infinite;
  font-weight: 700;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

.terminal-output {
  font-family: 'JetBrains Mono', 'Fira Code', monospace;
  font-size: clamp(0.75rem, 1.1vw, 0.875rem);
  text-align: left;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: 0 0 8px 8px;
  padding: 0.625rem 1.25rem;
  color: var(--text-tertiary);
}

.err-prefix {
  color: #ef4444;
  font-weight: 600;
}

.err-path {
  color: #ff8000;
}

/* ── Heading ── */
h1 {
  font-family: 'Urbanist', sans-serif;
  font-size: clamp(2rem, 4vw, 2.75rem);
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.035em;
  margin-bottom: 1.25rem;
  position: relative;
  padding-bottom: 1.25rem;
}

h1::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 48px;
  height: 3px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  border-radius: 2px;
  box-shadow: 0 0 8px color-mix(in srgb, var(--accent-primary) 50%, transparent);
  animation: lineExpand 0.45s cubic-bezier(0.4, 0, 0.2, 1) 0.7s both;
}

@keyframes lineExpand {
  from { width: 0; opacity: 0; }
  to   { width: 48px; opacity: 1; }
}

.message {
  font-size: clamp(1rem, 1.3vw, 1.0625rem);
  color: var(--text-secondary);
  line-height: 1.7;
  max-width: 480px;
  margin: 0 auto 3rem;
  font-weight: 400;
}

/* ── Nav links ── */
.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  align-items: center;
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: clamp(0.875rem, 1.1vw, 0.9375rem);
  font-weight: 600;
  letter-spacing: -0.01em;
  text-decoration: none;
  transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1.5px solid color-mix(in srgb, var(--accent-primary) 30%, transparent);
  color: var(--accent-primary);
  background: var(--bg-card);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transition: left 0.5s ease;
}

@media (hover: hover) {
  .nav-btn:hover {
    background: color-mix(in srgb, var(--accent-primary) 12%, var(--bg-card));
    border-color: var(--accent-primary);
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4),
                0 0 20px rgba(129, 140, 248, 0.15);
  }
}

.nav-btn:hover::before {
  left: 100%;
}

.nav-btn.primary {
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  color: #05060f;
  border-color: transparent;
  font-weight: 700;
  box-shadow: 0 4px 16px rgba(129, 140, 248, 0.25);
}

.nav-btn.primary:hover {
  background: linear-gradient(135deg, var(--accent-hover) 0%, var(--accent-primary) 100%);
  color: #05060f;
  box-shadow: 0 8px 28px rgba(129, 140, 248, 0.35),
              0 4px 10px rgba(0, 0, 0, 0.2);
}

/* ── Responsive ── */
@media (max-width: 640px) {
  .not-found {
    padding: 3rem 1.5rem;
  }

  .terminal-line,
  .terminal-output {
    font-size: 0.75rem;
    padding-left: 1rem;
    padding-right: 1rem;
  }

  .nav-links {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-btn {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .not-found {
    padding: 2.5rem 1.25rem;
  }
}
</style>
