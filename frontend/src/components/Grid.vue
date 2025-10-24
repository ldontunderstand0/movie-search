<script setup>
defineProps({
  items: {
    type: [Array, Object],
    default: () => [],
    required: true
  },
  routeName: { type: String, default: 'movie' }, // куда вести ссылку
    queryKey: { type: String, default: 'genre' }, // ключ query-параметра
    queryValueField: { type: String, default: 'name' } // поле из item для значения
})
</script>
<template>
<div class="grid">
    <div v-for="item in items" :key="item.id" class="card">
        <router-link :to="{ name: routeName, query: { [queryKey]: item[queryValueField] } }" class="link">
            <img v-if="item.random_poster" :src="item.random_poster" :alt="item.name" class="image" />
            <div v-else class="no-poster">Нет постера</div>
            <div class="overlay">
                <h3 class="name">{{ item.name }}</h3>
                <p class="count">Фильмов: {{ item.movies_count }}</p>
            </div>
        </router-link>
    </div>
</div>
</template>
<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
  padding: 16px;
}

.card {
  position: relative;
  cursor: pointer;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}

.card:hover {
  transform: scale(1.05);
}
.card a:focus {
  transform: scale(1.1);
}

.link {
  display: block;
  position: relative;
}

.image {
  width: 100%;
  height: 224px; /* h-56 */
  object-fit: cover;
}

.no-poster {
  width: 100%;
  height: 224px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e2e2e2;
  color: #555;
  font-weight: 600;
  font-size: 14px;
}

.overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  background: rgba(0, 0, 0, 0.75);
  padding: 8px 0px;
  color: white;
  display: flex;
  flex-direction: column;
}

.name {
  font-size: 16px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-transform: capitalize;
  text-align: center;
}

.count {
  font-size: 14px;
  text-align: center;
}
</style>