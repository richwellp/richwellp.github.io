<template>
  <div class="contact">
    <div class="container">
      <h1>Get in Touch</h1>
      <p class="page-intro">
        I'm always open to discussing new opportunities, collaborations, or just chatting about technology and AI.
        Feel free to reach out!
      </p>

      <div class="contact-content">
        <!-- Contact Form -->
        <div class="contact-form-section">
          <h2>Send Me a Message</h2>

          <!-- Success Message -->
          <div v-if="formStatus === 'success'" class="status-message success">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
            <p>Thank you! Your message has been sent successfully. I'll get back to you soon!</p>
          </div>

          <!-- Error Message -->
          <div v-if="formStatus === 'error'" class="status-message error">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="15" y1="9" x2="9" y2="15"></line>
              <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>
            <p>Oops! Something went wrong. Please try again or email me directly at {{ CONTACT.email }}</p>
          </div>

          <!-- Contact Form -->
          <form
            v-show="formStatus !== 'success'"
            @submit.prevent="handleSubmit"
            class="contact-form"
            ref="contactForm"
          >
            <div class="form-group">
              <label for="name">Your Name *</label>
              <input
                type="text"
                id="name"
                v-model="formData.name"
                required
                placeholder="John Doe"
                :disabled="formStatus === 'submitting'"
              />
            </div>

            <div class="form-group">
              <label for="email">Your Email *</label>
              <input
                type="email"
                id="email"
                v-model="formData.email"
                required
                placeholder="john@example.com"
                :disabled="formStatus === 'submitting'"
              />
            </div>

            <div class="form-group">
              <label for="subject">Subject *</label>
              <input
                type="text"
                id="subject"
                v-model="formData.subject"
                required
                placeholder="Job Opportunity / Collaboration / General Inquiry"
                :disabled="formStatus === 'submitting'"
              />
            </div>

            <div class="form-group">
              <label for="message">Message *</label>
              <textarea
                id="message"
                v-model="formData.message"
                required
                rows="6"
                placeholder="Tell me about your inquiry, project, or opportunity..."
                :disabled="formStatus === 'submitting'"
              ></textarea>
              <span class="char-count">{{ formData.message.length }} / 2000</span>
            </div>

            <button
              type="submit"
              class="submit-btn"
              :disabled="formStatus === 'submitting' || formData.message.length > 2000"
            >
              <span v-if="formStatus === 'submitting'">Sending...</span>
              <span v-else>Send Message</span>
            </button>
          </form>
        </div>

        <!-- Contact Info -->
        <div class="contact-info">
          <h2>Other Ways to Connect</h2>

          <div class="info-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            <div>
              <h3>Email</h3>
              <a :href="`mailto:${CONTACT.email}`" @click="trackExternalLink('email')">
                {{ CONTACT.email }}
              </a>
            </div>
          </div>

          <div class="info-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
            </svg>
            <div>
              <h3>LinkedIn</h3>
              <a
                :href="CONTACT.linkedin"
                target="_blank"
                rel="noopener noreferrer"
                @click="trackExternalLink('linkedin')"
              >
                {{ CONTACT.linkedin.replace('https://www.', '') }}
              </a>
            </div>
          </div>

          <div class="info-card">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
            </svg>
            <div>
              <h3>GitHub</h3>
              <a
                :href="CONTACT.github"
                target="_blank"
                rel="noopener noreferrer"
                @click="trackExternalLink('github')"
              >
                {{ CONTACT.github.replace('https://', '') }}
              </a>
            </div>
          </div>

          <div class="response-time">
            <p>
              <strong>⏱️ Response Time:</strong> I typically respond within 24-48 hours.
              For urgent matters, please mention it in your subject line.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAnalytics } from '../composables/useAnalytics'
import { CONTACT } from '../config/contact'

const { trackContactForm, trackExternalLink } = useAnalytics()

// Form data
const formData = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const formStatus = ref('') // '', 'submitting', 'success', 'error'
const contactForm = ref(null)

// Formspree endpoint (you'll need to replace this with your actual endpoint)
const FORMSPREE_ENDPOINT = 'https://formspree.io/f/mojnpkvk'

const handleSubmit = async () => {
  // Validate message length
  if (formData.message.length > 2000) {
    formStatus.value = 'error'
    setTimeout(() => {
      formStatus.value = ''
    }, 5000)
    return
  }

  formStatus.value = 'submitting'

  try {
    const response = await fetch(FORMSPREE_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })

    if (response.ok) {
      formStatus.value = 'success'
      trackContactForm('success')

      // Reset form
      formData.name = ''
      formData.email = ''
      formData.subject = ''
      formData.message = ''

      // Reset success message after 10 seconds
      setTimeout(() => {
        formStatus.value = ''
      }, 10000)
    } else {
      formStatus.value = 'error'
      trackContactForm('error')

      setTimeout(() => {
        formStatus.value = ''
      }, 5000)
    }
  } catch (error) {
    console.error('Form submission error:', error)
    formStatus.value = 'error'
    trackContactForm('network_error')

    setTimeout(() => {
      formStatus.value = ''
    }, 5000)
  }
}
</script>

<style scoped>
.contact {
  width: 100%;
  padding: 5rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
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
  margin-bottom: 4rem;
  max-width: 680px;
  margin-left: auto;
  margin-right: auto;
  font-weight: 400;
}

.contact-content {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 3rem;
  align-items: start;
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

/* Contact Form Section */
.contact-form-section {
  background: var(--bg-card);
  padding: 2.5rem;
  border-radius: 12px;
  border: 1px solid var(--border-color);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06),
              0 1px 3px rgba(0, 0, 0, 0.04);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.contact-form-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0.8;
}

