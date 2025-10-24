<script setup>
import { watch, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useResourceStore } from '@/stores/resourceStore'
import api from '@/services/api'
import Pagination from '@/components/Pagination.vue'
import { SearchFilter, RadioFilter, SelectFilter, OrderingFilter, ClearFilter } from '@/components/filters'
import Grid from '@/components/Grid.vue'

const topMovies = ref([])
const topGenres = ref([])
const closeBirthdays = ref([])

const formatDate = (dateStr) => {
    const date = new Date(dateStr)
    return new Intl.DateTimeFormat('ru-RU', { day: 'numeric', month: 'long' }).format(date)
}

const todayBirthday = (dateStr) => {
    const date = new Date(dateStr)
    const today = new Date()

    if (date.getMonth() === today.getMonth() && date.getDate() === today.getDate()) return true
    return false
}

onMounted(async () => {
    const movieResponce = await api.movie.list({sort: '-rate'})
    topMovies.value = movieResponce.data.results.slice(0, 5)

    const genreResponce = await api.genre.list({sort: '-movies_count'})
    topGenres.value = genreResponce.data.results.slice(0, 4)

    const personResponce = await api.person.list({sort: 'birthday'})
    closeBirthdays.value = personResponce.data.results.slice(0, 5)
})

</script>
<template>
<div class="movie-list-container" id="movie-list-container">
    <h1 class="main">Главная</h1>
    <div class="top-movies">
        <router-link class="link" :to="{ name: 'movie', query: {sort: '-rate'} }">
          <h3 class="section-title">Фильмы с наивысшим рейтингом ></h3>
        </router-link>
    
    <div class="movie-list">
      <div v-for="movie in topMovies" :key="movie.id" class="movie-card">
        <router-link :to="{ name: 'movie-detail', params: { id: movie.id } }">
          <div class="poster-wrapper">
            <img
              v-if="movie.poster"
              :src="movie.poster"
              :alt="movie.title"
              class="poster"
            />
            <div v-else class="no-poster">
              <span>Нет постера</span>
            </div>

            <div class="rating-badge">
              ★ {{ movie.rate ? movie.rate.toFixed(1) : '0.0' }}
            </div>
          </div>
        </router-link>

        <router-link
          :to="{ name: 'movie-detail', params: { id: movie.id } }"
          class="movie-title"
        >
          {{ movie.title }}
        </router-link>
      </div>
    </div>
    </div>

    <div class="top-movies">
        <router-link class="link" :to="{ name: 'genre', query: {sort: '-movies_count'} }">
          <h3 class="section-title">Жанры с наибольшим количеством фильмов ></h3>
        </router-link>
        <Grid :items="topGenres" routeName="movie" queryKey="genre" queryValueField="name" />
    </div>

    <div class="top-movies">
        <router-link class="link" :to="{ name: 'person', query: {sort: 'birthday'} }">
          <h3 class="section-title">Скоро день рождения ></h3>
        </router-link>
        <div class="movie-list">
      <div v-for="person in closeBirthdays" :key="person.id" class="movie-card">
        <router-link :to="{ name: 'person-detail', params: { id: person.id } }">

            <div class="poster-wrapper">
                <img
              v-if="person.photo"
              :src="person.photo"
              :alt="person.full_name"
              class="poster"
            />
            <div v-else class="no-poster">
              <span>Нет фото</span>
            </div>
            <div v-if="todayBirthday(person.birth_date)" class="confetti">
                <span></span>
                <span></span>
                <span></span>
                <span></span>
                <span></span>
            </div>
                <div class="bday-badge">
              {{ todayBirthday(person.birth_date) ? 'cегодня, ' + formatDate(person.birth_date) : formatDate(person.birth_date)}}
            </div>

            </div>
        </router-link>

        <router-link
          :to="{ name: 'person-detail', params: { id: person.id } }"
          class="movie-title"
        >
          {{ person.full_name }}
        </router-link>
      </div>
    </div>
    </div>
    <h3 class="section-title"></h3>
</div>
</template>

<style scoped>
.confetti span {
  position: absolute;
  width: 6px;
  height: 12px;
  background-color: #f1c40f;
  top: -20px;
  left: 50%;
  transform: rotate(45deg);
  animation: fall 2s infinite ease-in-out;
  opacity: 0.8;
}

