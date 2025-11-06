/**
 * Dashboard page component.
 * Follows Single Responsibility Principle - handles only dashboard display.
 */
import { useQuery } from '@tanstack/react-query'
import { zammadService } from '../../services/zammadService'
import StatisticsCards from '../../components/Statistics/StatisticsCards'
import TicketCharts from '../../components/Charts/TicketCharts'
import './Dashboard.css'

const Dashboard = () => {
  const { data: statistics, isLoading, error } = useQuery({
    queryKey: ['ticketStatistics'],
    queryFn: () => zammadService.getTicketStatistics(),
  })

  if (isLoading) {
    return <div className="dashboard-loading">Loading statistics...</div>
  }

  if (error) {
    return <div className="dashboard-error">Error loading statistics: {error.message}</div>
  }

  return (
    <div className="dashboard">
      <h2>Dashboard</h2>
      {statistics && (
        <>
          <StatisticsCards statistics={statistics} />
          <TicketCharts statistics={statistics} />
        </>
      )}
    </div>
  )
}

export default Dashboard

