<script setup>
import { onMounted, watch, toRaw, reactive, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

watch(
  () => route.params.id,
  async () => {
    if (route.params.id) {
         await loadMovie()
    }
    },
  { immediate: true }
)

async function loadMovie() {
  const responce = await api.movie.clear(route.params.id)
  const data = responce.data
  item.title = data.title
  item.type = data.type
  item.release_date = data.release_date
  item.description = data.description
  item.genres = data.genres
  item.countries = data.countries
  item.poster = data.poster
  item.trailer_url = data.trailer_url
}

const item = reactive({
    type: 'Фильм',
    title: null,
    release_date: null,
    description: null,
    genres: [],
    countries: [],
    poster: null,
    trailer_url: null,
})

const genres = ref([])
const countries = ref([])

const posterPreview = computed(() => {
  if (!item.poster) return null

  // если это файл или blob (новый загруженный файл)
  if (item.poster instanceof File || item.poster instanceof Blob) {
    return window.URL.createObjectURL(item.poster)
  }

  // если это строка (URL с сервера)
  if (typeof item.poster === 'string') {
    return item.poster
  }

  // для всяких неожиданных типов
  return null
})

const getGenres = async () => {
    const responce =  await api.genre.list()
    return responce.data.results
}
const getCountries = async () => {
    const responce =  await api.country.list()
    return responce.data.results
}

const save = async () => {
    console.log(toRaw(item))
  if (!item.title || !item.release_date) {
    alert('Заполните обязательные поля: Название и Дата релиза')
    return
  }
  const formData = new FormData()
  formData.append('title', item.title)
  formData.append('type', item.type)
  formData.append('release_date', item.release_date)
  formData.append('description', item.description || '')

  item.genres.forEach(id => formData.append('genres', Number(id)))
  item.countries.forEach(id => formData.append('countries', Number(id)))

  if (item.poster instanceof File) formData.append('poster', item.poster)

  formData.append('trailer_url', item.trailer_url || '')
  try {
  if (route.params.id) {
    await api.movie.update(route.params.id, formData)
    router.push({ name: 'movie-detail', params: { id: route.params.id } })
  } else {
    await api.movie.create(formData)
    router.push({ name: 'movie' })
  }
} catch (err) {
  console.error('Ошибка API:', err.response?.data || err.message)
  alert('Ошибка при сохранении фильма. Проверьте консоль.')
}
}

const onFileChange = (event) => {
  const file = event.target.files[0]
  if (!file) return
  item.poster = file
}

onMounted(async () => {
  console.log('Компонент смонтирован!')
  genres.value = await getGenres()
  countries.value = await getCountries()
})

</script>
<template>
<div id="movie-list-container">
    <router-link 
    :to="route.params.id ? {name: 'movie-detail', params: {id: route.params.id}} : {name: 'movie'}"
    class="back-link">&laquo; Назад</router-link>
    <h1>
      {{ route.params.id ? 'Редактировать фильм' : 'Добавить новый фильм' }}
    </h1>
    
    <div>
      <label class="required">Название</label>
      <input v-model="item.title" type="text" />
    </div>

    <!-- Тип -->
    <div>
      <label>Тип</label>
      <select v-model="item.type">
        <option value="Фильм">Фильм</option>
        <option value="Сериал">Сериал</option>
      </select>
    </div>

    <!-- Дата релиза -->
    <div>
      <label class="required">Дата релиза</label>
      <input v-model="item.release_date" type="date" />
    </div>

    <!-- Описание -->
    <div>
      <label>Описание</label>
      <textarea v-model="item.description"/>
    </div>

    <!-- Жанры -->
    <div>
      <label class="block font-medium">Жанры</label>
        <select v-model="item.genres" multiple>
            <option v-for="genre in genres" :key="genre.id" :value="genre.id">
            {{ genre.name }}
            </option>
        </select>
    </div>

    <!-- Страны -->
    <div>
      <label>Страны</label>
      <select v-model="item.countries" multiple>
    <option v-for="country in countries" :key="country.id" :value="country.id">
      {{ country.name }}
    </option>
  </select>
    </div>

    <!-- Постер -->
    <div>
      <label>Постер (URL)</label>
      <input @change="onFileChange" accept="image/*" type="file"/>
    </div>

    <div v-if="posterPreview">
        <img :src="posterPreview" alt="Превью" class="w-32 h-auto mt-2"/>
    </div>

    <!-- Трейлер -->
    <div>
      <label class="block font-medium">Ссылка на трейлер</label>
      <input v-model="item.trailer_url" type="url"/>
    </div>

    <!-- Кнопка -->
    <button @click="save">{{ route.params.id ? 'Сохранить изменения' : 'Добавить фильм' }}</button>
</div>
</template>

<style scoped>
.back-link {
  display: inline-block;
  padding: 8px 16px;
  background-color: #f1f1f1; /* тёмный фон */
  color: #000000; /* жёлтый текст */
  text-decoration: none;
  font-weight: bold;
  border: 1px solid #444;
  border-radius: 8px;
  transition: background-color 0.2s, color 0.2s, transform 0.1s;
  cursor: pointer;
}

.back-link:hover {
  background-color: #ffcc00;
  color: #1b1b1b;
  transform: translateY(-2px);
}
label.required::after {
  content: ' *';
  color: #ff4d4f; /* красный */
  margin-left: 2px;
}

form *, div * {
  box-sizing: border-box;
}
form, div {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #e6e6e6; /* тёмный фон */
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  color: #000000;
  font-family: 'Arial', sans-serif;
}

/* Заголовки */
h1 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
  color: #000000; /* жёлтый, как Кинопоиск */
  text-align: center;
}

/* Метки */
label {
  display: block;
  font-weight: 600;
  margin-bottom: 6px;
  color: #000000;
}

/* Текстовые поля и textarea */
input[type="text"],
input[type="url"],
input[type="date"],
select,
textarea {
  width: 100%;
  padding: 10px 12px;
  border-radius: 8px;
  border: 1px solid #444;
  background-color: #f4f4f4;
  color: #000000;
  font-size: 1rem;
  margin-bottom: 15px;
  transition: border 0.2s, box-shadow 0.2s;
}
textarea {
  min-height: 200px; /* базовая высота */
  line-height: 1.5;
}
input[type="text"]:focus,
input[type="url"]:focus,
input[type="date"]:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #ffcc00;
  box-shadow: 0 0 5px #ffcc00;
}

/* Множественный выбор */
select[multiple] {
  height: 120px;
}

/* Кнопка */
button {
  background-color: #ffffff;
  color: #1b1b1b;
  padding: 12px 20px;
  font-size: 1rem;
  font-weight: bold;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.1s;
  width: 100%;
  margin-top: 10px;
}

button:hover {
  background-color: #e6b800;
  transform: translateY(-2px);
}

/* Превью постера */
img {
  border-radius: 8px;
  margin-top: 10px;
  max-width: 30%;
  display: block;
  box-shadow: 0 4px 10px rgba(0,0,0,0.6);
}

/* Фокус на чекбоксы / multiple select элементы */
select[multiple] option:checked {
  background-color: #ffcc00;
  color: #1b1b1b;
}
</style>