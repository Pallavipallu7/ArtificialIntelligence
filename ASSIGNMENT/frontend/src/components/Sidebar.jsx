import React from 'react';
import { getUser, removeAuthToken } from '../services/api';

export default function Sidebar({ currentPage, setCurrentPage }) {
  const user = getUser();

  const handleLogout = () => {
    removeAuthToken();
    localStorage.removeItem('user');
    window.location.reload();
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊', roles: ['USER', 'STAFF', 'ADMIN'] },
    { id: 'chat', label: 'AI Helpdesk Chat', icon: '💬', roles: ['USER', 'STAFF', 'ADMIN'] },
    { id: 'report', label: 'Report a Fault', icon: '⚠️', roles: ['USER', 'ADMIN'] },
    { id: 'tickets', label: 'My Tickets', icon: '📋', roles: ['USER'] },
    { id: 'staff_dashboard', label: 'Assigned Tickets', icon: '🔧', roles: ['STAFF', 'ADMIN'] },
    { id: 'admin_dashboard', label: 'Admin Dashboard', icon: '🛡️', roles: ['ADMIN'] },
    { id: 'knowledge_base', label: 'Knowledge Base', icon: '🧠', roles: ['ADMIN'] },
    { id: 'ai_transparency', label: 'AI Transparency', icon: '🔍', roles: ['ADMIN', 'STAFF'] },
    { id: 'analytics', label: 'PySpark Analytics', icon: '📈', roles: ['ADMIN', 'STAFF', 'USER'] },
  ];

  const userRole = (user?.role || 'USER').toUpperCase();
  const visibleItems = navItems.filter(item => item.roles.includes(userRole));

  return (
    <div className="sidebar">
      <div className="brand">
        <div className="brand-icon">AI</div>
        <div>
          <div className="brand-title">Campus Helpdesk</div>
          <div className="brand-subtitle">Fault Diagnosis AI</div>
        </div>
      </div>

      <ul className="nav-links">
        {visibleItems.map(item => (
          <li key={item.id}>
            <button
              className={`nav-link ${currentPage === item.id ? 'active' : ''}`}
              onClick={() => setCurrentPage(item.id)}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          </li>
        ))}
      </ul>

      <div className="user-profile-bar">
        <div>
          <div style={{ fontWeight: 600, fontSize: '0.9rem', color: 'white' }}>{user?.name || 'Guest User'}</div>
          <span className="badge badge-medium" style={{ fontSize: '0.65rem' }}>{userRole}</span>
        </div>
        <button onClick={handleLogout} className="btn btn-secondary" style={{ padding: '0.4rem 0.6rem', fontSize: '0.8rem' }}>
          Exit
        </button>
      </div>
    </div>
  );
}
