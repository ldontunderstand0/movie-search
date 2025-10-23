<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const username = ref('')
const password = ref('')

const submit = async () => {
    try {
    await auth.login(username.value, password.value)
    router.push({name: 'index'})
  } catch (err) {
    alert('Ошибка входа')
  }
}
</script>

<template>
  <div>
    <input v-model="username" placeholder="Логин" />
    <input v-model="password" type="password" placeholder="Пароль" />
    <button @click="submit">Войти</button>

    <div v-if="auth.user">Привет, {{ auth.user.username }}!</div>
    <div v-if="auth.error" class="error">{{ auth.error }}</div>
  </div>
</template>