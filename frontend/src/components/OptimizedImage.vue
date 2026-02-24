<template>
  <picture>
    <source
      v-if="webpSrc"
      :srcset="webpSrc"
      type="image/webp"
    />
    <img
      :src="src"
      :alt="alt"
      :loading="loading"
      :class="imgClass"
      v-bind="$attrs"
    />
  </picture>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  loading: {
    type: String,
    default: 'lazy',
    validator: (value) => ['lazy', 'eager'].includes(value)
  },
  size: {
    type: String,
    default: 'full',
    validator: (value) => ['thumb', 'md', 'full'].includes(value)
  },
  imgClass: {
    type: String,
    default: ''
  }
})

// Convert original image path to WebP path with size
// Only for local images (not Supabase Storage URLs)
const webpSrc = computed(() => {
  if (!props.src) return null

  // Skip WebP optimization for Supabase Storage URLs
  if (props.src.includes('supabase.co/storage')) {
    return null
  }

  // Extract the extension and base path
  const lastDot = props.src.lastIndexOf('.')
  if (lastDot === -1) return null

  const basePath = props.src.substring(0, lastDot)

  // Add size suffix if not full size
  const suffix = props.size === 'full' ? '' : `_${props.size}`

  return `${basePath}${suffix}.webp`
})
</script>

<style scoped>
picture {
  display: contents;
}
</style>
