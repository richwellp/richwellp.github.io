<template>
  <div class="album-page">
    <div class="container">
      <!-- Header -->
      <div class="album-header">
        <router-link to="/misc" class="back-link">← Back to Misc</router-link>
        <h1>{{ icon }} {{ title }}</h1>
        <p class="album-subtitle">{{ subtitle }}</p>
      </div>

      <!-- Coming Soon State -->
      <div v-if="comingSoon" class="coming-soon">
        <div class="icon">{{ icon }}</div>
        <h2>Coming Soon</h2>
        <p>{{ comingSoonMessage || 'Photos will be added here soon!' }}</p>
      </div>

      <!-- Content (when not coming soon) -->
      <template v-else>
        <!-- Tabs (if categories exist) -->
        <div v-if="hasCategories" class="tabs">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="activeTab = category.id"
            :class="['tab', { active: activeTab === category.id }]"
          >
            {{ category.name }}
          </button>
        </div>

        <!-- Photo Grid -->
        <div v-if="currentPhotos.length > 0" class="photos-grid">
          <div v-for="item in currentPhotos" :key="item.src" class="photo-item">
            <OptimizedImage
              v-if="!item.type || item.type === 'image'"
              :src="item.src"
              :alt="item.caption"
              size="md"
              loading="lazy"
              img-class="photo-image"
              @click="openLightbox(item)"
            />
            <video
              v-else-if="item.type === 'video'"
              :src="item.src"
              @click="openLightbox(item)"
              muted
              loop
              playsinline
            />
            <p class="photo-caption">{{ item.caption }}</p>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="currentPhotos.length === 0 && !comingSoon" class="empty-state">
          <p>📸 No photos yet for this section. Check back later!</p>
        </div>
      </template>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxPhoto" class="lightbox" @click="closeLightbox">
      <div class="lightbox-content" @click.stop>
        <button class="lightbox-close" @click="closeLightbox">×</button>
        <OptimizedImage
          v-if="!lightboxPhoto.type || lightboxPhoto.type === 'image'"
          :src="lightboxPhoto.src"
          :alt="lightboxPhoto.caption"
          size="full"
          loading="eager"
          img-class="lightbox-image"
        />
        <video
          v-else-if="lightboxPhoto.type === 'video'"
          :src="lightboxPhoto.src"
          controls
          autoplay
          loop
          playsinline
        />
        <p class="lightbox-caption">{{ lightboxPhoto.caption }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import OptimizedImage from './OptimizedImage.vue'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  icon: {
    type: String,
    default: '📷'
  },
  subtitle: {
    type: String,
    default: ''
  },
  photos: {
    type: [Array, Object],
    default: () => []
  },
  categories: {
    type: Array,
    default: () => []
  },
  defaultCategory: {
    type: String,
    default: null
  },
  comingSoon: {
    type: Boolean,
    default: false
  },
  comingSoonMessage: {
    type: String,
    default: ''
  }
})

const activeTab = ref(props.defaultCategory || (props.categories[0]?.id || null))
const lightboxPhoto = ref(null)

const hasCategories = computed(() => props.categories.length > 0)

const currentPhotos = computed(() => {
  if (hasCategories.value && typeof props.photos === 'object' && !Array.isArray(props.photos)) {
    return props.photos[activeTab.value] || []
  }
  return Array.isArray(props.photos) ? props.photos : []
})

const openLightbox = (photo) => {
  lightboxPhoto.value = photo
}

const closeLightbox = () => {
  lightboxPhoto.value = null
}
</script>

<style scoped>
.album-page {
  padding: 4rem 2rem;
  background: var(--bg-primary);
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
}

/* Header */
.album-header {
  margin-bottom: 2rem;
}

.back-link {
  display: inline-block;
  color: var(--link-color);
  text-decoration: none;
  font-weight: 600;
  margin-bottom: 1rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--link-hover);
}

h1 {
  font-size: 2.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.album-subtitle {
  font-size: 1.1rem;
  color: var(--text-secondary);
}

/* Coming Soon */
.coming-soon {
  text-align: center;
  padding: 6rem 2rem;
  background: var(--bg-card);
  border-radius: 12px;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
}

.coming-soon .icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
}

.coming-soon h2 {
  font-size: 2rem;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.coming-soon p {
  font-size: 1.1rem;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
}

/* Tabs */
.tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.tab {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  font-size: 1rem;
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  border-radius: 6px 6px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.tab:hover {
  color: var(--text-primary);
  background: var(--bg-hover);
}

.tab.active {
  color: var(--accent-primary);
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-bottom-color: var(--bg-card);
  position: relative;
  bottom: -2px;
}

/* Photos Grid */
.photos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
}

.photo-item {
  background: var(--bg-card);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 10px var(--shadow);
  border: 1px solid var(--border-color);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.photo-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px var(--shadow);
}

.photo-item img,
.photo-item video,
.photo-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
  display: block;
  cursor: pointer;
}

.photo-item video {
  background: #000;
}

.photo-caption {
  padding: 1rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
  text-align: center;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--text-secondary);
  font-size: 1.1rem;
}

/* Lightbox */
.lightbox {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 2rem;
}

.lightbox-content {
  position: relative;
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.lightbox-close {
  position: absolute;
  top: -40px;
  right: 0;
  background: transparent;
  border: none;
  color: white;
  font-size: 3rem;
  cursor: pointer;
  font-weight: 300;
  transition: transform 0.2s ease;
}

.lightbox-close:hover {
  transform: scale(1.2);
}

.lightbox-content img,
.lightbox-content video,
.lightbox-image {
  max-width: 100%;
  max-height: calc(90vh - 100px);
  object-fit: contain;
  border-radius: 8px;
}

.lightbox-content video {
  background: #000;
}

.lightbox-caption {
  color: white;
  font-size: 1.1rem;
  margin-top: 1rem;
  text-align: center;
}

/* Responsive */
@media (max-width: 768px) {
  .album-page {
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .tabs {
    gap: 0.25rem;
  }

  .tab {
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }

  .photos-grid {
    grid-template-columns: 1fr;
  }

  .coming-soon {
    padding: 4rem 1rem;
  }

  .coming-soon .icon {
    font-size: 4rem;
  }

  .lightbox-close {
    top: -50px;
    font-size: 2.5rem;
  }
}
</style>
