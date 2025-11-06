/**
 * Ticket charts component.
 * Follows Single Responsibility Principle - handles only chart visualization.
 */
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { TicketStatistics } from '../../services/zammadService'
import './TicketCharts.css'

interface TicketChartsProps {
  statistics: TicketStatistics
}

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']

const TicketCharts = ({ statistics }: TicketChartsProps) => {
  const stateData = Object.entries(statistics.tickets_by_state).map(([name, value]) => ({
    name,
    value,
  }))

  const priorityData = Object.entries(statistics.tickets_by_priority).map(([name, value]) => ({
    name,
    value,
  }))

  return (
    <div className="ticket-charts">
      <div className="chart-container">
        <h3>Tickets by State</h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={stateData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="chart-container">
        <h3>Tickets by Priority</h3>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={priorityData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {priorityData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
          </PieChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default TicketCharts

