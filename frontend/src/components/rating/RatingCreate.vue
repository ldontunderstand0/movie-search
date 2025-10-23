<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const auth = useAuthStore()
const rate = ref('')
const is_watched = ref('')

const submit = async () => {
    try {
    await api.rating.create(rate.value, is_watched.value, auth.user.id, )
    router.push({name: 'rating'})
  } catch (err) {
    alert('Ошибка создания', err)
  }
}
</script>
<template>
<div>
    <input v-model="rate" placeholder="Оценка" />
    <input v-model="is_watched" placeholder="Просмотр" />
    <button @click="submit">Войти</button>
</div>
</template>