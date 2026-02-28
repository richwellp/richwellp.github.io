<template>
  <div class="contact">

    <!-- ── Hero: left-aligned, editorial ── -->
    <section class="contact-hero">
      <div class="hero-inner">

        <p class="availability-label">
          <span class="status-dot"></span>
          {{ content.availabilityLabel }}
        </p>

        <h1>Let's work<br><em>together.</em></h1>

        <p class="hero-sub">{{ content.contactHeroSub }}</p>

        <!-- Primary CTA: email -->
        <a
          :href="`mailto:${CONTACT.email}`"
          class="email-cta"
          @click="trackExternalLink('email')"
        >
          <span class="cta-meta">// EMAIL</span>
          <span class="cta-address">{{ CONTACT.email }}</span>
          <svg class="cta-arrow" viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12"></line>
            <polyline points="12 5 19 12 12 19"></polyline>
          </svg>
        </a>

        <!-- Secondary: social pills -->
        <div class="social-row">
          <a
            :href="CONTACT.github"
            target="_blank"
            rel="noopener noreferrer"
            class="social-pill"
            @click="trackExternalLink('github')"
          >
            <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            GitHub
          </a>
          <a
            :href="CONTACT.linkedin"
            target="_blank"
            rel="noopener noreferrer"
            class="social-pill"
            @click="trackExternalLink('linkedin')"
          >
            <svg viewBox="0 0 24 24" width="15" height="15" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            LinkedIn
          </a>
        </div>

      </div>
    </section>

    <!-- ── Message form ── -->
    <section class="form-section">
      <div class="form-container">

        <div class="form-header">
          <h2>Send a message</h2>
          <p>Prefer to write something longer? I read every message.</p>
        </div>

        <!-- Success -->
        <div v-if="formStatus === 'success'" class="status-message success">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <p>Sent! I'll get back to you soon.</p>
        </div>

        <!-- Error -->
        <div v-if="formStatus === 'error'" class="status-message error">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="15" y1="9" x2="9" y2="15"></line>
            <line x1="9" y1="9" x2="15" y2="15"></line>
          </svg>
          <p>Something went wrong. Email me directly at <a :href="`mailto:${CONTACT.email}`">{{ CONTACT.email }}</a></p>
        </div>

        <form
          v-show="formStatus !== 'success'"
          @submit.prevent="handleSubmit"
          class="contact-form"
          ref="contactForm"
        >
          <div class="form-row">
            <div class="form-group">
              <label for="name">Name</label>
              <input
                type="text"
                id="name"
                v-model="formData.name"
                required
                placeholder="Your name"
                :disabled="formStatus === 'submitting'"
              />
            </div>
            <div class="form-group">
              <label for="email">Email</label>
              <input
                type="email"
                id="email"
                v-model="formData.email"
                required
                placeholder="your@email.com"
                :disabled="formStatus === 'submitting'"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="subject">Subject</label>
            <input
              type="text"
              id="subject"
              v-model="formData.subject"
              required
              placeholder="What's this about?"
              :disabled="formStatus === 'submitting'"
            />
          </div>

          <div class="form-group">
            <label for="message">Message</label>
            <textarea
              id="message"
              v-model="formData.message"
              required
              rows="5"
              placeholder="Tell me about your project, opportunity, or question..."
              :disabled="formStatus === 'submitting'"
            ></textarea>
            <span class="char-count" :class="{ warn: formData.message.length > 1800 }">
              {{ formData.message.length }} / 2000
            </span>
          </div>

          <button
            type="submit"
            class="submit-btn"
            :disabled="formStatus === 'submitting' || formData.message.length > 2000"
          >
            <span v-if="formStatus === 'submitting'">Sending...</span>
            <span v-else>Send message →</span>
          </button>
        </form>

      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAnalytics } from '../composables/useAnalytics'
import { CONTACT } from '../config/contact'
import { useProfessionalInfo } from '../composables/useProfessionalInfo'

const { trackContactForm, trackExternalLink } = useAnalytics()
const { content, loadProfessionalInfo } = useProfessionalInfo()

onMounted(async () => {
  await loadProfessionalInfo()
})

