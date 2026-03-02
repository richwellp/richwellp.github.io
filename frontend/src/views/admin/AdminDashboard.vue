<template>
  <div class="admin-dashboard">
    <AdminAuthModal
      :is-open="showAuthModal"
      @close="handleAuthCancel"
      @authenticated="handleAuthenticated"
    />

    <div v-if="isAuthenticated" class="dashboard-content">
      <div class="dashboard-header">
        <h1>Admin Dashboard</h1>
        <button @click="handleLogout" class="btn btn-secondary">Logout</button>
      </div>

      <div class="dashboard-cards">
        <!-- Blog Posts Card -->
        <router-link to="/admin/blogs" class="dashboard-card">
          <div class="card-icon">📝</div>
          <h2>Blog Posts</h2>
          <p class="card-stats" v-if="!loadingBlog">
            {{ blogStats.total }} total ({{ blogStats.published }} published, {{ blogStats.drafts }} drafts)
          </p>
          <p class="card-stats" v-else>Loading...</p>
          <span class="card-action">Manage Blog →</span>
        </router-link>

        <!-- Albums Card -->
        <router-link to="/admin/albums" class="dashboard-card">
          <div class="card-icon">📸</div>
          <h2>Albums</h2>
          <p class="card-stats" v-if="!loadingAlbums">
            {{ albumStats.albumCount }} albums, {{ albumStats.photoCount }} photos total
          </p>
          <p class="card-stats" v-else>Loading...</p>
          <span class="card-action">Manage Albums →</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AdminAuthModal from '../../components/AdminAuthModal.vue'
import { useAdminAuth } from '../../composables/useAdminAuth'
import { useAdminBlog } from '../../composables/useAdminBlog'
import { useAdminAlbums } from '../../composables/useAdminAlbums'

const router = useRouter()
const { isAuthenticated, logout } = useAdminAuth()
const { posts: blogPosts, loading: loadingBlog, fetchAdminPosts } = useAdminBlog()
const { albums, loading: loadingAlbums, fetchAdminAlbums } = useAdminAlbums()

const showAuthModal = ref(!isAuthenticated.value)

const blogStats = computed(() => {
  const published = blogPosts.value.filter(p => p.published).length
  const drafts = blogPosts.value.filter(p => !p.published).length
  return {
    total: blogPosts.value.length,
    published,
    drafts
  }
})

const albumStats = computed(() => {
  const photoCount = albums.value.reduce((sum, album) => sum + (album.photo_count || 0), 0)
  return {
    albumCount: albums.value.length,
    photoCount
  }
})

const handleAuthenticated = async () => {
  showAuthModal.value = false
  await loadData()
}

const handleAuthCancel = () => {
  router.push('/')
}

const handleLogout = () => {
  logout()
  router.push('/')
}

const loadData = async () => {
  try {
    await Promise.all([
      fetchAdminPosts(),
      fetchAdminAlbums()
    ])
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
}

onMounted(() => {
  if (isAuthenticated.value) {
    loadData()
  }
})
</script>

<style scoped>
.admin-dashboard {
  min-height: 100vh;
  background: var(--bg-primary);
  padding: 2rem;
}

.dashboard-content {
  max-width: 1200px;
  margin: 0 auto;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 3rem;
}

.dashboard-header h1 {
  font-size: 2rem;
  color: var(--text-primary);
}

.dashboard-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
}

.dashboard-card {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 2rem;
  text-decoration: none;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

@media (hover: hover) {
  .dashboard-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 20px var(--shadow);
    border-color: var(--accent-primary);
  }
}

.card-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.dashboard-card h2 {
  font-size: 1.5rem;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.card-stats {
  color: var(--text-secondary);
  font-size: 1rem;
  margin-bottom: 1.5rem;
  flex: 1;
}

.card-action {
  color: var(--accent-primary);
  font-weight: 600;
  font-size: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-secondary {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.btn-secondary:hover {
  background: var(--border-color);
}

@media (max-width: 768px) {
  .dashboard-cards {
    grid-template-columns: 1fr;
  }
}
</style>
