import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import SetupPage from './pages/SetupPage';
import FeedPage from './pages/FeedPage';
import MatchesPage from './pages/MatchesPage';
import ChatPage from './pages/ChatPage';
import ProfilePage from './pages/ProfilePage';
import BottomNav from './components/BottomNav';
import './styles.css';

function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const tokens = localStorage.getItem('tokens');
  if (!tokens) return <Navigate to="/login" replace />;
  return (
    <div className="app">
      <div className="main-layout">
        {children}
      </div>
      <BottomNav />
    </div>
  );
}

export default function App() {
  return (
    <HashRouter>
      <div className="app">
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/setup" element={<ProtectedRoute><SetupPage /></ProtectedRoute>} />
          <Route path="/feed" element={<ProtectedRoute><FeedPage /></ProtectedRoute>} />
          <Route path="/matches" element={<ProtectedRoute><MatchesPage /></ProtectedRoute>} />
          <Route path="/chat/:matchId" element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />
          <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
          <Route path="*" element={<Navigate to="/feed" replace />} />
        </Routes>
      </div>
    </HashRouter>
  );
}
