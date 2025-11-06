/**
 * Layout component for the application.
 * Follows Single Responsibility Principle - handles only layout structure.
 */
import { ReactNode } from 'react'
import './Layout.css'

interface LayoutProps {
  children: ReactNode
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="layout">
      <header className="layout-header">
        <h1>Zammad Hacka</h1>
        <nav className="layout-nav">
          <a href="/">Dashboard</a>
          <a href="/tickets">Tickets</a>
        </nav>
      </header>
      <main className="layout-main">
        {children}
      </main>
      <footer className="layout-footer">
        <p>&copy; 2024 Zammad Hacka</p>
      </footer>
    </div>
  )
}

export default Layout

