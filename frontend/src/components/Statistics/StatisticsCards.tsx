/**
 * Statistics cards component.
 * Follows Single Responsibility Principle - handles only statistics display.
 */
import { TicketStatistics } from '../../services/zammadService'
import './StatisticsCards.css'

interface StatisticsCardsProps {
  statistics: TicketStatistics
}

const StatisticsCards = ({ statistics }: StatisticsCardsProps) => {
  return (
    <div className="statistics-cards">
      <div className="stat-card">
        <h3>Total Tickets</h3>
        <p className="stat-value">{statistics.total_tickets}</p>
      </div>
      <div className="stat-card">
        <h3>Open Tickets</h3>
        <p className="stat-value">{statistics.open_tickets}</p>
      </div>
      <div className="stat-card">
        <h3>Closed Tickets</h3>
        <p className="stat-value">{statistics.closed_tickets}</p>
      </div>
    </div>
  )
}

export default StatisticsCards

