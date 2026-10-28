import React from 'react';
import { Link } from 'react-router-dom';
import { Shield, Lock, Globe, ArrowRight } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex flex-col min-h-[80vh]">
      {/* Hero Section */}
      <div className="flex-grow flex flex-col items-center justify-center text-center px-4 py-20 bg-gradient-to-b from-indigo-50 to-white">
        <h1 className="text-5xl md:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600 mb-6 tracking-tight">
          Land Registry System
        </h1>
        <p className="text-xl md:text-2xl text-gray-600 mb-10 max-w-3xl">
          Secure, transparent, and immutable property records powered by blockchain technology. Buy, sell, and verify land with absolute confidence.
        </p>
        <div className="flex space-x-4">
          <Link to="/register" className="px-8 py-4 bg-indigo-600 text-white rounded-full font-semibold text-lg hover:bg-indigo-700 transition shadow-lg hover:shadow-xl flex items-center">
            Get Started <ArrowRight className="ml-2" size={20} />
          </Link>
          <Link to="/dashboard" className="px-8 py-4 bg-white text-indigo-600 border border-indigo-200 rounded-full font-semibold text-lg hover:bg-indigo-50 transition shadow-sm">
            View Explorer
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-blue-100 text-blue-600 rounded-2xl">
                  <Shield size={40} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Immutable Records</h3>
              <p className="text-gray-500">Property deeds and transfer histories are permanently recorded on the blockchain, preventing fraud and tampering.</p>
            </div>
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-purple-100 text-purple-600 rounded-2xl">
                  <Lock size={40} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Cryptographic Security</h3>
              <p className="text-gray-500">State-of-the-art encryption guarantees that only authorized owners can initiate transfers or tokenization.</p>
            </div>
            <div className="text-center">
              <div className="flex justify-center mb-4">
                <div className="p-4 bg-green-100 text-green-600 rounded-2xl">
                  <Globe size={40} />
                </div>
              </div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Global Accessibility</h3>
              <p className="text-gray-500">Verify property ownership from anywhere in the world instantly without relying on slow bureaucratic processes.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