.contact-form-section h2 {
  font-size: clamp(1.5rem, 2vw, 1.875rem);
  margin-bottom: 1.75rem;
  color: var(--text-primary);
  text-align: left;
  font-weight: 700;
  letter-spacing: -0.02em;
}

/* Status Messages */
.status-message {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem 1.5rem;
  border-radius: 10px;
  margin-bottom: 1.75rem;
  animation: slideDown 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.status-message.success {
  background: linear-gradient(135deg, rgba(200, 108, 74, 0.12) 0%, rgba(212, 165, 116, 0.12) 100%);
  border: 1.5px solid var(--accent-primary);
  color: var(--accent-primary);
  border-left: 5px solid var(--accent-primary);
}

.status-message.error {
  background: rgba(220, 38, 38, 0.08);
  border: 1.5px solid rgba(220, 38, 38, 0.5);
  color: #dc2626;
  border-left: 5px solid #dc2626;
}

.status-message svg {
  flex-shrink: 0;
  opacity: 0.9;
}

.status-message p {
  margin: 0;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.6;
  font-weight: 500;
}

/* Form Styles */
.contact-form {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  position: relative;
}

.form-group label {
  font-weight: 600;
  color: var(--text-primary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  letter-spacing: -0.01em;
}

.form-group input,
.form-group textarea {
  padding: 1rem 1.25rem;
  border: 1.5px solid var(--border-color);
  border-radius: 10px;
  background: var(--bg-primary);
  color: var(--text-primary);
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-family: 'Source Sans 3', -apple-system, BlinkMacSystemFont, sans-serif;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: var(--text-tertiary);
  opacity: 0.7;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 4px rgba(200, 108, 74, 0.12),
              0 2px 8px rgba(0, 0, 0, 0.08);
  transform: translateY(-1px);
}

.form-group input:disabled,
.form-group textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-group textarea {
  resize: vertical;
  min-height: 150px;
  line-height: 1.65;
}

.char-count {
  font-size: clamp(0.8125rem, 1vw, 0.875rem);
  color: var(--text-tertiary);
  text-align: right;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.submit-btn {
  padding: 1.125rem 2.5rem;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-secondary) 100%);
  color: var(--bg-primary);
  border: none;
  border-radius: 10px;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  align-self: flex-start;
  letter-spacing: -0.01em;
  box-shadow: 0 3px 12px rgba(200, 108, 74, 0.25),
              0 1px 3px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

.submit-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.6s ease;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(200, 108, 74, 0.35),
              0 4px 8px rgba(0, 0, 0, 0.12);
  background: linear-gradient(135deg, var(--accent-hover) 0%, var(--accent-primary) 100%);
}

.submit-btn:hover:not(:disabled)::before {
  left: 100%;
}

.submit-btn:active:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(200, 108, 74, 0.3);
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

/* Contact Info */
.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.contact-info h2 {
  font-size: clamp(1.375rem, 1.8vw, 1.625rem);
  margin-bottom: 0.75rem;
  color: var(--text-primary);
  text-align: left;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
  padding: 1.5rem 1.75rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 10px;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
}

.info-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
  background: linear-gradient(180deg, var(--accent-primary), var(--accent-secondary));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.info-card:hover {
  transform: translateX(8px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1),
              0 3px 8px rgba(0, 0, 0, 0.06);
  border-color: var(--accent-primary)40;
}

.info-card:hover::before {
  opacity: 1;
}

.info-card svg {
  flex-shrink: 0;
  color: var(--accent-primary);
  margin-top: 0.25rem;
}

.info-card h3 {
  font-size: clamp(1.0625rem, 1.3vw, 1.1875rem);
  margin: 0 0 0.5rem 0;
  color: var(--text-primary);
  font-weight: 600;
  letter-spacing: -0.015em;
}

.info-card a {
  color: var(--link-color);
  text-decoration: none;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  word-break: break-word;
  font-weight: 500;
  letter-spacing: -0.01em;
  display: inline-block;
}

.info-card a:hover {
  color: var(--accent-hover);
  text-decoration: none;
  transform: translateX(3px);
}

.response-time {
  padding: 1.5rem 1.75rem;
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-card) 100%);
  border-left: 5px solid var(--accent-primary);
  border-radius: 10px;
  margin-top: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  border: 1px solid var(--border-color);
  border-left-width: 5px;
}

.response-time p {
  margin: 0;
  font-size: clamp(0.9375rem, 1.1vw, 1rem);
  line-height: 1.7;
  color: var(--text-secondary);
  font-weight: 400;
}

.response-time strong {
  color: var(--text-primary);
  font-weight: 600;
}

/* Responsive */
@media (max-width: 968px) {
  .contact {
    padding: 3.5rem 1.5rem;
  }

  .contact-content {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .contact-info {
    order: -1;
  }
}

@media (max-width: 768px) {
  .contact {
    padding: 3rem 1.25rem;
  }

  .page-intro {
    margin-bottom: 3rem;
  }

  .contact-form-section {
    padding: 2rem;
  }

  .submit-btn {
    width: 100%;
  }

  .info-card {
    padding: 1.25rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .contact {
    padding: 2.5rem 1rem;
  }

  .contact-form-section {
    padding: 1.5rem;
  }

  .form-group input,
  .form-group textarea {
    padding: 0.875rem 1rem;
  }

  .submit-btn {
    padding: 1rem 2rem;
  }
}
</style>
