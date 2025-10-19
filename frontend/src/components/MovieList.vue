<script setup>
import { onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const store = useResourceStore()

store.setResource(api.listMovie, api.filterMovie)

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

            <div class="filter-group">
                <strong class="filter-label-text">Поиск:</strong>
                <input class="filter-input search-input" type="text"
                       name="search"
                       placeholder="Название фильма..."
                       :value="store.currentParams.search"
                       onchange="this.form.submit()">
            </div>

            <div class="filter-group">
                <strong class="filter-label-text">Тип:</strong>
                <label class="filter-radio-label">
                    <input class="filter-radio" type="radio" name="type" value=""
                           :checked="!store.currentParams.type"
                           onchange="this.form.submit()">
                    <span class="filter-radio-text">Все</span>
                </label>
                <label v-for="t in store.filter.types" class="filter-radio-label">
                    <input class="filter-radio" type="radio" name="type" :value="t"
                           :checked="store.currentParams.type === t"
                           onchange="this.form.submit()">
                    <span class="filter-radio-text">{{ t }}</span>
                </label>
            </div>

            <!-- Год выпуска -->
            <div class="filter-group">
                <strong class="filter-label-text">Год:</strong>
                <select :value="store.currentParams.year ?? ''" class="filter-select year-select" name="year" onchange="this.form.submit()">
                    <option key="" value="">Все года</option>
                    <option v-for="y in store.filter.years" :key="y" :value="y">{{ y }}</option>
                </select>
            </div>

            <div class="filter-group">
                <strong class="filter-label-text">Жанр:</strong>
                <select :value="store.currentParams.genre ?? ''" class="filter-select genre-select" name="genre" onchange="this.form.submit()">
                    <option key="" value="">Все жанры</option>
                    <option v-for="g in store.filter.genres" :key="g" :value="g">{{ g }}</option>
                </select>
            </div>

            <div class="filter-group">
                <strong class="filter-label-text">Страна:</strong>
                <select :value="store.currentParams.country ?? ''" class="filter-select genre-select" name="country" onchange="this.form.submit()">
                    <option key="" value="">Все страны</option>
                    <option v-for="c in store.filter.countries" :key="c" :value="c">{{ c }}</option>
                </select>
            </div>

            <div class="filter-group">
                <strong class="filter-label-text">Сортировка:</strong>
                <select :value="store.currentParams.sort ?? ''" class="filter-select sort-select" name="sort" onchange="this.form.submit()">
                    <option value="">По умолчанию</option>
                    <option value="-rate">
                        Рейтинг (высокий → низкий)
                    </option>
                    <option value="rate">
                        Рейтинг (низкий → высокий)
                    </option>
                    <option value="-release_date">
                        Новые сначала
                    </option>
                    <option value="release_date">
                        Старые сначала
                    </option>
                    <option value="title">
                        Название (А-Я)
                    </option>
                    <option value="-title">
                        Название (Я-А)
                    </option>
                </select>
            </div>

            <div class="filter-group">
                <a href="?" class="filter-button clear-button">Сбросить</a>
            </div>

        </div>
    </form>

    <h1 class="page-title">Фильмы</h1>
    <div v-if="store.loading">Загрузка...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

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
            <a :href="movie.id">
                <img class="poster-image" :src="movie.poster">
            </a>
        </div>
        <div v-else class="movie-list">
            <div class="no-poster">
                <span class="no-poster-text">Нет постера</span>
            </div>
        </div>
        <div class="movie-info">
            <a class="movie-title-link" :href="movie.id">
                <span class="movie-title">{{ movie.title }}</span>
            </a>
            <a class="movie-year-link" :href="movie.id">
                <span class="movie-year">{{ movie.release_year }}</span>
            </a>
            <a class="movie-rate-link" :href="movie.id">
                <span v-if="movie.rate" class="movie-rate">★ {{ movie.rate }}</span>
                <span v-else class="movie-rate">★ 0.0</span>
            </a>
        </div>
        </li>
    </ol>


    <div class="pagination-container">
        <nav class="pagination-nav">
            <ul class="pagination-list">
                    <li class="pagination-item">
                        <router-link :class="['pagination-link', 'pagination-first', { disabled: !store.previous }]"
                           :to="{ name: 'movie', query: store.updatePage(store.currentParams, 1) }">
                            Первая
                        </router-link>
                    </li>
                    <li class="pagination-item">
                        <router-link :class="['pagination-link', 'pagination-prev', { disabled: !store.previous }]"
                           :to="{ name: 'movie', query: store.getParams(store.previous) }">
                            Назад
                        </router-link>
                    </li>

                    <li v-for="page in store.visiblePages" class="pagination-item">
                        <router-link :class="['pagination-link', 'pagination-prev', { disabled: store.currentPage === page }]"
                           :to="{ name: 'movie', query: store.updatePage(store.currentParams, page) }">
                            {{ page }}
                        </router-link>
                    </li>


                    <li class="pagination-item">
                        <router-link :class="['pagination-link', 'pagination-next', { disabled: !store.next }]"
                           :to="{ name: 'movie', query: store.getParams(store.next) }">
                            Вперед
                        </router-link>
                    </li>
                    <li class="pagination-item">
                        <router-link :class="['pagination-link', 'pagination-last', { disabled: !store.next }]"
                           :to="{ name: 'movie', query: store.updatePage(store.currentParams, store.totalPages) }">
                            Последняя
                        </router-link>
                    </li>
            </ul>
        </nav>
        <div class="pagination-stats">
            Страница <span class="current-page">{{ store.currentPage }}</span>
            из <span class="total-pages">{{ store.totalPages }}</span>
        </div>
    </div>

    
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
    margin: 0 auto;
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

/* Поля ввода */
.filter-input {
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
}

.search-input {
    min-width: 200px;
}

.filter-input:focus {
    outline: none;
    border-color: #ff8a00;
    box-shadow: 0 0 0 2px rgba(255, 138, 0, 0.1);
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

/* Кнопки */
.filter-button {
    display: inline-block;
    padding: 8px 16px;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.clear-button {
    background: #ff8a00;
    color: white;
}

.clear-button:hover {
    background: #e67a00;
    transform: translateY(-1px);
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

/* Контейнер пагинации */
.pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 40px;
    padding: 20px 0;
    border-top: 1px solid #e5e5e5;
}

/* Навигация пагинации */
.pagination-nav {
    display: flex;
}

.pagination-list {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 5px;
}

.pagination-item {
    display: flex;
}

.pagination-link,
.pagination-current {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 8px 12px;
    border: 1px solid #ddd;
    border-radius: 4px;
    text-decoration: none;
    font-size: 14px;
    min-width: 40px;
    transition: all 0.3s ease;
}

.pagination-link {
    color: #666;
    background: white;
}

.pagination-link:hover {
    background: #ff8a00;
    color: white;
    border-color: #ff8a00;
    transform: translateY(-1px);
}

.pagination-current {
    background: #ff8a00;
    color: white;
    border-color: #ff8a00;
    font-weight: 600;
}

/* Специальные кнопки пагинации */
.pagination-first,
.pagination-last {
    font-weight: 500;
}

.pagination-prev,
.pagination-next {
    font-weight: 500;
}

/* Статистика пагинации */
.pagination-stats {
    font-size: 14px;
    color: #666;
}

.current-page {
    font-weight: 600;
    color: #000;
}

.total-pages {
    font-weight: 600;
    color: #ff8a00;
}
</style>