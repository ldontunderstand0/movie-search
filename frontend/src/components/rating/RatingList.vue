<script setup>
import { watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, RadioFilter, SelectFilter, OrderingFilter, ClearFilter } from '@/components/filters'
import MovieNav from '@/components/movie/MovieNav.vue'
import { destroyButton } from '@/components/buttons'

const route = useRoute()
const store = useResourceStore()

const userRateId = ref(null)
const userRate = ref(null)
const userIsWatched = ref(false)

store.setResource('rating', api.rating.list, api.rating.filter)

const userRating = async () => {
    if (!store.user || !store.currentParams.movie) return null
    const result = await api.rating.list({user: store.user.id, movie: Number(store.currentParams.movie)})
    const data = result.data
    if (!data.count) return null
    const rating = data.results[0]
    userRateId.value = rating.id 
    userRate.value = rating.rate
    userIsWatched.value = rating.is_watched
    console.log()
    return data.results[0]
}

const createRate = async (rate) => {
    await api.rating.create({rate: rate, user: store.user.id, movie: Number(store.currentParams.movie)})
    await userRating()
    window.location.reload()
}

const updateRate = async (rate) => {
    await api.rating.update(userRateId.value, {rate: rate, user: store.user.id, movie: Number(store.currentParams.movie)})
    await userRating()
    window.location.reload()
}

const createIsWatched = async (is_watched) => {
    await api.rating.create({is_watched: is_watched, user: store.user.id, movie: Number(store.currentParams.movie)})
    await userRating()
    window.location.reload()
}

const updateIsWatched = async (is_watched) => {
    await api.rating.update(userRateId.value, {is_watched: is_watched, user: store.user.id, movie: Number(store.currentParams.movie)})
    await userRating()
    window.location.reload()
}

watch(
  () => route.query,   // следим за query в URL
  async (newQuery) => {
    await store.loadItems(newQuery)
    await userRating()
    window.scrollTo({ top: 0, behavior: 'smooth' })
  },
  { immediate: true }  // вызываем сразу при монтировании
)

</script>

