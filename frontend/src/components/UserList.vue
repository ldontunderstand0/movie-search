<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, RadioFilter, SelectFilter, OrderingFilter, ClearFilter } from '@/components/filters'

const route = useRoute()
const store = useResourceStore()

store.setResource('user', api.user.list, api.user.filter)

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
  <div class="movie-list-container">

    <form method="get" class="movie-filter-form">
        <div class="filter-row">
            <SearchFilter :search="store.currentParams.search ?? ''" placeholder="Логин пользователя..." />
            <OrderingFilter :currentFilter="store.currentParams.sort ?? ''" :items="store.filter.sort" />
            <ClearFilter />
        </div>
    </form>

    <h1 class="page-title">Пользователи</h1>
    <div v-if="store.loading">Загрузка...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

    <div v-else class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> пользователей
    </div>
 
    <ol class="movie-list">
        <li v-for="(user, index) in store.items" :key="user.id" class="movie-item">
        <div class="movie-number">
            {{ (store.currentPage - 1) * 10 + index + 1 }}
        </div>
        <div class="movie-info">
            <a class="movie-title-link" :href="user.id">
                <table>
                    <tr>
                        <th><span class="movie-title">{{ user.username }}</span></th>
                        <th><span class="movie-year">Просмотрено фильмов: {{ user.watches }}</span></th>
                        <th><span class="movie-year">Оценено фильмов: {{ user.rates }}</span></th>
                        <th><span class="movie-year">Рецензий написано: {{ user.reviews }}</span></th>
                    </tr>
                </table>
            </a>
        </div>
        </li>
    </ol>

    <Pagination :store="store" />
    
  </div>
</template>


<style scoped>
table {
  width: 100%;
  /* другие стили для таблицы */
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
    color: #999;
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
    padding-left: 5%;
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
    color: #666;
}

.movie-rate {
    font-size: 14px;
    color: #ff8a00;
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
@media (max-width: 992px) {
  .movie-list-container {
    margin: 0 6%;
    padding: 15px;
  }

  .filter-row {
    flex-wrap: wrap;
    gap: 10px;
  }

  .movie-title {
    font-size: 17px;
  }

  .movie-year {
    font-size: 13px;
  }

  .page-title {
    font-size: 24px;
  }

  .movie-item {

    padding: 15px 10px 15px 45px;
  }

  .movie-number {
    font-size: 20px;
    left: 10px;
    top: 15px;
  }

  .movie-title-link {
    padding-left: 0;
  }

  table th {

    text-align: left;
    padding: 4px 0;
  }
}

/* --- Телефоны (до 768px) --- */
@media (max-width: 768px) {
  .movie-list-container {
    margin: 0 4%;
    padding: 12px;
  }

  .movie-filter-form {
    padding: 15px;
  }

  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .page-title {
    font-size: 22px;
    text-align: center;
  }

  .movie-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
    padding: 15px 10px 15px 40px;
  }

  .movie-number {
    font-size: 18px;
    top: 10px;
    left: 5px;
  }

  .movie-title {
    font-size: 16px;
  }

  .movie-year {
    font-size: 12px;
  }

  .pagination-info {
    font-size: 13px;
    padding: 10px 15px;
  }

  table {
    font-size: 13px;
  }

  table th {
    display: block;
    text-align: left;
    font-weight: normal;
    padding: 4px 0;
  }
}

/* --- Маленькие телефоны (до 480px) --- */
@media (max-width: 480px) {
  .movie-list-container {
    margin: 0 2%;
    padding: 10px;
  }

  .movie-filter-form {
    padding: 12px;
  }
  .filter-group {
    width: 90%;
  }

  .page-title {
    font-size: 20px;
  }

  .movie-item {
    padding: 12px 8px 12px 35px;
  }

  .movie-number {
    font-size: 16px;
    top: 8px;
    left: 3px;
  }

  .movie-title {
    font-size: 15px;
  }

  .movie-year {
    font-size: 11px;
  }

  .pagination-info {
    font-size: 12px;
  }

  table {
    font-size: 12px;
  }

  table th {
    display: block;
    padding: 3px 0;
  }
}
</style>