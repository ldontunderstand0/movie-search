<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, ClearFilter } from '@/components/filters'
import MovieNav from './movie/MovieNav.vue'
import router from '../router'

const route = useRoute()
const store = useResourceStore()

store.setResource('person', api.person.list, api.person.filter)

watch(
  () => route.query,   // следим за query в URL
  (newQuery) => {
    store.loadItems(newQuery)              // вызываем Pinia action
    window.scrollTo({ top: 0, behavior: 'smooth' })
  },
  { immediate: true }  // вызываем сразу при монтировании
)
</script>

<template>
  <div class="movie-list-container">

    <form method="get" class="movie-filter-form">
        <div class="filter-row">

            <SearchFilter :search="store.currentParams.search ?? ''" placeholder="Имя или фамилия..." />
            <ClearFilter />

        </div>
    </form>

    <h1 class="page-title">Личности</h1>
    <div v-if="store.loading">Загрузка...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

    <div class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> личностей
    </div>
 
    <ol class="movie-list">
        <li v-for="(person, index) in store.items" :key="person.id" class="movie-item">
        <div class="movie-number">
            {{ (store.currentPage - 1) * 10 + index + 1 }}
        </div>
        <div class="movie-list">
        </div>
        <div class="movie-info">
            <router-link class="movie-title-link" :to="{name: 'person-detail', params: {id: person.id}}">
                <span class="movie-title">{{ person.full_name }}</span>
            </router-link>
            <router-link class="movie-year-link" :to="{name: 'person-detail', params: {id: person.id}}">
                <span class="movie-year">{{ person.sex }}</span>
            </router-link>
            <router-link class="movie-year-link" :to="{name: 'person-detail', params: {id: person.id}}">
                <span class="movie-year">{{ person.birth_date }}</span>
            </router-link>
        </div>
        </li>
    </ol>

    <Pagination :store="store" />
  </div>
</template>


<style scoped>
.disabled {
  color: gray;
  pointer-events: none;
  cursor: not-allowed;
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

.filter-group {
    display: flex;
    align-items: center;
    gap: 10px;
    background: white;
    padding: 10px 15px;
    border-radius: 6px;
    border: 1px solid #ddd;
}

.filter-label-text {
    font-weight: 600;
    color: #333;
    white-space: nowrap;
}

/* Селекты */
.filter-select {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    background: white;
    min-width: 120px;
}

.filter-select:focus {
    outline: none;
    border-color: #ff8a00;
}

/* Радио кнопки */
.filter-radio-label {
    display: flex;
    align-items: center;
    gap: 5px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 4px;
    transition: background-color 0.2s;
}

.filter-radio-label:hover {
    background-color: #f0f0f0;
}

.filter-radio {
    margin: 0;
}

.filter-radio-text {
    font-size: 14px;
    color: #666;
}

.filter-radio:checked + .filter-radio-text {
    color: #ff8a00;
    font-weight: 500;
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
        padding-left: 5%;
    text-align: center;
}

/* Информация о фильме */
.movie-info {
    padding-left: 5%;
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
@media (max-width: 480px) {
  .movie-list-container {
    margin: 0 1%;
    padding: 3%;
  }

}  
</style>