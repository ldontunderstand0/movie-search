<script setup>
import { onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useDetailStore } from '@/stores/detailStore'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import MovieNav from './MovieNav.vue'
import { destroyButton, updateButton } from '@/components/buttons'

const auth = useAuthStore()
const route = useRoute()
const store = useDetailStore()
store.setResource('movie', api.movie.retrieve)

onMounted(() => {
  loadMovie()
})

// при смене id в URL
watch(
  () => route.params.id,
  async () => loadMovie()
)

async function loadMovie() {
  await store.loadItems(route.params.id)
}
</script>

<template>
<div v-if="store.loading">Загрузка...</div>
<div v-else-if="store.error" class="error">{{ store.error }}</div>
<div v-else-if="store.items" class="movie-detail-container" id="movie-list-container">

    <MovieNav :movie_id="store.items.id" active="movie"/>

    <div class="movie-header-section">
        <div class="movie-poster-section">
            <div class="movie-poster-wrapper">
                    <img v-if="store.items.poster" class="movie-poster-image" :src="store.items.poster" :alt="store.items.title">
                    <div v-else class="movie-poster-placeholder">
                        <span class="placeholder-text">Нет постера</span>
                    </div>
            </div>
        </div>

        <div class="movie-main-info">
            <div class="movie-title-section">
                <h1 class="movie-main-title">{{ store.items.title }} ({{ store.items.release_date.split("-")[0] }})</h1>
                <updateButton v-if="auth.user && auth.user.is_staff" name="movie-update" :id="route.params.id" />
                <destroyButton v-if="auth.user && auth.user.is_staff" :id="route.params.id" :api="api.movie"/>
            </div>

            <div class="movie-rating-section">
                <div class="rating-main">
                    <div class="rating-score">{{ store.items.rate ? store.items.rate : 0.0 }}</div>
                    <div class="rating-label">рейтинг</div>
                </div>
                <div class="rating-votes">количество оценок: {{ store.items.rates_count }}</div>
                <!-- <button class="rate-button">Изменить оценку</button> -->
            </div>

            <div class="info-left-column">
            <section class="info-section" role="region" aria-label="Информация о фильме"> 
                <h3 class="section-title">О фильме</h3>
                <div class="info-table">
                    <div class="info-row">
                        <div class="info-label">Год производства</div>
                        <div class="info-value">
                            <router-link :to="{name: 'movie', query: {year: store.items.release_date.split('-')[0]}}" class="actor-link">
                                {{ store.items.release_date.split("-")[0] }}
                            </router-link>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Страна</div>
                        <div class="info-value">
                                <router-link v-if="store.items.countries.length > 0" v-for="country in store.items.countries" :to="{name: 'movie', query: {country: country.name}}" class="actor-link">
                                    {{ country.name }}, </router-link>
                                <div v-else class="info-label">-</div>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Жанр</div>
                        <div class="info-value">
                            <router-link v-if="store.items.genres.length > 0" v-for="genre in store.items.genres" :to="{name: 'movie', query: {genre: genre.name}}" class="actor-link">
                                    {{ genre.name }}, </router-link>
                            <div v-else class="info-label">-</div>
                        </div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">Режиссер</div>
                        <div class="info-value">
                            <router-link v-if="store.items.countries.length > 0" v-for="director in store.items.directors" :to="{name: 'person-detail', params: {id: director.person__id}}" class="actor-link">
                                    {{ director.person__full_name }}, </router-link>
                            <div v-else class="info-label">-</div>
                        </div>
                    </div>
                </div>
            </section>
            </div>
        </div>
    </div>

    <!-- Описание фильма -->
    <section class="description-section" role="region" aria-label="Описание фильма">
        <h3 class="section-title">Описание</h3>
        <div v-if="store.items.description" class="movie-description">
            {{ store.items.description }}
        </div>
        <div v-else class="info-label">Нет описания</div>
    </section>

    <section class="video-section" role="region" aria-label="Трейлер фильма">
        <h3 class="section-title">Трейлер</h3>
        <section>
            <div v-if="store.items.trailer_url" class="video-wrapper">
                <iframe
                :src="store.items.trailer_url.replace('watch?v=', 'embed/')"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
                class="youtube-iframe"
                ></iframe>
            </div>
            <div v-else class="info-label">Нет трейлера</div>
        </section>
        
    </section>
</div>
</template>

<style scoped>
.destroy {
    margin-left: 2%;
}
.video-section {
    margin-top: 3%;
    margin-bottom: 3%;
    padding: 25px;
}
.video-section section {
    justify-content: center;
    display: flex;
}
.video-wrapper {
  position: relative;
  width: 50%;
  height: 50%;
  padding-bottom: 28.1%; /* 16:9 */
  height: 0;
}

.youtube-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}
/* Основной контейнер */
.movie-detail-container {
    max-width: 1200px;
    margin-left: 12%;
    margin-right: 12%;
    padding: 20px;
    background: white;
}

/* Верхняя секция */
.movie-header-section {
    display: flex;
    gap: 30px;
    margin-bottom: 40px;
    padding-bottom: 30px;
    border-bottom: 1px solid #e5e5e5;
}

/* Постер */
.movie-poster-section {
    flex-shrink: 0;
}

