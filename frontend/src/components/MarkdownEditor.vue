<template>
  <div class="markdown-editor">
    <!-- Toolbar -->
    <div class="editor-toolbar">
      <button
        v-for="action in toolbarActions"
        :key="action.name"
        @click="applyFormat(action)"
        class="toolbar-btn"
        :title="action.title"
        type="button"
      >
        {{ action.icon }}
      </button>

      <div class="toolbar-divider"></div>

      <!-- View toggle -->
      <button
        v-for="view in views"
        :key="view.name"
        @click="currentView = view.name"
        class="toolbar-btn"
        :class="{ active: currentView === view.name }"
        :title="view.title"
        type="button"
      >
        {{ view.icon }}
      </button>
    </div>

    <!-- Editor content -->
    <div class="editor-content">
      <!-- Write view -->
      <div
        v-show="currentView === 'write' || currentView === 'split'"
        class="editor-pane"
      >
        <textarea
          id="markdown-editor"
          ref="textarea"
          v-model="content"
          @input="handleInput"
          class="editor-textarea"
          :placeholder="placeholder"
          spellcheck="true"
          aria-label="Markdown content editor"
        ></textarea>
      </div>

      <!-- Preview view -->
      <div
        v-show="currentView === 'preview' || currentView === 'split'"
        class="preview-pane"
      >
        <div
          class="markdown-body preview-content"
          v-html="renderedMarkdown"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: 'Write your content in markdown...'
  }
})

const emit = defineEmits(['update:modelValue'])

const content = ref(props.modelValue)
const currentView = ref('split')
const textarea = ref(null)

// Initialize markdown-it (matches BlogPost.vue configuration)
const md = new MarkdownIt({
  html: false,        // Disable HTML for security
  linkify: true,      // Auto-convert URLs
  typographer: true   // Smart quotes
})

// Open links in new tab
md.renderer.rules.link_open = (tokens, idx, options, env, self) => {
  tokens[idx].attrSet('target', '_blank')
  tokens[idx].attrSet('rel', 'noopener noreferrer')
  return self.renderToken(tokens, idx, options)
}

// Custom renderer: Convert video files from <img> to <video>
const defaultImageRenderer = md.renderer.rules.image
md.renderer.rules.image = (tokens, idx, options, env, self) => {
  const token = tokens[idx]
  const src = token.attrGet('src')
  const alt = token.content

  // Check if source is a video file
  if (src && /\.(mp4|webm|ogg|mov)$/i.test(src)) {
    return `<video controls style="max-width: 100%; border-radius: 8px;">
      <source src="${src}" type="video/${src.split('.').pop().toLowerCase()}">
      ${alt}
    </video>`
  }

  // Default image rendering
  return defaultImageRenderer(tokens, idx, options, env, self)
}

// Watch for external changes
watch(() => props.modelValue, (newValue) => {
  if (newValue !== content.value) {
    content.value = newValue
  }
})

// Rendered markdown
const renderedMarkdown = computed(() => {
  if (!content.value) {
    return '<p class="preview-placeholder">Preview will appear here...</p>'
  }
  return md.render(content.value)
})

// Toolbar actions
const toolbarActions = [
  {
    name: 'bold',
    icon: 'B',
    title: 'Bold (Ctrl+B)',
    before: '**',
    after: '**',
    placeholder: 'bold text'
  },
  {
    name: 'italic',
    icon: 'I',
    title: 'Italic (Ctrl+I)',
    before: '_',
    after: '_',
    placeholder: 'italic text'
  },
  {
    name: 'heading',
    icon: 'H',
    title: 'Heading',
    before: '## ',
    after: '',
    placeholder: 'Heading'
  },
  {
    name: 'list',
    icon: '•',
    title: 'Bullet List',
    before: '- ',
    after: '',
    placeholder: 'List item'
  },
  {
    name: 'link',
    icon: '🔗',
    title: 'Link',
    before: '[',
    after: '](url)',
    placeholder: 'link text'
  },
  {
    name: 'code',
    icon: '</>',
    title: 'Code',
    before: '`',
    after: '`',
    placeholder: 'code'
  },
  {
    name: 'quote',
    icon: '"',
    title: 'Quote',
    before: '> ',
    after: '',
    placeholder: 'Quote'
  }
]

// View options
const views = [
  { name: 'write', icon: '✏️', title: 'Write' },
  { name: 'split', icon: '⬌', title: 'Split View' },
  { name: 'preview', icon: '👁️', title: 'Preview' }
]

// Handle input
const handleInput = () => {
  emit('update:modelValue', content.value)
}

