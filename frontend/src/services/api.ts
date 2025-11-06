/**
 * API service for making HTTP requests.
 * Follows Single Responsibility Principle - handles only HTTP communication.
 */
import axios, { AxiosInstance, AxiosError } from 'axios'
import apiConfig from '../config/api'

class ApiService {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: apiConfig.baseURL,
      timeout: apiConfig.timeout,
      headers: apiConfig.headers,
    })

    this.setupInterceptors()
  }

  private setupInterceptors(): void {
    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add any request modifications here
        return config
      },
      (error) => {
        return Promise.reject(error)
      }
    )

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        // Handle errors globally
        if (error.response) {
          console.error('API Error:', error.response.status, error.response.data)
        } else if (error.request) {
          console.error('Network Error:', error.request)
        } else {
          console.error('Error:', error.message)
        }
        return Promise.reject(error)
      }
    )
  }

  public get<T>(url: string, config?: any): Promise<T> {
    return this.client.get<T>(url, config).then((response) => response.data)
  }

  public post<T>(url: string, data?: any, config?: any): Promise<T> {
    return this.client.post<T>(url, data, config).then((response) => response.data)
  }

  public put<T>(url: string, data?: any, config?: any): Promise<T> {
    return this.client.put<T>(url, data, config).then((response) => response.data)
  }

  public delete<T>(url: string, config?: any): Promise<T> {
    return this.client.delete<T>(url, config).then((response) => response.data)
  }
}

export const apiService = new ApiService()
export default apiService

