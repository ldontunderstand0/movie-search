import { createRouter, createWebHistory } from 'vue-router'
import MovieList from '@/components/movie/MovieList.vue'
import MovieDetail from '@/components/movie/MovieDetail.vue'
import Edit from '@/components/movie/Edit.vue'

import PersonList from '@/components/PersonList.vue'
import PersonDetail from '@/components/PersonDetail.vue'
import ReviewList from '@/components/ReviewList.vue'
import UserList from '@/components/UserList.vue'

import RatingList from '@/components/rating/RatingList.vue'
import RatingCreate from '@/components/rating/RatingCreate.vue'

import GenreList from '@/components/GenreList.vue'
import CountryList from '@/components/CountryList.vue'
import ProfessionList from '@/components/ProfessionList.vue'
import Index from '@/components/Index.vue'

import Login from '@/components/auth/Login.vue'
import Logout from '@/components/auth/Logout.vue'

const routes = [
  { path: '/', name: 'index', component: Index },
  { path: '/admin', name: 'admin', component: Login },

  { path: '/login', name: 'login', component: Login },
  { path: '/logout', name: 'logout', component: Logout },

  { path: '/user', name: 'user', component: UserList },
  { path: '/user/:id', name: 'user-detail', component: MovieDetail },

  { path: '/movie', name: 'movie', component: MovieList },
  { path: '/movie', name: 'movie-create', component: Edit },
  { path: '/movie/:id', name: 'movie-detail', component: MovieDetail },
  { path: '/movie/:id', name: 'movie-update', component: Edit },

  { path: '/review', name: 'review', component: ReviewList },

  { path: '/rating', name: 'rating', component: RatingList },
  { path: '/rating', name: 'rating-create', component: RatingCreate },

  { path: '/person', name: 'person', component: PersonList },
  { path: '/person/:id', name: 'person-detail', component: PersonDetail },

  { path: '/profession', name: 'profession', component: ProfessionList },

  { path: '/genre', name: 'genre', component: GenreList },

  { path: '/country', name: 'country', component: CountryList },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router