import { createRouter, createWebHistory } from 'vue-router'
import MovieList from '@/components/MovieList.vue'
import PersonList from '@/components/PersonList.vue'
import ReviewList from '@/components/ReviewList.vue'
import UserList from '@/components/UserList.vue'
import RatingList from '@/components/RatingList.vue'
import GenreList from '@/components/GenreList.vue'
import CountryList from '@/components/CountryList.vue'
import ProfessionList from '@/components/ProfessionList.vue'

const routes = [
  { path: '/user/', name: 'user', component: UserList },
  { path: '/movie/', name: 'movie', component: MovieList },
  { path: '/review/', name: 'review', component: ReviewList },
  { path: '/rating/', name: 'rating', component: RatingList },
  { path: '/person/', name: 'person', component: PersonList },
  { path: '/profession/', name: 'profession', component: ProfessionList },
  { path: '/genre/', name: 'genre', component: GenreList },
  { path: '/country/', name: 'country', component: CountryList },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router