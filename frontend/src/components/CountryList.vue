<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, ClearFilter } from '@/components/filters'
import Grid from '@/components/Grid.vue'

const route = useRoute()
const store = useResourceStore()

store.setResource('counrty', api.country.list, api.country.filter)

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

            <SearchFilter :search="store.currentParams.search ?? ''" placeholder="Название страны..." />
            <ClearFilter />

        </div>
    </form>

    <h1 class="page-title">Страны</h1>
    <div v-if="store.loading">Загрузка...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

    <div v-else class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> стран
    </div>

    <Grid :items="store.items" routeName="movie" queryKey="country" queryValueField="name" />

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
    color: #5f3300;
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