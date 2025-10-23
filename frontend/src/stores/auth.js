import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || null)
  const isAuthenticated = computed((state) => !!state.token)
  
  const login = async (username, password) => {
    try {
    const res = await api.login(username, password)
    token.value = res.data.token
    user.value = res.user
    localStorage.setItem('token', token.value)
    await fetchUser()
    } catch (err) {
    console.error('Ошибка входа:', err)
    throw err // чтобы можно было поймать в компоненте
  }
  }
  const fetchUser = async () => {
    if (user.value) return
      if (!token.value) return
      const res = await api.me()
      user.value = res.data
    }
  const logout = async () => {
      await api.logout()
      token.value = null
      user.value = null
      localStorage.removeItem('token')
    }
  
    return { user, token, isAuthenticated, login, logout, fetchUser }
  })