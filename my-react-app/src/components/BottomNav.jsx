import { NavLink } from 'react-router-dom'
import './BottomNav.css'

const TABS = [
  { to: '/', label: 'Bus', icon: '🚌', end: true },
  { to: '/nearest-stop', label: 'Nearest Stop', icon: '📍' },
  { to: '/taxi-share', label: 'Taxi Share', icon: '🚕' },
  { to: '/profile', label: 'Profile', icon: '👤' },
]

function BottomNav() {
  return (
    <nav className="bottom-nav">
      {TABS.map((tab) => (
        <NavLink
          key={tab.to}
          to={tab.to}
          end={tab.end}
          className={({ isActive }) =>
            'bottom-nav-item' + (isActive ? ' active' : '')
          }
        >
          <span className="bottom-nav-icon" aria-hidden="true">
            {tab.icon}
          </span>
          <span className="bottom-nav-label">{tab.label}</span>
        </NavLink>
      ))}
    </nav>
  )
}

export default BottomNav