// Apply formatting
const applyFormat = (action) => {
  const el = textarea.value
  if (!el) return

  const start = el.selectionStart
  const end = el.selectionEnd
  const selectedText = content.value.substring(start, end)
  const textBefore = content.value.substring(0, start)
  const textAfter = content.value.substring(end)

  // Insert format
  const textToInsert = selectedText || action.placeholder
  const newText = textBefore + action.before + textToInsert + action.after + textAfter

  content.value = newText
  emit('update:modelValue', content.value)

  // Restore focus and selection
  el.focus()
  const newCursorPos = start + action.before.length + textToInsert.length
  el.setSelectionRange(newCursorPos, newCursorPos)
}
</script>

<style scoped>
.markdown-editor {
  display: flex;
  flex-direction: column;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  overflow: hidden;
  background: var(--bg-card);
  height: 500px;
}

/* Toolbar */
.editor-toolbar {
  display: flex;
  gap: 0.25rem;
  padding: 0.75rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-tertiary);
  flex-wrap: wrap;
}

.toolbar-btn {
  padding: 0.5rem 0.75rem;
  background: transparent;
  border: 1px solid transparent;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-secondary);
  transition: all 0.2s ease;
  min-width: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toolbar-btn:hover {
  background: var(--bg-hover);
  color: var(--text-primary);
  border-color: var(--border-color);
}

.toolbar-btn.active {
  background: var(--accent-primary);
  color: white;
  border-color: var(--accent-primary);
}

.toolbar-divider {
  width: 1px;
  background: var(--border-color);
  margin: 0 0.5rem;
}

/* Editor content */
.editor-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.editor-pane,
.preview-pane {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.editor-pane {
  border-right: 1px solid var(--border-color);
  background: var(--bg-primary);
}

.editor-textarea {
  width: 100%;
  height: 100%;
  border: none;
  background: transparent;
  color: var(--text-primary);
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  font-size: 0.9375rem;
  line-height: 1.6;
  resize: none;
  outline: none;
}

.editor-textarea::placeholder {
  color: var(--text-tertiary);
}

/* Preview */
.preview-pane {
  background: var(--bg-card);
}

.preview-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: var(--text-secondary);
}

.preview-placeholder {
  color: var(--text-tertiary);
  font-style: italic;
}

/* Markdown body styles */
.markdown-body p {
  margin: 1em 0;
}

.markdown-body p:first-child {
  margin-top: 0;
}

.markdown-body p:last-child {
  margin-bottom: 0;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  margin: 1.5em 0 0.5em;
  font-weight: 600;
  line-height: 1.3;
}

.markdown-body h1 {
  font-size: 2em;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.3em;
}

.markdown-body h2 {
  font-size: 1.5em;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.3em;
}

.markdown-body h3 {
  font-size: 1.25em;
}

.markdown-body h4 {
  font-size: 1.1em;
}

.markdown-body ul,
.markdown-body ol {
  margin: 1em 0;
  padding-left: 2em;
}

.markdown-body li {
  margin: 0.5em 0;
}

.markdown-body code {
  background: var(--bg-tertiary);
  color: var(--accent-primary);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.95em;
  font-family: 'Courier New', monospace;
}

.markdown-body pre {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 8px;
  padding: 1.5rem;
  overflow-x: auto;
  margin-bottom: 1.5rem;
}

.markdown-body pre code {
  background: none;
  color: var(--text-primary);
  padding: 0;
}

.markdown-body a {
  color: var(--link-color);
  text-decoration: none;
  font-weight: 500;
}

.markdown-body a:hover {
  color: var(--link-hover);
  text-decoration: underline;
}

.markdown-body blockquote {
  border-left: 4px solid var(--accent-primary);
  padding-left: 1.5rem;
  margin: 1.5rem 0;
  color: var(--text-secondary);
  font-style: italic;
}

.markdown-body strong {
  font-weight: 600;
}

.markdown-body em {
  font-style: italic;
}

/* Scrollbars */
.editor-pane::-webkit-scrollbar,
.preview-pane::-webkit-scrollbar {
  width: 8px;
}

.editor-pane::-webkit-scrollbar-track,
.preview-pane::-webkit-scrollbar-track {
  background: transparent;
}

.editor-pane::-webkit-scrollbar-thumb,
.preview-pane::-webkit-scrollbar-thumb {
  background: var(--border-color);
  border-radius: 10px;
}

.editor-pane::-webkit-scrollbar-thumb:hover,
.preview-pane::-webkit-scrollbar-thumb:hover {
  background: var(--text-tertiary);
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .markdown-editor {
    height: 400px;
  }

  .editor-content {
    flex-direction: column;
  }

  .editor-pane {
    border-right: none;
    border-bottom: 1px solid var(--border-color);
    min-height: 200px;
  }

  .editor-toolbar {
    padding: 0.5rem;
    gap: 0.125rem;
  }

  .toolbar-btn {
    padding: 0.375rem 0.5rem;
    min-width: 32px;
    font-size: 0.8125rem;
  }
}
</style>
