import { Routes, Route, useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DashboardPage from './pages/DashboardPage';
import NetworkDetailPage from './pages/NetworkDetailPage';
import SettingsPage from './pages/SettingsPage';

function getTitle(pathname) {
  if (pathname.startsWith('/networks/')) return 'Network Detail';
  switch (pathname) {
    case '/':
      return 'Dashboard';
    case '/networks':
      return 'Networks';
    case '/settings':
      return 'Settings';
    default:
      return 'Dashboard';
  }
}

function App() {
  const location = useLocation();
  const title = getTitle(location.pathname);

  return (
    <div className="flex h-screen bg-light-background dark:bg-dark-background text-light-text dark:text-dark-text">
      {/* Sidebar */}
      <div className="w-64 flex-shrink-0">
        <Sidebar />
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <header className="bg-light-card dark:bg-dark-card shadow-sm border-b border-light-border dark:border-dark-border">
          <div className="max-w-7xl mx-auto py-4 px-4 sm:px-6 lg:px-8">
            <h1 className="text-lg font-semibold">
              {title}
            </h1>
          </div>
        </header>

        <main className="flex-1 overflow-y-auto">
          <div className="py-6">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/networks" element={<div className="px-4">Networks Page Placeholder</div>} />
              <Route path="/networks/:networkId" element={<NetworkDetailPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
