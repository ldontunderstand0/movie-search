import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useResourceStore = defineStore('resource', () => {
  const items = ref([])
  const count = ref(0)
  const next = ref(null)
  const previous = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const apiFunc = ref(null)
  const apiFilter = ref(null)

  const currentPage = computed(() => {
      if (next.value) {
        return getParams(next.value).page - 1
      }
      else {
        return totalPages.value
      }
  })

  const totalPages = computed(() => {return Math.ceil(count.value / 10)})

  const shownItems = computed(() => {
    const start = (currentPage.value - 1) * 10 + 1
    const end = Math.min(currentPage.value * 10, count.value)
    return `${start} - ${end}`
  })

  const currentParams = ref({})

  const maxVisiblePages = ref(3)

  const visiblePages = computed(() => {
    const half = Math.floor(maxVisiblePages.value / 2)
    let start = Math.max(1, currentPage.value - half)
    let end = Math.min(totalPages.value, start + maxVisiblePages.value - 1)
    
    // Корректируем start, если мы в конце списка
    start = Math.max(1, end - maxVisiblePages.value + 1)
    
    const pages = []
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    return pages
  })

  const filter = ref({})

  const setResource = (api, filter) => {
    apiFunc.value = api
    apiFilter.value = filter
  }

  const getParams = (url) => {
    if (!url) return {}
      // превращает ссылку API типа /movie/?page=2 в { page: "2" }
    return Object.fromEntries(new URL(url).searchParams)
  }

    const updatePage = (params, pageNum) => {
      const newParams = { ...params, page: pageNum}
      if (pageNum === 1) {
        delete newParams.page
      }
    return newParams
  }

  const loadItems = async (params = {}) => {
    if (!apiFunc.value) {
      console.error('API для ресурса не установлен!')
      return
    }

    if (!apiFilter.value) {
      console.error('Filter для ресурса не установлен!')
      return
    }

    loading.value = true
    error.value = null
    try {
      const { data } = await apiFunc.value(params)
      items.value = data.results
      count.value = data.count
      next.value = data.next
      previous.value = data.previous
      currentParams.value = params
    } catch (err) {
      console.error(err)
      error.value = 'Ошибка при загрузке данных'
    } finally {
      loading.value = false
    }

    try {
      const { data } = await apiFilter.value()
      filter.value = data
    } catch (err) {
      console.error(err)
      error.value = 'Ошибка при загрузке filter'
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    count,
    previous,
    next,
    loading,
    error,
    totalPages,
    currentPage,
    shownItems,
    currentParams,
    visiblePages,
    filter,
    setResource,
    loadItems,
    getParams,
    updatePage,
  }
})