import { useState, useEffect } from 'react'
import axios from 'axios'
import { Activity, Box, Users, FileText } from 'lucide-react'

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalBlocks: 0,
    totalTransactions: 0,
    totalProperties: 0,
    activeUsers: 0
  })
  
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // We will fetch real stats from our backend API here
    const fetchStats = async () => {
      try {
        // Placeholder for API call
        // const response = await axios.get('/api/dashboard/stats')
        // setStats(response.data)
        
        // Mock data for now until backend is connected
        setTimeout(() => {
          setStats({
            totalBlocks: 5,
            totalTransactions: 12,
            totalProperties: 8,
            activeUsers: 3
          })
          setLoading(false)
        }, 500)
      } catch (error) {
        console.error("Error fetching stats:", error)
        setLoading(false)
      }
    }
    
    fetchStats()
  }, [])

  if (loading) {
    return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div>
  }

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">System Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-blue-50 text-blue-600 rounded-lg">
            <Box size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Total Blocks</p>
            <p className="text-2xl font-bold text-gray-900">{stats.totalBlocks}</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-green-50 text-green-600 rounded-lg">
            <Activity size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Transactions</p>
            <p className="text-2xl font-bold text-gray-900">{stats.totalTransactions}</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-purple-50 text-purple-600 rounded-lg">
            <FileText size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Properties Registered</p>
            <p className="text-2xl font-bold text-gray-900">{stats.totalProperties}</p>
          </div>
        </div>
        
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 flex items-center space-x-4">
          <div className="p-3 bg-orange-50 text-orange-600 rounded-lg">
            <Users size={24} />
          </div>
          <div>
            <p className="text-sm font-medium text-gray-500">Active Users</p>
            <p className="text-2xl font-bold text-gray-900">{stats.activeUsers}</p>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Recent Network Activity</h3>
        <div className="text-center py-10 text-gray-500">
          <p>Recent transactions will appear here once connected to the blockchain API.</p>
        </div>
      </div>
    </div>
  )
}