// Form state
const formData = reactive({ name: '', email: '', subject: '', message: '' })
const formStatus = ref('')

const FORMSPREE_ENDPOINT = 'https://formspree.io/f/mojnpkvk'

const handleSubmit = async () => {
  if (formData.message.length > 2000) {
    formStatus.value = 'error'
    setTimeout(() => { formStatus.value = '' }, 5000)
    return
  }

  formStatus.value = 'submitting'

  try {
    const response = await fetch(FORMSPREE_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      formStatus.value = 'success'
      trackContactForm('success')
      formData.name = ''
      formData.email = ''
      formData.subject = ''
      formData.message = ''
      setTimeout(() => { formStatus.value = '' }, 10000)
    } else {
      formStatus.value = 'error'
      trackContactForm('error')
      setTimeout(() => { formStatus.value = '' }, 5000)
    }
  } catch (error) {
    console.error('Form submission error:', error)
    formStatus.value = 'error'
    trackContactForm('network_error')
    setTimeout(() => { formStatus.value = '' }, 5000)
  }
}
</script>

<style scoped>
.contact {
  width: 100%;
}

/* ── Hero ── */
.contact-hero {
  background: var(--bg-primary);
  background-image:
    repeating-linear-gradient(0deg, transparent, transparent 39px, rgba(129, 140, 248, 0.025) 39px, rgba(129, 140, 248, 0.025) 40px),
    repeating-linear-gradient(90deg, transparent, transparent 39px, rgba(129, 140, 248, 0.025) 39px, rgba(129, 140, 248, 0.025) 40px);
  min-height: 72vh;
  display: flex;
  align-items: center;
  padding: 6rem 2rem 5rem;
  position: relative;
  overflow: hidden;
  border-bottom: 1px solid var(--border-color);
}

/* Teal radial glow — top-left */
.contact-hero::before {
  content: '';
  position: absolute;
  top: -20%;
  left: -10%;
  width: 60%;
  height: 130%;
  background: radial-gradient(ellipse at 30% 40%, rgba(129, 140, 248, 0.1) 0%, rgba(129, 140, 248, 0.03) 45%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

.hero-inner {
  position: relative;
  z-index: 1;
  max-width: 820px;
  margin: 0 auto;
  width: 100%;
}

/* Availability badge */
.availability-label {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  color: var(--accent-primary);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-weight: 500;
  margin-bottom: 1.75rem;
  opacity: 0;
  animation: heroReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.1s both;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent-primary);
  box-shadow: 0 0 8px rgba(129, 140, 248, 0.7);
  animation: blink 2.5s ease-in-out infinite;
  flex-shrink: 0;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.3; }
}

@keyframes heroReveal {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

h1 {
  font-size: clamp(3rem, 7vw, 5.5rem);
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.1;
  color: var(--text-primary);
  margin: 0 0 1.5rem;
  opacity: 0;
  animation: heroReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.2s both;
}

h1 em {
  font-style: italic;
  color: var(--accent-primary);
}

.hero-sub {
  font-size: clamp(1rem, 1.4vw, 1.125rem);
  color: var(--text-secondary);
  line-height: 1.65;
  margin: 0 0 2.75rem;
  font-weight: 400;
  max-width: 500px;
  opacity: 0;
  animation: heroReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.3s both;
}

/* ── Primary email CTA ── */
.email-cta {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1.25rem 1.75rem;
  background: color-mix(in srgb, var(--accent-primary) 4%, var(--bg-card));
  border: 1px solid color-mix(in srgb, var(--accent-primary) 18%, transparent);
  border-left: 3px solid var(--accent-primary);
  border-radius: 10px;
  text-decoration: none;
  max-width: 520px;
  margin-bottom: 1.75rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  animation: heroReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.4s both;
}

.email-cta:hover {
  background: color-mix(in srgb, var(--accent-primary) 10%, var(--bg-card));
  border-color: var(--accent-primary);
  transform: translateX(6px);
  box-shadow: 0 8px 28px rgba(0, 0, 0, 0.35), 0 0 20px rgba(129, 140, 248, 0.07);
}

.cta-meta {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent-primary);
  opacity: 0.55;
  flex-shrink: 0;
}

