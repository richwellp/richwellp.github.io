import { createRouter, createWebHistory } from 'vue-router'
import AboutMe from '../views/AboutMe.vue'
import Experience from '../views/Experience.vue'
import Projects from '../views/Projects.vue'
import CV from '../views/CV.vue'
import Misc from '../views/Misc.vue'
import Albums from '../views/Albums.vue'
import Contact from '../views/Contact.vue'

// Album views
import TravelAlbum from '../views/albums/TravelAlbum.vue'
import ProfessionalAlbum from '../views/albums/ProfessionalAlbum.vue'
import SportsAlbum from '../views/albums/SportsAlbum.vue'

// Blog views
import BlogList from '../views/blog/BlogList.vue'
import BlogPost from '../views/blog/BlogPost.vue'

// Admin views
import AdminPanel from '../views/admin/AdminPanel.vue'
import PostEditor from '../views/admin/PostEditor.vue'

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
    // Album routes
    {
      path: '/misc/travel',
      name: 'travel-album',
      component: TravelAlbum
    },
    {
      path: '/misc/professional',
      name: 'professional-album',
      component: ProfessionalAlbum
    },
    {
      path: '/misc/sports',
      name: 'sports-album',
      component: SportsAlbum
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
      name: 'admin-panel',
      component: AdminPanel
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