/* Делаем несколько разных цветов и задержек */
.confetti span:nth-child(1) { background: #f1c40f; left: 10%; animation-delay: 0s; }
.confetti span:nth-child(2) { background: #e74c3c; left: 30%; animation-delay: 0.3s; }
.confetti span:nth-child(3) { background: #2ecc71; left: 50%; animation-delay: 0.6s; }
.confetti span:nth-child(4) { background: #3498db; left: 70%; animation-delay: 0.9s; }
.confetti span:nth-child(5) { background: #9b59b6; left: 90%; animation-delay: 1.2s; }

@keyframes fall {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 1;
  }
  50% {
    transform: translateY(50px) rotate(180deg);
    opacity: 0.7;
  }
  100% {
    transform: translateY(100px) rotate(360deg);
    opacity: 0;
  }
}
.grid {
    padding: 0;
}
.main {
    text-align: center;
}
.link {
    text-decoration: none;
}
.movie-list-container {
    max-width: 1200px;
    margin-left: 12%;
    margin-right: 12%;
    padding: 20px;
    background: white;
}
.top-movies {
  margin: 30px 0;
  justify-content: center;
  margin: 1% 8%;
}

.section-title {
  font-size: 1.6rem;
  margin-bottom: 15px;
  color: #000000;
}
.section-title:hover {
    color: #ffa500;
}

.movie-list {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 10px;
  padding-top: 4px;
}

.movie-card {
  position: relative;
  min-width: 160px;
  flex-shrink: 0;
  text-align: center;
}

.poster-wrapper {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
  transition: transform 0.2s, box-shadow 0.2s;
}

.poster-wrapper:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 14px rgba(255, 165, 0, 0.4);
}

.poster {
  width: 170px;
  height: 240px;
  object-fit: cover;
  display: block;
}

.no-poster {
  width: 170px;
  height: 240px;
  background-color: #222;
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.rating-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background-color: rgba(60, 19, 0, 0.9);
  color: #fff;
  font-weight: bold;
  font-size: 0.9rem;
  padding: 3px 6px;
  border-radius: 8px;
}
.bday-badge {
  position: absolute;
  top: 205px;
  right: 8px;
  background-color: rgba(89, 255, 0, 0.9);
  color: #000000;
  font-size: 0.9rem;
  padding: 3px 6px;
  border-radius: 8px;
  width: 83%;
}

.movie-title {
  display: block;
  color: #000000;
  font-size: 0.95rem;
  margin-top: 6px;
  text-decoration: none;
  transition: color 0.2s;
}

.movie-title:hover {
  color: #ffa500;
}

@media (max-width: 1024px) {
  .movie-list-container {
    margin-left: 6%;
    margin-right: 6%;
    padding: 15px;
  }

  .section-title {
    font-size: 1.4rem;
  }

  .poster {
    width: 160px;
    height: 210px;
  }

  .no-poster {
    width: 150px;
    height: 210px;
  }

  .bday-badge {
    top: 180px;
    font-size: 0.85rem;
  }
}

/* --- Для экранов до 768px (мобильные в горизонтали, маленькие планшеты) --- */
@media (max-width: 768px) {
  .movie-list-container {
    margin: 0 4%;
    padding: 10px;
  }

  .main {
    font-size: 1.4rem;
  }

  .section-title {
    font-size: 1.2rem;
    text-align: center;
  }

  .movie-list {
    gap: 14px;
  }

  .movie-card {
    min-width: 140px;
  }

  .poster,
  .no-poster {
    width: 145px;
    height: 200px;
  }

  .bday-badge {
    top: 170px;
    font-size: 0.8rem;
  }
}

/* --- Для экранов до 480px (смартфоны) --- */
@media (max-width: 480px) {
  .movie-list-container {
    margin: 0 2%;
    padding: 8px;
  }

  .main {
    font-size: 1.2rem;
  }

  .section-title {
    font-size: 1rem;
    margin-bottom: 10px;
  }

  .movie-list {
    gap: 10px;
    padding-bottom: 6px;
  }

  .movie-card {
    min-width: 120px;
  }

  .poster,
  .no-poster {
    width: 120px;
    height: 170px;
  }

  .rating-badge {
    font-size: 0.75rem;
    padding: 2px 5px;
  }

  .bday-badge {
    top: 145px;
    font-size: 0.75rem;
    width: 80%;
  }

  .movie-title {
    font-size: 0.85rem;
  }

  .confetti span {
    width: 4px;
    height: 8px;
  }
}

/* --- Для очень маленьких экранов до 360px --- */
@media (max-width: 360px) {
  .poster,
  .no-poster {
    width: 100px;
    height: 150px;
  }

  .movie-card {
    min-width: 100px;
  }

  .movie-title {
    font-size: 0.75rem;
  }

  .section-title {
    font-size: 0.9rem;
  }
}
</style>