.movie-poster-wrapper {
    width: 260px;
    height: 380px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.movie-poster-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.movie-poster-placeholder {
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 16px;
}

/* Основная информация */
.movie-main-info {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 25px;
}

.movie-title-section {
    margin-bottom: 10px;
}

.movie-main-title {
    font-size: 36px;
    font-weight: 700;
    color: #000;
    margin: 0 0 8px 0;
    line-height: 1.2;
}

.movie-original-title {
    font-size: 20px;
    font-weight: 400;
    color: #666;
    margin: 0 0 12px 0;
    font-style: italic;
}

.movie-age-rating {
    display: inline-block;
    background: #ff8a00;
    color: white;
    padding: 4px 12px;
    border-radius: 4px;
    font-size: 14px;
    font-weight: 600;
}

/* Действия с фильмом */
.movie-actions {
    display: flex;
    gap: 15px;
    align-items: center;
}

.action-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 20px;
    border: 1px solid #ddd;
    border-radius: 6px;
    background: white;
    color: #333;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.action-button:hover {
    background: #f8f9fa;
    border-color: #ff8a00;
    transform: translateY(-1px);
}

.action-divider {
    width: 1px;
    height: 20px;
    background: #e5e5e5;
}

/* Рейтинг */
.movie-rating-section {
    display: flex;
    align-items: center;
    gap: 30px;
    background: #f8f9fa;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #e5e5e5;
}

.rating-main {
    text-align: center;
}

.rating-score {
    font-size: 32px;
    font-weight: 700;
    color: #000;
    line-height: 1;
}

.rating-label {
    font-size: 12px;
    color: #333333;
    margin-top: 4px;
}

.rating-top250 {
    text-align: center;
}

.top250-badge {
    background: #ff8a00;
    color: white;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 600;
    margin-bottom: 4px;
}

.top250-position {
    font-size: 14px;
    font-weight: 600;
    color: #000;
}

.rating-votes {
    font-size: 14px;
    color: #333333;
}

.rate-button {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.3s ease;
}

.rate-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

/* Секции информации */
.movie-info-sections {
    display: grid;
    grid-template-columns: 2fr 1fr;
    gap: 40px;
    margin-bottom: 40px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #000;
    margin: 0 0 20px 0;
    padding-bottom: 10px;
    border-bottom: 2px solid #ff8a00;
}

/* Таблица информации */
.info-table {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.info-row {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    padding: 8px 0;
    border-bottom: 1px solid #f0f0f0;
}

.info-row:last-child {
    border-bottom: none;
}

.info-label {
    font-weight: 500;
    color: #3f3f3f;
    width: 140px;
    flex-shrink: 0;
    font-size: 14px;
}

.info-value {
    flex: 1;
    color: #000;
    font-size: 14px;
    line-height: 1.4;
}

.genre-link {
    color: #ff8a00;
    text-decoration: none;
}

.genre-link:hover {
    text-decoration: underline;
}

/* Секция актеров */
.cast-section {
    margin-bottom: 30px;
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

.show-all-link {
    color: #ff8a00;
    text-decoration: none;
    font-size: 14px;
    font-weight: 500;
}

.show-all-link:hover {
    text-decoration: underline;
}

.cast-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.cast-item {
    padding: 4px 0;
}

.actor-link {
    color: #000;
    text-decoration: none;
    font-size: 14px;
    transition: color 0.2s;
}

.actor-link:hover {
    color: #ff8a00;
}

/* Секция дубляжа */
.dubbing-section {
    margin-bottom: 30px;
}

.dubbing-list {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.dubbing-item {
    font-size: 14px;
    color: #666;
    padding: 3px 0;
}

/* Описание */
.description-section {
    background: #f8f9fa;
    padding: 25px;
    border-radius: 8px;
    border: 1px solid #e5e5e5;
}

.movie-description {
    font-size: 16px;
    line-height: 1.6;
    color: #333;
}
/* Анимации */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.movie-header-section {
    animation: fadeInUp 0.6s ease-out;
}

.movie-info-sections {
    animation: fadeInUp 0.6s ease-out 0.1s both;
}

.description-section {
    animation: fadeInUp 0.6s ease-out 0.2s both;
}

/* Дополнительные стили */
.button-icon {
    font-size: 16px;
}

.rating-main .rating-score {
    background: linear-gradient(135deg, #ff8a00, #ff5e00);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Адаптивность */
@media (max-width: 800px) {
    .movie-detail-container {
        padding: 20px 15px;
        margin: 1%;

    }

    .movie-header-section {
        flex-direction: column;
        gap: 20px;
    }

    .movie-poster-wrapper {
        width: 200px;
        height: 300px;
        margin: 0 auto;
    }

    .movie-main-title {
        font-size: 28px;
        text-align: center;
    }

    .movie-rating-section {
        flex-direction: column;
        gap: 20px;
        text-align: center;
    }

    .movie-info-sections {
        grid-template-columns: 1fr;
        gap: 30px;
    }

    .info-row {
        flex-direction: column;
        gap: 5px;
    }

    .info-label {
        width: auto;
        font-weight: 600;
    }
}



@media (max-width: 480px) {
  .movie-detail-container {
    margin: 0 1%;
    padding: 3%;
  }
  .video-wrapper {
    width: 300px;
    height: 70px;
  }

}  

</style>