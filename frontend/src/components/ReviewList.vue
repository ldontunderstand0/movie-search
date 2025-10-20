<script setup>
import { watch } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, RadioFilter, SelectFilter, OrderingFilter, ClearFilter } from '@/components/filters'

const route = useRoute()
const store = useResourceStore()

store.setResource('review', api.review.list, api.review.filter)

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

            <OrderingFilter :currentFilter="store.currentParams.sort ?? ''" :items="store.filter.sort" />

        </div>
    </form>

    <h1 class="page-title">Рецензии</h1>
    <div v-if="store.loading">Загрузка...</div>
    <div v-else-if="store.error" class="error">{{ store.error }}</div>

    <div v-else class="pagination-info">
        Показано <span class="current-count">{{ store.shownItems }}</span> из
        <span class="total-count">{{ store.count }}</span> рецензий
    </div>
 
    <div class="reviews-container">
    <div class="reviews-list">
        <div v-for="review in store.items" class="review-item review-type">
            <div class="review-header">
                <div class="user-avatar">
                    <span class="avatar-icon">👤</span>
                </div>
                <div class="user-info">
                    <div class="user-name">{{ review.user }}</div>
                    <div class="review-date">{{ review.created_at }}</div>
                    <div class="review-date">{{ review.updated_at }}</div>
                </div>
            </div>

            <div class="review-content">
                <h3 class="review-title">{{ review.title }}</h3>
                <div class="review-text">
                    {{ review.text }}
                </div>
            </div>
        </div>
    </div>
</div>

    <Pagination :store="store" />
    
  </div>
</template>


<style scoped>
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
    margin: 0 0 30px 0;
    padding-bottom: 15px;
    border-bottom: 1px solid #e5e5e5;
}
.review-item {
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 20px;
    transition: all 0.3s ease;
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
}

.review-date {
    font-size: 12px;
    color: #666;
}
.review-content {
    margin-left: 52px;
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
</style>