import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/catalog/'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  listMovie(params = {}) {
    return apiClient.get('/movie/', { params })
  },
  filterMovie() {
    return apiClient.get('/movie/filter/')
  },

  retrieveMovie(id) {
    return apiClient.get(`/movie/${id}/`)
  }
}