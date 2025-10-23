import axios from 'axios'
import { useAuthStore } from '@/stores/auth'

const apiClient = axios.create({
  baseURL: 'http://localhost:8001/catalog/',
  headers: {'Accept': 'application/json'},
  withCredentials: true,
})

apiClient.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.token) {
    config.headers.Authorization = `Token ${auth.token}`
  }
  return config
})

function createResourceApi(resource) {
  return {
    list(params = {}) {
      return apiClient.get(`${resource}/`, { params })
    },
    filter() {
      return apiClient.get(`${resource}/filter/`)
    },
    clear(id) {
      return apiClient.get(`${resource}/${id}/clear/`)
    },
    create(data) {
      return apiClient.post(`${resource}/`, data)
    },
    retrieve(id) {
      return apiClient.get(`${resource}/${id}/`)
    },
    update(id, data) {
      return apiClient.patch(`${resource}/${id}/`, data)
    },
    destroy(id) {
      return apiClient.delete(`${resource}/${id}/`)
    }
  }
}

export default {
  user: createResourceApi('user'),
  movie: createResourceApi('movie'),
  review: createResourceApi('review'),
  rating: createResourceApi('rating'),
  person: createResourceApi('person'),
  profession: createResourceApi('profession'),
  genre: createResourceApi('genre'),
  country: createResourceApi('country'),

  async login(username, password) {
  return await apiClient.post('login/', { username, password })
},
  async logout(){
  return await apiClient.post('logout/')
},
  async me(){
  return await apiClient.get('me/')
},
}