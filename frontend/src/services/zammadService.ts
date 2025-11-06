/**
 * Service for Zammad API interactions.
 * Follows Single Responsibility Principle - handles only Zammad-related API calls.
 */
import apiService from './api'

export interface Ticket {
  id: number
  number?: string
  title?: string
  state?: string
  priority?: string
  created_at?: string
  updated_at?: string
  customer_id?: number
  organization_id?: number
}

export interface Organization {
  id: number
  name?: string
  active?: boolean
  created_at?: string
  updated_at?: string
}

export interface User {
  id: number
  login?: string
  firstname?: string
  lastname?: string
  email?: string
  active?: boolean
  created_at?: string
  updated_at?: string
}

export interface TicketStatistics {
  total_tickets: number
  open_tickets: number
  closed_tickets: number
  tickets_by_state: Record<string, number>
  tickets_by_priority: Record<string, number>
}

class ZammadService {
  private basePath = '/api/v1'

  async getTickets(limit?: number, offset?: number): Promise<Ticket[]> {
    const params = new URLSearchParams()
    if (limit) params.append('limit', limit.toString())
    if (offset) params.append('offset', offset.toString())
    
    const queryString = params.toString()
    const url = `${this.basePath}/tickets${queryString ? `?${queryString}` : ''}`
    return apiService.get<Ticket[]>(url)
  }

  async getTicket(id: number): Promise<Ticket> {
    return apiService.get<Ticket>(`${this.basePath}/tickets/${id}`)
  }

  async getOrganizations(limit?: number, offset?: number): Promise<Organization[]> {
    const params = new URLSearchParams()
    if (limit) params.append('limit', limit.toString())
    if (offset) params.append('offset', offset.toString())
    
    const queryString = params.toString()
    const url = `${this.basePath}/organizations${queryString ? `?${queryString}` : ''}`
    return apiService.get<Organization[]>(url)
  }

  async getUsers(limit?: number, offset?: number): Promise<User[]> {
    const params = new URLSearchParams()
    if (limit) params.append('limit', limit.toString())
    if (offset) params.append('offset', offset.toString())
    
    const queryString = params.toString()
    const url = `${this.basePath}/users${queryString ? `?${queryString}` : ''}`
    return apiService.get<User[]>(url)
  }

  async getTicketStatistics(): Promise<TicketStatistics> {
    return apiService.get<TicketStatistics>(`${this.basePath}/statistics/tickets`)
  }
}

export const zammadService = new ZammadService()
export default zammadService

