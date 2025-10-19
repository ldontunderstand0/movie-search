import { createRouter, createWebHistory } from 'vue-router'
import MovieList from '@/components/MovieList.vue'

const routes = [
  { path: '/movie/', name: 'movie', component: MovieList }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router