<template>
<div v-if="store.loading">Загрузка...</div>
<div v-else-if="store.error" class="error">{{ store.error }}</div>
<div v-else-if="store.items" class="movie-list-container">

    <MovieNav v-if="store.currentParams.movie" :movie_id="store.currentParams.movie" active="rating"/>

    <h1 v-if="store.currentParams.movie" class="page-title">Оцените фильм или измените оценку</h1>
    <div class="buttons" v-if="store.user && store.currentParams.movie">
        
        <div class="rate-buttons">
            <button 
            :class="['buttons-circle', userRate === n ? n > 7 ? 'rate-green' : n >= 4 ? 'rate-yellow' : 'rate-red' : '']" 
            v-for="n in 10" :key="n" 
            @click="userRate ? updateRate(n): createRate(n)">
                {{ n }}
        </button>
        </div>

        <div class="rate-buttons">
            <button 
            :class="['buttons-circle', userIsWatched ? 'rate-green' : '']" 
            @click="userIsWatched === null ? createIsWatched(true): updateIsWatched(true)">
                👁️
            </button>
            <button 
            :class="['buttons-circle', !userIsWatched ? 'rate-green' : '']" 
            @click="userIsWatched === null ? createIsWatched(false): updateIsWatched(false)">
                🙈
            </button>
        </div>
    </div>
    
    <h1 v-if="store.currentParams.movie" class="page-title">Оценки других пользователей</h1>
    <form method="get" class="movie-filter-form">
        <div class="filter-row">

            <RadioFilter label="Оценки" name="rate" emptyLabel="Все" :currentFilter="store.currentParams.rate ?? ''" :items="store.filter.rates"/>
            <OrderingFilter :currentFilter="store.currentParams.sort ?? ''" :items="store.filter.sort" />

        </div>
    </form>

    <h1 v-if="!store.currentParams.movie" class="page-title">Оценки</h1>
    
    <div v-if="store.count" class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> оценок
    </div>

    <!-- <router-link v-if="store.user && store.user.is_staff" :to="{name: 'rating-create', query: {movie: store.currentParams.movie ?? ''}}">Создать</router-link>
  -->
    <div class="reviews-container">
    <div class="reviews-list">
        <div v-for="rating in store.items" class="review-item review-type">
            <div class="review-header">
                <div class="user-avatar">
                    <span class="avatar-icon">👤</span>
                </div>
                <div class="user-info">
                    <router-link class="user-name" :to="{name: 'user-detail', params: {id: rating.user.id}}">{{ rating.user.username }}</router-link>
                    <div class="review-date">{{ new Date(rating.updated_at).toLocaleString('ru-RU', {year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit'}) }}</div>
                </div>
            </div>

            <div class="review-content">
                <h3 :class="['rate-circle', rating.rate > 7 ? 'rate-green' : rating.rate >= 4 ? 'rate-yellow' : 'rate-red']">{{ rating.rate }}</h3>
                <h3 v-if="!store.currentParams.movie" class="review-title">{{ rating.movie.title }}</h3>
                <span v-if="rating.is_watched" class="eye-icon rate-circle">👁️</span>
                <span v-else class="eye-icon rate-circle">🙈</span>
            </div>
            <destroyButton v-if="store.user && store.user.is_staff" :id="rating.id" :api="api.rating"/>
        </div>
    </div>
</div>

    <Pagination :store="store" />
    
  </div>
</template>


<style scoped>
.buttons {
    width: 100%;
    display: flex;
    justify-content: space-between;
    margin-bottom: 3%;
}
.rate-buttons {
    display: flex;
}
.buttons-circle {
  color: #000;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin: 10px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
  border-color: #e4e2e2;
}
.rate-circle {
  color: #000;
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin: 10px 20px;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.rate-green {
  background-color: #2ddb56; /* зелёный */
  border-color: #2ddb56;
}

.rate-yellow {
  background-color: #ffc107; /* жёлтый */
  border-color: #ffc107;
}

.rate-red {
  background-color: #dc3545; /* красный */
  border-color: #dc3545;
}
.reviews-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 30px 20px;
    background: white;
}
.movie-list-container {
    max-width: 1200px;
    margin-left: 12%;
    margin-right: 12%;
    padding: 20px;
    background: white;
    min-height: 100vh;
}
.movie-filter-form {
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    margin-bottom: 30px;
    border: 1px solid #e5e5e5;
}

.filter-row {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
}

.page-title {
    font-size: 28px;
    font-weight: 300;
    color: #000;
    margin: 0 0 20px 0;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5e5e5;
}
.review-item {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.3s ease;
    display: flex;
    justify-content: space-between;
}
.review-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 15px;
}
.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: #f0f0f0;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.avatar-icon {
    font-size: 16px;
    color: #666;
}
.user-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
}

.user-name {
    font-size: 14px;
    font-weight: 600;
    color: #000;
    text-decoration: none;
}

.review-date {
    font-size: 12px;
    color: #666;
}
.review-content {
    display: flex;
}

.review-title {
    font-size: 18px;
    font-weight: 600;
    color: #000;
    margin: 0 0 12px 0;
    line-height: 1.3;
}
.review-status {
    font-size: 18px;
    font-weight: 600;
    color: #000000;
    text-align: center;
}

.review-text {
    font-size: 14px;
    line-height: 1.5;
    color: #333;
    white-space: normal;
    word-break: break-word;
    text-align: justify;
    overflow-wrap: break-word;
}

.review-text p {
    margin: 0 0 10px 0;
}

.review-text p:last-child {
    margin-bottom: 0;
}

.review-type-positive {
    background: #f8fff8;
    border-left: 4px solid #2ed573;
}

.review-type-negative {
    background: #fff8f8;
    border-left: 4px solid #ff4757;
}

.review-type-neutral {
    background: #f8f8f8;
    border-left: 4px solid #747d8c;
}

.review-status-positive {
    color: #2ed573;
}

.review-status-negative {
    color: #ff4757;
}

.review-status-neutral {
    color: #000000;
}
.pagination-info {
    background: #f8f9fa;
    padding: 12px 20px;
    border-radius: 6px;
    margin-bottom: 20px;
    font-size: 14px;
    color: #666;
    border: 1px solid #e5e5e5;
}

.current-count {
    font-weight: 600;
    color: #000;
}

.total-count {
    font-weight: 600;
    color: #ff8a00;
}

/* Сообщение об отсутствии результатов */
.no-results {
    text-align: center;
    padding: 60px 20px;
    border-bottom: 1px solid #e5e5e5;
}

.no-results-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
}

