import { Routes, Route } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import NetworkDetailPage from './pages/NetworkDetailPage';
import ClientDetailPage from './pages/ClientDetailPage';

function App() {
  return (
    <div className="bg-gray-100 min-h-screen font-sans">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <h1 className="text-3xl font-bold text-gray-900">Meraki Control</h1>
        </div>
      </header>

      <Routes>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/networks/:networkId" element={<NetworkDetailPage />} />
        <Route path="/clients/:clientMac" element={<ClientDetailPage />} />
      </Routes>
    </div>
  )
}

export default App;
