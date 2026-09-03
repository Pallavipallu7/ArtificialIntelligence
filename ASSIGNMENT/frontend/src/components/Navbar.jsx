import React, { useState, useEffect } from 'react';
import { api, getUser, removeAuthToken } from '../services/api';

export default function Navbar({ currentPage, setCurrentPage, setSelectedTicketId }) {
  const user = getUser();
  const [notifications, setNotifications] = useState([]);
  const [showNotifs, setShowNotifs] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (user) {
      fetchNotifications();
      const interval = setInterval(fetchNotifications, 10000); // Poll notifications every 10s
      return () => clearInterval(interval);
    }
  }, []);

  const fetchNotifications = async () => {
    try {
      const data = await api.getNotifications();
      setNotifications(data || []);
    } catch (e) {
      console.error(e);
    }
  };

  const unreadCount = notifications.filter(n => !n.is_read).length;

  const handleSearch = (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    // Direct lookup attempt
    const searchId = searchQuery.trim().toUpperCase();
    if (searchId.startsWith('TKT-')) {
      // Find matching ticket or navigate
      setCurrentPage('tickets');
    }
    setSearchQuery('');
  };

  const handleLogout = () => {
    removeAuthToken();
    localStorage.removeItem('user');
    window.location.reload();
  };

  return (
    <header style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '1rem 2rem',
      backgroundColor: '#0b1329',
      borderBottom: '1px solid #334155',
      position: 'sticky',
      top: 0,
      zIndex: 50
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        <h3 style={{ fontSize: '1.1rem', fontWeight: 600, color: 'white', textTransform: 'capitalize' }}>
          {currentPage.replace('_', ' ')}
        </h3>
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
        {/* Search Bar */}
        <form onSubmit={handleSearch} style={{ display: 'flex', alignItems: 'center' }}>
          <input
            type="text"
            placeholder="Search Ticket (e.g. TKT-1001)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              padding: '0.45rem 0.9rem',
              fontSize: '0.85rem',
              width: '240px',
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '20px'
            }}
          />
        </form>

        {/* Notification Bell */}
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowNotifs(!showNotifs)}
            style={{
              background: 'transparent',
              border: 'none',
              fontSize: '1.25rem',
              cursor: 'pointer',
              position: 'relative',
              padding: '0.4rem',
              color: '#94a3b8'
            }}
          >
            🔔
            {unreadCount > 0 && (
              <span style={{
                position: 'absolute',
                top: '2px',
                right: '2px',
                backgroundColor: '#ef4444',
                color: 'white',
                fontSize: '0.65rem',
                fontWeight: 700,
                borderRadius: '9999px',
                padding: '2px 5px'
              }}>
                {unreadCount}
              </span>
            )}
          </button>

          {/* Notifications Dropdown */}
          {showNotifs && (
            <div style={{
              position: 'absolute',
              right: 0,
              top: '40px',
              width: '320px',
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '12px',
              boxShadow: '0 10px 25px rgba(0,0,0,0.5)',
              padding: '1rem',
              zIndex: 100
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.75rem', borderBottom: '1px solid #334155', paddingBottom: '0.5rem' }}>
                <strong style={{ fontSize: '0.9rem' }}>Notifications ({unreadCount} unread)</strong>
                <button style={{ background: 'none', border: 'none', color: '#60a5fa', fontSize: '0.75rem', cursor: 'pointer' }} onClick={() => setShowNotifs(false)}>Close</button>
              </div>

              <div style={{ maxHeight: '250px', overflowY: 'auto' }}>
                {notifications.length === 0 ? (
                  <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>No new notifications.</p>
                ) : (
                  notifications.map(n => (
                    <div key={n.id} style={{ padding: '0.5rem 0', borderBottom: '1px solid #334155', fontSize: '0.8rem', color: '#cbd5e1' }}>
                      <div style={{ fontWeight: 600, color: '#60a5fa' }}>{n.notification_type || 'Update'}</div>
                      <div>{n.message}</div>
                      <div style={{ fontSize: '0.7rem', color: '#94a3b8', marginTop: '2px' }}>
                        {new Date(n.created_at).toLocaleTimeString()}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>

        {/* User Info Tag */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <div style={{ textAlign: 'right' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 600, color: 'white' }}>{user?.name}</div>
            <div style={{ fontSize: '0.7rem', color: '#94a3b8' }}>{user?.department} • {user?.role}</div>
          </div>
          <button
            onClick={handleLogout}
            className="btn btn-secondary"
            style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem' }}
          >
            Sign Out
          </button>
        </div>
      </div>
    </header>
  );
}
