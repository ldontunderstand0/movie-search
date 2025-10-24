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
  <div class="login-container" id="movie-list-container">
    <div class="card">
      <div class="card-header">
                <h4 class="mb-0">Вход</h4>
            </div>
      <div class="card-body">
        <div class="mb-2"><label for="username" class="form-label">Имя пользователя</label></div>
        <div class="mb-3"><input class="form-input" v-model="username" id="username" /></div>
        <div class="mb-2"><label for="password" class="form-label">Пароль</label></div>
        <div class="mb-3"><input class="form-input" v-model="password" type="password" id="password"/></div>
        <div class="mb-3"><button class="btn btn-primary" @click="submit"><div class="form-label">Войти</div></button></div>
      </div>
    </div>

    <div v-if="auth.user">Привет, {{ auth.user.username }}!</div>
    <div v-if="auth.error" class="error">{{ auth.error }}</div>
  </div>
</template>

<style scoped>
.mb-0 {
  margin: 5%;
}
.login-container {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: #f5f5f5;
    margin: 0;
    padding: 0;
    color: #333;
    max-width: 400px;
    width: 100%;
    padding: 20px;
    margin: 0 auto;
    margin-top: 5%;
}
.card {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border: none;
    border-radius: 10px;
}
.card-header {
    background-color: rgba(33, 37, 41, 1);
    color: white;
    text-align: center;
    border-radius: 10px 10px 0 0 !important;
    padding: 5px 15px;
}
.btn-primary {
    margin-top: 5%;
    background-color: rgba(33, 37, 41, 1);
    border: none;
    padding: 10px;
    color: white;
    font-weight: 500;
    border-radius: 10%;
    margin-bottom: 5%;
}
.form-label {
    margin-top: 5%;
    margin-bottom: 2%;
    font-weight: 500;
}
.register-link {
    text-align: center;
    margin-top: 15px;
}
.mb-3 {
display: flex;
justify-content: center;
}
.form-input {
        border-radius: 5px;
}
.mb-2 {
display: flex;
justify-content: center;

}
@media (max-width: 480px) {
  .login-container {
    width: auto;
  }
}
</style>