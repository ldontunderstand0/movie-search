import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:8000/catalog/',
  headers: {'Content-Type': 'application/json'}
})

function createResourceApi(resource) {
  return {
    list(params = {}) {
      return apiClient.get(`/${resource}/`, { params })
    },
    filter() {
      return apiClient.get(`/${resource}/filter/`)
    },
    retrieve(id) {
      return apiClient.get(`/${resource}/${id}/`)
    },
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
}