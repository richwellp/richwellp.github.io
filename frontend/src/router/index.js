import { createRouter, createWebHistory } from 'vue-router'
import AboutMe from '../views/AboutMe.vue'
import Experience from '../views/Experience.vue'
import Projects from '../views/Projects.vue'
import CV from '../views/CV.vue'
import Misc from '../views/Misc.vue'
import Albums from '../views/Albums.vue'
import Contact from '../views/Contact.vue'

// Album views
import AlbumDetail from '../views/albums/AlbumDetail.vue'

// Blog views
import BlogList from '../views/blog/BlogList.vue'
import BlogPost from '../views/blog/BlogPost.vue'

// Admin views
import AdminDashboard from '../views/admin/AdminDashboard.vue'
import AdminPanel from '../views/admin/AdminPanel.vue'
import PostEditor from '../views/admin/PostEditor.vue'
import AlbumsAdmin from '../views/admin/AlbumsAdmin.vue'
import PhotoManager from '../views/admin/PhotoManager.vue'

// Structured data utilities
import { useStructuredDataOnRouteChange } from '../composables/useStructuredData'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'about-me',
      component: AboutMe
    },
    {
      path: '/experience',
      name: 'experience',
      component: Experience
    },
    {
      path: '/projects',
      name: 'projects',
      component: Projects
    },
    {
      path: '/cv',
      name: 'cv',
      component: CV
    },
    {
      path: '/misc',
      name: 'misc',
      component: Misc
    },
    {
      path: '/contact',
      name: 'contact',
      component: Contact
    },
    // Albums landing page
    {
      path: '/misc/albums',
      name: 'albums',
      component: Albums
    },
    // Dynamic album route
    {
      path: '/misc/albums/:slug',
      name: 'album-detail',
      component: AlbumDetail
    },
    // Blog routes
    {
      path: '/misc/blog',
      name: 'blog-list',
      component: BlogList
    },
    {
      path: '/misc/blog/:slug',
      name: 'blog-post',
      component: BlogPost
    },
    // Admin routes
    {
      path: '/admin',
      name: 'admin-dashboard',
      component: AdminDashboard
    },
    {
      path: '/admin/blogs',
      name: 'admin-blogs',
      component: AdminPanel
    },
    {
      path: '/admin/albums',
      name: 'admin-albums',
      component: AlbumsAdmin
    },
    {
      path: '/admin/albums/:slug/photos',
      name: 'admin-album-photos',
      component: PhotoManager
    },
    {
      path: '/admin/new',
      name: 'admin-new-post',
      component: PostEditor
    },
    {
      path: '/admin/edit/:slug',
      name: 'admin-edit-post',
      component: PostEditor
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

// Inject structured data on route change
router.beforeEach((to, from, next) => {
  useStructuredDataOnRouteChange(to)
  next()
})

export default router
