<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, RadioFilter, SelectFilter, OrderingFilter, ClearFilter } from '@/components/filters'
import { destroyButton, updateButton, createButton } from '@/components/buttons'

const auth = useAuthStore()
const route = useRoute()
const store = useResourceStore()

store.setResource('movie', api.movie.list, api.movie.filter)

watch(
  () => route.query,
  (newQuery) => {
    store.loadItems(newQuery)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  },
  { immediate: true }
)

</script>

<template>

<div class="movie-list-container" id="movie-list-container">

    <form method="get" class="movie-filter-form" role="form" aria-label="Фильтры">
        <div class="filter-row">

            <SearchFilter :search="store.currentParams.search ?? ''" placeholder="Название фильма..." />
            <RadioFilter label="Тип" name="type" emptyLabel="Все" :currentFilter="store.currentParams.type ?? ''" :items="store.filter.types" />
            <SelectFilter label="Год" name="year" emptyLabel="Все года" :currentFilter="store.currentParams.year ?? ''" :items="store.filter.years" />
            <SelectFilter label="Жанр" name="genre" emptyLabel="Все жанры" :currentFilter="store.currentParams.genre ?? ''" :items="store.filter.genres" />
            <SelectFilter label="Страна" name="country" emptyLabel="Все страны" :currentFilter="store.currentParams.country ?? ''" :items="store.filter.countries" />
            <OrderingFilter :currentFilter="store.currentParams.sort ?? ''" :items="store.filter.sort" />
            <ClearFilter />

        </div>
    </form>

    <h1 class="page-title">Фильмы
        <createButton v-if="auth.user && auth.user.is_staff" name="movie-create" />
    </h1>

    <div class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> фильмов
    </div>
 
    <ol class="movie-list">
        <li v-for="(movie, index) in store.items" :key="movie.id" class="movie-item">
        <div class="movie-number">
            {{ (store.currentPage - 1) * 10 + index + 1 }}
        </div>
        <div v-if="movie.poster" class="movie-poster">
            <router-link :to="{name: 'movie-detail',  params: {id: movie.id}}">
                <img class="poster-image" :src="movie.poster">
            </router-link>
        </div>
        <div v-else class="movie-list">
            <div class="no-poster">
                <span class="no-poster-text">Нет постера</span>
            </div>
        </div>
        <div class="movie-info">
            <router-link class="movie-title-link" :to="{name: 'movie-detail',  params: {id: movie.id}}">
                <span class="movie-title">{{ movie.title }}</span>
            </router-link>
            <router-link class="movie-year-link" :to="{name: 'movie-detail',  params: {id: movie.id}}">
                <span class="movie-year">{{ movie.release_year }}</span>
            </router-link>
            <router-link class="movie-rate-link" :to="{name: 'movie-detail',  params: {id: movie.id}}">
                <span v-if="movie.rate" class="movie-rate">★ {{ movie.rate }}</span>
                <span v-else class="movie-rate">★ 0.0</span>
            </router-link>
        </div>
        <updateButton v-if="auth.user && auth.user.is_staff" name="movie-update" :id="movie.id" />
        <destroyButton v-if="auth.user && auth.user.is_staff" :id="movie.id" :api="api.movie"/>
        </li>
    </ol>

    <Pagination :store="store" />
    
  </div>
</template>


<style scoped>
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
    margin: 0 0 30px 0;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5e5e5;
}
.movie-list {
    list-style: none;
    padding: 0;
    margin: 0;
    counter-reset: movie-counter;
}

.movie-item {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 20px;
    border-bottom: 1px solid #e5e5e5;
    counter-increment: movie-counter;
    position: relative;
    transition: background-color 0.2s;
}

.movie-item:hover {
    background-color: #f8f9fa;
}

.movie-item:last-child {
    border-bottom: none;
}
.movie-number {
    font-size: 24px;
    font-weight: 300;
    color: #000000;
    min-width: 40px;
    text-align: center;
    position: absolute;
    left: 10px;
    top: 25px;
}

.movie-item::before {
    display: none;
}

/* Постер */
.movie-poster {
    width: 100px;
    height: 150px;
    margin-left: 50px;
    flex-shrink: 0;
}

.poster-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    border-radius: 4px;
}

.no-poster {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    border-radius: 4px;
    font-size: 12px;
}

.no-poster-text {
    text-align: center;
}

/* Информация о фильме */
.movie-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.movie-title-link {
    text-decoration: none;
}

.movie-title {
    font-size: 18px;
    font-weight: 500;
    color: #000;
    transition: color 0.2s;
}

.movie-title:hover {
    color: #ff8a00;
}

.movie-year-link, .movie-rate-link {
    text-decoration: none;
}

.movie-year {
    font-size: 14px;
    color: #2f2f2f;
}

.movie-rate {
    font-size: 14px;
    color: #703c00;
    font-weight: 500;
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
    color: #824500;
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

@media (max-width: 1024px) {
  .movie-list-container {
    margin-left: 5%;
    margin-right: 5%;
    padding: 15px;
  }

  .filter-row {
    gap: 10px;
  }

  .movie-item {
    gap: 15px;
  }

  .movie-poster {
    width: 90px;
    height: 135px;
    margin-left: 40px;
  }

  .movie-title {
    font-size: 16px;
  }

  .movie-number {
    left: 5px;
    top: 20px;
    font-size: 20px;
  }
}

/* Экран до 768px (планшеты и большие телефоны) */
@media (max-width: 768px) {
  .movie-list-container {
    margin: 0;
    padding: 10px;
  }



  .movie-item {
    flex-direction: row;
    align-items: flex-start;
    gap: 12px;
    padding: 15px 10px;
  }

  .movie-number {
    position: static;
    font-size: 18px;
    min-width: 30px;
    text-align: left;
  }

  .movie-poster {
    width: 80px;
    height: 120px;
    margin-left: 0;
  }

  .movie-title {
    font-size: 16px;
  }

  .movie-year,
  .movie-rate {
    font-size: 13px;
  }
}

/* Экран до 480px (телефоны) */
@media (max-width: 480px) {
  .movie-list-container {
    padding: 8px;
  }

  .page-title {
    font-size: 22px;
    text-align: center;
  }

  .movie-item {
    padding: 15px;
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .movie-number {
    position: static;
    font-size: 18px;
    margin-bottom: 5px;
  }

  .movie-poster {
    width: 120px;
    height: 180px;
    margin: 0 auto 10px;
  }

  .movie-info {
    align-items: center;
  }

  .movie-title {
    font-size: 18px;
  }

  .movie-year,
  .movie-rate {
    font-size: 14px;
  }

  .pagination-info {
    font-size: 12px;
    padding: 10px;
    text-align: center;
  }

  .movie-filter-form {
    padding: 10px;
  }

}
</style>