import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDetailStore = defineStore('resourceDetail', () => {
  const name = ref(null)
  const items = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const apiFunc = ref(null)

  const setResource = (resourceName, api) => {
    name.value = resourceName
    apiFunc.value = api
  }

  const getParams = (url) => {
    if (!url) return {}
      // превращает ссылку API типа /movie/?page=2 в { page: "2" }
    return Object.fromEntries(new URL(url).searchParams)
  }

  const loadItems = async (id) => {
    if (!apiFunc.value) {
      console.error('API для ресурса не установлен!')
      return
    }
    loading.value = true
    error.value = null
    try {
      const response = await apiFunc.value(id)
    items.value = response.data
    } catch (err) {
      console.error(err)
      error.value = 'Ошибка при загрузке данных'
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    setResource,
    loadItems,
    getParams,
  }
})