.cta-address {
  font-family: 'JetBrains Mono', monospace;
  font-size: clamp(0.875rem, 1.3vw, 1rem);
  color: var(--text-primary);
  font-weight: 500;
  letter-spacing: -0.01em;
  flex: 1;
}

.cta-arrow {
  color: var(--accent-primary);
  flex-shrink: 0;
  transition: transform 0.25s ease;
}

.email-cta:hover .cta-arrow {
  transform: translateX(4px);
}

/* ── Social pills ── */
.social-row {
  display: flex;
  gap: 0.625rem;
  flex-wrap: wrap;
  opacity: 0;
  animation: heroReveal 0.6s cubic-bezier(0.4, 0, 0.2, 1) 0.5s both;
}

.social-pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5625rem 1.125rem;
  border-radius: 8px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.social-pill:hover {
  background: var(--accent-primary);
  border-color: var(--accent-primary);
  color: #05060f;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(129, 140, 248, 0.22);
}

/* ── Message form section ── */
.form-section {
  background: var(--bg-secondary);
  padding: 5rem 2rem;
  border-top: 1px solid var(--border-color);
}

.form-container {
  max-width: 740px;
  margin: 0 auto;
}

.form-header {
  margin-bottom: 2.5rem;
}

.form-header h2 {
  font-size: clamp(1.75rem, 3vw, 2.25rem);
  font-weight: 800;
  letter-spacing: -0.035em;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
}

.form-header p {
  color: var(--text-secondary);
  font-size: clamp(0.9375rem, 1.2vw, 1rem);
  margin: 0;
  line-height: 1.6;
}

/* Status messages */
.status-message {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 1rem 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.75rem;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  animation: slideDown 0.45s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}

.status-message.success {
  background: color-mix(in srgb, var(--accent-primary) 8%, var(--bg-card));
  border: 1px solid color-mix(in srgb, var(--accent-primary) 30%, transparent);
  border-left: 3px solid var(--accent-primary);
  color: var(--accent-primary);
}

.status-message.error {
  background: rgba(220, 38, 38, 0.08);
  border: 1px solid rgba(220, 38, 38, 0.3);
  border-left: 3px solid #dc2626;
  color: #ef4444;
}

.status-message svg { flex-shrink: 0; }
.status-message p { margin: 0; font-weight: 500; line-height: 1.5; }
.status-message a { color: inherit; text-decoration: underline; }

/* Form */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4375rem;
  position: relative;
}

.form-group label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  font-weight: 500;
  color: var(--text-tertiary);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.form-group input,
.form-group textarea {
  padding: 0.875rem 1.125rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  background: var(--bg-card);
  color: var(--text-primary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-family: 'Nunito', system-ui, sans-serif;
  transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--text-tertiary);
  opacity: 0.55;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 130px;
  line-height: 1.65;
}

.char-count {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--text-tertiary);
  text-align: right;
  letter-spacing: 0.03em;
  transition: color 0.25s ease;
}

.char-count.warn {
  color: var(--accent-secondary);
}

.submit-btn {
  align-self: flex-start;
  padding: 0.9375rem 2rem;
  background: var(--accent-primary);
  color: #05060f;
  border: none;
  border-radius: 8px;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-weight: 700;
  cursor: pointer;
  letter-spacing: -0.01em;
  font-family: 'Urbanist', sans-serif;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.submit-btn:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(129, 140, 248, 0.3);
}

.submit-btn:active:not(:disabled) {
  transform: translateY(0);
}

.submit-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .contact-hero {
    padding: 4.5rem 1.5rem 4rem;
    min-height: auto;
  }

  h1 {
    font-size: clamp(2.5rem, 8vw, 3.5rem);
  }

  .email-cta {
    max-width: 100%;
  }

  .form-section {
    padding: 3.5rem 1.5rem;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  .submit-btn {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .contact-hero {
    padding: 4rem 1.25rem 3.5rem;
  }

  h1 {
    font-size: clamp(2.25rem, 10vw, 3rem);
  }

  .form-section {
    padding: 3rem 1.25rem;
  }
}
</style>
