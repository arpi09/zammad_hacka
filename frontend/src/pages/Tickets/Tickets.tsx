/**
 * Tickets page component.
 * Follows Single Responsibility Principle - handles only tickets display.
 */
import { useQuery } from '@tanstack/react-query'
import { zammadService } from '../../services/zammadService'
import './Tickets.css'

const Tickets = () => {
  const { data: tickets, isLoading, error } = useQuery({
    queryKey: ['tickets'],
    queryFn: () => zammadService.getTickets(100),
  })

  if (isLoading) {
    return <div className="tickets-loading">Loading tickets...</div>
  }

  if (error) {
    return <div className="tickets-error">Error loading tickets: {error.message}</div>
  }

  return (
    <div className="tickets">
      <h2>Tickets</h2>
      {tickets && tickets.length > 0 ? (
        <div className="tickets-list">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="ticket-card">
              <h3>{ticket.title || `Ticket #${ticket.number || ticket.id}`}</h3>
              <p>State: {ticket.state || 'N/A'}</p>
              <p>Priority: {ticket.priority || 'N/A'}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No tickets found.</p>
      )}
    </div>
  )
}

export default Tickets

