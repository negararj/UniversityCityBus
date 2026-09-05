import { Routes, Route } from 'react-router-dom'
import BottomNav from './components/BottomNav.jsx'
import Home from './screens/Home.jsx'
import NearestStop from './screens/NearestStop.jsx'
import TaxiShare from './screens/TaxiShare.jsx'
import Profile from './screens/Profile.jsx'
import './App.css'

function App() {
  return (
    <div className="app-shell">
      <main className="app-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/nearest-stop" element={<NearestStop />} />
          <Route path="/taxi-share" element={<TaxiShare />} />
          <Route path="/profile" element={<Profile />} />
        </Routes>
      </main>
      <BottomNav />
    </div>
  )
}

export default App
