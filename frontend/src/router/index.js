import { createRouter, createWebHashHistory } from 'vue-router'
import AboutMe from '../views/AboutMe.vue'
import Experience from '../views/Experience.vue'
import Projects from '../views/Projects.vue'
import CV from '../views/CV.vue'
import Misc from '../views/Misc.vue'

// Album views
import TravelAlbum from '../views/albums/TravelAlbum.vue'
import ProfessionalAlbum from '../views/albums/ProfessionalAlbum.vue'
import SportsAlbum from '../views/albums/SportsAlbum.vue'

// Blog views
import BlogList from '../views/blog/BlogList.vue'
import BlogPost from '../views/blog/BlogPost.vue'

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
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
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    return savedPosition || { top: 0 }
  }
})

export default router
