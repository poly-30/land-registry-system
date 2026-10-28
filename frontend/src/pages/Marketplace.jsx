import { useState, useEffect } from 'react';
import { ShoppingCart, Tag, AlertCircle } from 'lucide-react';

export default function Marketplace() {
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [buyId, setBuyId] = useState('');
  const [sellId, setSellId] = useState('');
  const [newOwner, setNewOwner] = useState('');
  const [message, setMessage] = useState({ type: '', text: '' });

  useEffect(() => {
    fetchProperties();
  }, []);

  const fetchProperties = async () => {
    try {
      const response = await fetch('/api/properties');
      const data = await response.json();
      setProperties(data || []);
    } catch (error) {
      console.error("Error fetching properties:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleBuy = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });
    // In a real app, this would deduct funds. Here we just transfer ownership to the logged-in user.
    // For demo, we'll prompt for the "new owner address" in the form below, but for a one-click buy:
    try {
      const response = await fetch('/api/transactions/transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          property_id: buyId,
          to_address: '0xBuyerAddress' + Math.floor(Math.random()*1000), // mock buyer address
          sale_price: 100000
        })
      });
      const data = await response.json();
      if (response.ok) {
        setMessage({ type: 'success', text: 'Property purchased successfully!' });
        fetchProperties();
      } else {
        setMessage({ type: 'error', text: data.message || 'Error purchasing property.' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error.' });
    }
  };

  const handleSell = async (e) => {
    e.preventDefault();
    setMessage({ type: '', text: '' });
    try {
      const response = await fetch('/api/transactions/transfer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          property_id: sellId,
          to_address: newOwner,
          sale_price: 150000
        })
      });
      const data = await response.json();
      if (response.ok) {
        setMessage({ type: 'success', text: 'Property ownership transferred successfully!' });
        fetchProperties();
      } else {
        setMessage({ type: 'error', text: data.message || 'Error transferring property.' });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Network error.' });
    }
  };

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      <div className="mb-8">
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Marketplace</h2>
        <p className="text-gray-600">Buy properties or transfer your property ownership securely on the blockchain.</p>
      </div>

      {message.text && (
        <div className={`p-4 rounded-lg flex items-center ${message.type === 'error' ? 'bg-red-50 text-red-700' : 'bg-green-50 text-green-700'}`}>
          <AlertCircle className="mr-2" size={20} />
          {message.text}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Buy Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
          <div className="flex items-center space-x-3 mb-6 border-b border-gray-100 pb-4">
            <div className="p-3 bg-indigo-50 text-indigo-600 rounded-lg">
              <ShoppingCart size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-800">Buy Property</h3>
          </div>
          
          <form onSubmit={handleBuy} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Select Property to Buy</label>
              <select 
                value={buyId} 
                onChange={(e) => setBuyId(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                required
              >
                <option value="">-- Select a property --</option>
                {properties.map(p => (
                  <option key={p.property_id} value={p.property_id}>
                    {p.property_id} - {p.details}
                  </option>
                ))}
              </select>
            </div>
            <button type="submit" className="w-full py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:bg-indigo-700 transition">
              Purchase Property
            </button>
            <p className="text-xs text-gray-500 text-center mt-2">
              Note: This demo will automatically generate a mock buyer address and execute the transfer.
            </p>
          </form>
        </div>

        {/* Sell Section */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-8">
          <div className="flex items-center space-x-3 mb-6 border-b border-gray-100 pb-4">
            <div className="p-3 bg-green-50 text-green-600 rounded-lg">
              <Tag size={24} />
            </div>
            <h3 className="text-xl font-bold text-gray-800">Sell / Transfer Property</h3>
          </div>

          <form onSubmit={handleSell} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Select Your Property</label>
              <select 
                value={sellId} 
                onChange={(e) => setSellId(e.target.value)}
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:outline-none"
                required
              >
                <option value="">-- Select a property --</option>
                {properties.map(p => (
                  <option key={p.property_id} value={p.property_id}>
                    {p.property_id} - Owned by {p.owner.substring(0,8)}...
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">New Owner's Address</label>
              <input 
                type="text" 
                value={newOwner}
                onChange={(e) => setNewOwner(e.target.value)}
                placeholder="e.g. 0xabcdef123456..."
                className="w-full border border-gray-300 rounded-lg px-4 py-2 focus:ring-2 focus:ring-green-500 focus:outline-none"
                required
              />
            </div>
            <button type="submit" className="w-full py-3 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition">
              Transfer Ownership
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
