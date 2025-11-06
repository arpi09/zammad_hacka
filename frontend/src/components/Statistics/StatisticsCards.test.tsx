/**
 * Unit tests for StatisticsCards component.
 */
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import StatisticsCards from './StatisticsCards'
import { TicketStatistics } from '../../services/zammadService'

describe('StatisticsCards', () => {
  const mockStatistics: TicketStatistics = {
    total_tickets: 100,
    open_tickets: 60,
    closed_tickets: 40,
    tickets_by_state: { open: 60, closed: 40 },
    tickets_by_priority: { high: 20, medium: 50, low: 30 },
  }

  it('renders statistics cards correctly', () => {
    render(<StatisticsCards statistics={mockStatistics} />)

    expect(screen.getByText('Total Tickets')).toBeInTheDocument()
    expect(screen.getByText('Open Tickets')).toBeInTheDocument()
    expect(screen.getByText('Closed Tickets')).toBeInTheDocument()
    expect(screen.getByText('100')).toBeInTheDocument()
    expect(screen.getByText('60')).toBeInTheDocument()
    expect(screen.getByText('40')).toBeInTheDocument()
  })
})

