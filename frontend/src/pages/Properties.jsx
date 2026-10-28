import { useState, useEffect } from 'react';
import axios from 'axios';
import { Home, MapPin, Search } from 'lucide-react';

export default function Properties() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProperties = async () => {
      try {
        // Fetch from backend
        // const response = await axios.get('/api/properties');
        // setProperties(response.data);
        
        // Temporarily fetching from local API bridge via proxy or hardcoded for demo
        const response = await fetch('/api/properties');
        const data = await response.json();
        setProperties(data || []);
      } catch (error) {
        console.error("Error fetching properties:", error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchProperties();
  }, []);

  if (loading) {
    return <div className="flex justify-center items-center h-64"><div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div></div>;
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-gray-900">Registered Properties</h2>
        <div className="relative">
          <input 
            type="text" 
            placeholder="Search by ID or Location..." 
            className="pl-10 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-indigo-500 w-64"
          />
          <Search className="absolute left-3 top-2.5 text-gray-400" size={18} />
        </div>
      </div>
      
      {properties.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-12 text-center text-gray-500">
          <Home className="mx-auto text-gray-300 mb-4" size={64} />
          <h3 className="text-xl font-medium text-gray-700 mb-2">No Properties Found</h3>
          <p>There are currently no properties registered on the blockchain.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {properties.map((prop, idx) => (
            <div key={idx} className="bg-white rounded-xl overflow-hidden shadow-sm border border-gray-100 hover:shadow-md transition">
              <div className="h-48 bg-gradient-to-r from-blue-100 to-indigo-100 flex justify-center items-center">
                <Home className="text-indigo-300" size={64} />
              </div>
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <p className="text-xs font-bold text-indigo-600 uppercase tracking-wider mb-1">Property ID</p>
                    <h3 className="text-lg font-bold text-gray-900">{prop.property_id}</h3>
                  </div>
                  <span className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded-full font-medium">Verified</span>
                </div>
                
                <div className="space-y-3 mb-6">
                  <div className="flex items-start text-sm text-gray-600">
                    <MapPin className="mr-2 mt-0.5 text-gray-400 shrink-0" size={16} />
                    <p>{prop.details || "Details not specified in registry."}</p>
                  </div>
                  <div className="pt-3 border-t border-gray-100">
                    <p className="text-xs text-gray-500 mb-1">Owner Address</p>
                    <p className="text-sm font-mono text-gray-700 truncate" title={prop.owner}>{prop.owner}</p>
                  </div>
                </div>
                
                <button className="w-full py-2 bg-indigo-50 text-indigo-700 rounded-lg font-medium hover:bg-indigo-100 transition">
                  View Details
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
