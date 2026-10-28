import { Routes, Route, Link } from 'react-router-dom'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Properties from './pages/Properties'
import Marketplace from './pages/Marketplace'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans flex flex-col">
      <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-50 shadow-sm border-b border-gray-100 px-6 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">
          LandRegistry
        </Link>
        <div className="space-x-6 font-medium">
          <Link to="/" className="text-gray-600 hover:text-indigo-600 transition">Home</Link>
          <Link to="/marketplace" className="text-gray-600 hover:text-indigo-600 transition">Trade</Link>
          <Link to="/properties" className="text-gray-600 hover:text-indigo-600 transition">Properties</Link>
          <Link to="/dashboard" className="text-gray-600 hover:text-indigo-600 transition">Dashboard</Link>
          <Link to="/login" className="px-4 py-2 text-indigo-600 bg-indigo-50 rounded-full hover:bg-indigo-100 transition">Log In</Link>
        </div>
      </nav>
      <main className="flex-grow p-6 flex flex-col">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/properties" element={<Properties />} />
          <Route path="/marketplace" element={<Marketplace />} />
        </Routes>
      </main>
      <footer className="bg-white border-t border-gray-200 py-8 text-center text-gray-500">
        <p>© 2026 Land Registry Blockchain System. All rights reserved.</p>
      </footer>
    </div>
  )
}

export default App