.no-results-icon {
    font-size: 48px;
}

.no-results-text {
    font-size: 18px;
    color: #666;
}
@media (max-width: 1200px) {
      .movie-list-container {
    margin: 0 5%;
    padding: 15px;
  }
}
@media (max-width: 992px) {
  .movie-list-container {
    margin: 0 5%;
    padding: 15px;
  }

  .buttons {
    flex-direction: column;
    align-items: center;
    gap: 15px;
  }

  .rate-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }

  .buttons-circle {
    width: 45px;
    height: 45px;
    font-size: 18px;
    margin: 8px;
  }

  .rate-circle {
    width: 45px;
    height: 45px;
    font-size: 18px;
    margin: 8px 15px;
  }

  .page-title {
    font-size: 24px;
  }

  .review-item {
    align-items: flex-start;
    gap: 10px;
  }

  .review-content {
    flex-wrap: wrap;
    align-items: center;
    gap: 10px;
  }

  .pagination-info {
    font-size: 13px;
  }
}

/* --- Мобильные до 768px --- */
@media (max-width: 768px) {
  .movie-list-container {
    margin: 0 3%;
    padding: 12px;
  }

  .buttons {
    flex-direction: column;
    align-items: center;
  }

  .rate-buttons {
    justify-content: center;
    flex-wrap: wrap;
    gap: 6px;
  }

  .buttons-circle {
    width: 40px;
    height: 40px;
    font-size: 16px;
    margin: 6px;
  }

  .rate-circle {
    width: 40px;
    height: 40px;
    font-size: 16px;
    margin: 6px 10px;
  }

  .page-title {
    font-size: 22px;
    text-align: center;
  }

  .filter-row {
    flex-direction: column;
    gap: 10px;
    align-items: stretch;
  }

  :deep(.filter-group) {

    flex-direction: column;
    align-items: flex-start;
  }

  .review-item {
    padding: 15px;
  }

  .user-avatar {
    width: 35px;
    height: 35px;
  }

  .user-name {
    font-size: 13px;
  }

  .review-date {
    font-size: 11px;
  }

  .review-title {
    font-size: 16px;
  }

  .review-content {
    flex-direction: row;
    justify-content: flex-start;
  }

  .pagination-info {
    font-size: 12px;
    padding: 10px 15px;
  }
}

/* --- Маленькие телефоны до 480px --- */
@media (max-width: 480px) {
  .movie-list-container {
    margin: 0 1%;
    padding: 8px;
  }

  .buttons {
    flex-direction: column;
    align-items: center;
    gap: 8px;
  }

  .rate-buttons {
    flex-wrap: wrap;
    justify-content: center;
  }

  .buttons-circle {
    width: 35px;
    height: 35px;
    font-size: 14px;
    margin: 5px;
  }

  .rate-circle {
    width: 35px;
    height: 35px;
    font-size: 14px;
    margin: 5px 8px;
  }

  .page-title {
    font-size: 20px;
  }

  .review-item {
    padding: 10px;
  }

  .review-content {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 6px;
  }

  .review-title {
    font-size: 14px;
  }

  .review-date {
    font-size: 10px;
  }

  .pagination-info {
    font-size: 11px;
    padding: 8px 12px;
  }
}
</style>