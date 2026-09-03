import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Register from './pages/Register';
import UserDashboard from './pages/UserDashboard';
import ChatbotPage from './pages/ChatbotPage';
import ReportFaultPage from './pages/ReportFaultPage';
import MyTicketsPage from './pages/MyTicketsPage';
import TicketDetailsPage from './pages/TicketDetailsPage';
import StaffDashboard from './pages/StaffDashboard';
import AdminDashboard from './pages/AdminDashboard';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import AITransparencyPage from './pages/AITransparencyPage';
import AnalyticsPage from './pages/AnalyticsPage';
import { getUser } from './services/api';

export default function App() {
  const [user, setUser] = useState(getUser());
  const [authView, setAuthView] = useState('login'); // 'login' or 'register'
  const [currentPage, setCurrentPage] = useState('dashboard');
  const [selectedTicketId, setSelectedTicketId] = useState(null);

  useEffect(() => {
    if (user) {
      if (user.role === 'STAFF') {
        setCurrentPage('staff_dashboard');
      } else if (user.role === 'ADMIN') {
        setCurrentPage('admin_dashboard');
      } else {
        setCurrentPage('dashboard');
      }
    }
  }, [user]);

  if (!user) {
    if (authView === 'register') {
      return (
        <Register
          onLoginSuccess={(u) => setUser(u)}
          switchToLogin={() => setAuthView('login')}
        />
      );
    }
    return (
      <Login
        onLoginSuccess={(u) => setUser(u)}
        switchToRegister={() => setAuthView('register')}
      />
    );
  }

  const renderContent = () => {
    switch (currentPage) {
      case 'dashboard':
        return <UserDashboard setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
      case 'chat':
        return <ChatbotPage setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
      case 'report':
        return <ReportFaultPage setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
      case 'tickets':
        return <MyTicketsPage setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
      case 'ticket_details':
        return <TicketDetailsPage ticketId={selectedTicketId} setCurrentPage={setCurrentPage} />;
      case 'staff_dashboard':
        return <StaffDashboard setSelectedTicketId={setSelectedTicketId} setCurrentPage={setCurrentPage} />;
      case 'admin_dashboard':
        return <AdminDashboard setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
      case 'knowledge_base':
        return <KnowledgeBasePage />;
      case 'ai_transparency':
        return <AITransparencyPage />;
      case 'analytics':
        return <AnalyticsPage />;
      default:
        return <UserDashboard setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />;
    }
  };

  return (
    <div className="app-container">
      <Sidebar currentPage={currentPage} setCurrentPage={setCurrentPage} />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0 }}>
        <Navbar currentPage={currentPage} setCurrentPage={setCurrentPage} setSelectedTicketId={setSelectedTicketId} />
        <main className="main-content">
          {renderContent()}
        </main>
      </div>
    </div>
  );
}
