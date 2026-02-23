/**
 * Centralized contact information configuration
 * Can be overridden via environment variables
 */

export const CONTACT = {
  email: import.meta.env.VITE_CONTACT_EMAIL || 'richwell.perez@gmail.com',
  linkedin: import.meta.env.VITE_CONTACT_LINKEDIN || 'https://www.linkedin.com/in/richwell-perez',
  github: import.meta.env.VITE_CONTACT_GITHUB || 'https://github.com/richwellp',

  // Formatted for error messages
  getContactMessage() {
    return `reach out to Richwell directly at ${this.email} or ${this.linkedin}`
  },

  // Short version
  getEmailOnly() {
    return this.email
  }
}
