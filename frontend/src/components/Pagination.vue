<script setup>
defineProps({
  store: {
    type: Object,
    required: true
  }
})
</script>

<template>
<div v-if="store.count" class="pagination-container">
    <nav class="pagination-nav">
        <ul class="pagination-list">
                <li class="pagination-item">
                    <router-link :class="['pagination-link', 'pagination-first', { disabled: !store.previous }]"
                        :to="{ name: store.name, query: store.updatePage(store.currentParams, 1) }">
                        Первая
                    </router-link>
                </li>
                <li class="pagination-item">
                    <router-link :class="['pagination-link', 'pagination-prev', { disabled: !store.previous }]"
                        :to="{ name: store.name, query: store.getParams(store.previous) }">
                        Назад
                    </router-link>
                </li>

                <li v-for="page in store.visiblePages" class="pagination-item">
                    <router-link :class="['pagination-link', 'pagination-prev', { disabled: store.currentPage === page }]"
                        :to="{ name: store.name, query: store.updatePage(store.currentParams, page) }">
                        {{ page }}
                    </router-link>
                </li>


                <li class="pagination-item">
                    <router-link :class="['pagination-link', 'pagination-next', { disabled: !store.next }]"
                        :to="{ name: store.name, query: store.getParams(store.next) }">
                        Вперед
                    </router-link>
                </li>
                <li class="pagination-item">
                    <router-link :class="['pagination-link', 'pagination-last', { disabled: !store.next }]"
                        :to="{ name: store.name, query: store.updatePage(store.currentParams, store.totalPages) }">
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
</template>

<style scoped>
.disabled {
  color: gray;
  pointer-events: none;
  cursor: not-allowed;
}
/* Контейнер пагинации */
.pagination-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
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