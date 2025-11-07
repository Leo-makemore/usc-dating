import axios from 'axios'

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

// Add request interceptor for better error handling
api.interceptors.request.use(
  (config) => {
    // Add token to requests if available
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor for better error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.code === 'ECONNABORTED') {
      error.message = 'Request timeout. Please check if the backend server is running.'
    } else if (error.message === 'Network Error' || error.code === 'ERR_NETWORK') {
      error.message = 'Network Error: Cannot connect to backend server. Please make sure the backend is running on http://localhost:8000'
    }
    return Promise.reject(error)
  }
)

export default api

