<script setup>
defineProps({
  movie_id: {
    required: true
  },
    active: {
    required: true
  },
})
</script>
<template>
<nav class="tabs">
    <ul>
        <li :class="['tab-link', {active: active === 'movie'}]">
            <router-link :to="{name: 'movie-detail', params: {id: movie_id}}">Описание</router-link>
        </li>
        <li :class="['tab-link', {active: active === 'actors'}]">
            <router-link :to="{name: 'profession', query: {movie: movie_id, name: 'актер'}}">Актеры</router-link>
        </li>
        <li :class="['tab-link', {active: active === 'directors'}]">
            <router-link :to="{name: 'profession', query: {movie: movie_id, name: 'режиссер'}}">Режиссеры</router-link>
        </li>
        <li :class="['tab-link', {active: active === 'review'}]">
            <router-link :to="{name: 'review', query: {movie: movie_id}}">Рецензии</router-link>
        </li>
        <li :class="['tab-link', {active: active === 'rating'}]">
            <router-link :to="{name: 'rating', query: {movie: movie_id}}">Оценки</router-link>
        </li>
    </ul>
</nav>
</template>

<style scoped>
.tabs ul {
  display: flex;
  list-style: none;
  padding: 0;
  margin-bottom: 2%;
  margin-top: 0;
  gap: 12px; /* расстояние между табами */
  justify-content: center;
}

.tab-link a {
    text-decoration: none;
    color: #5e5e5e;
    font-size: large;
}

.tab-link {
  text-decoration: none;
  color: #333;
  padding: 12px;
  transition: background 0.2s;
}

.tab-link:hover {
  color: #000;
}

.active {
  border-bottom: 3px solid #000;
  color: #000;
}
@media (max-width: 920px) {
  .tab-link {
    padding: 8px;
    
  }
  .tab-link a{
    font-size: 14px;
  }
  .tabs ul {
gap: 0;
  }
  
}
@media (max-width: 480px) {
  .tab-link {
    padding: 8px;
    
  }
  .tab-link a{
    font-size: 14px;
  }
  .tabs ul {
gap: 0;
  }
  
}
</style>