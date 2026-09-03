import React, { useEffect, useState } from 'react';
import { api, getUser } from '../services/api';

export default function UserDashboard({ setCurrentPage, setSelectedTicketId }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const user = getUser();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await api.getTickets();
      setTickets(data);
    } catch (e) {
      console.error('Failed to load tickets', e);
    } finally {
      setLoading(false);
    }
  };

  const total = tickets.length;
  const open = tickets.filter(t => ['Reported', 'Diagnosed', 'Assigned'].includes(t.status)).length;
  const resolved = tickets.filter(t => t.status === 'Resolved').length;
  const escalated = tickets.filter(t => t.status === 'Escalated' || t.escalated).length;

  return (
    <div>
      <div style={{ marginBottom: '1.5rem', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', fontWeight: 700 }}>Welcome back, {user?.name || 'Student'}</h1>
          <p style={{ color: '#94a3b8' }}>Campus Intelligent Facility Helpdesk Portal ({user?.department || 'CSE'} Department)</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn btn-primary" onClick={() => setCurrentPage('chat')}>
            💬 Chat with AI Assistant
          </button>
          <button className="btn btn-secondary" onClick={() => setCurrentPage('report')}>
            ⚠️ Report a Fault
          </button>
        </div>
      </div>

      <div className="grid-cols-4">
        <div className="metric-card">
          <div className="metric-label">Total Tickets</div>
          <div className="metric-value">{total}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="metric-label">Active / Open</div>
          <div className="metric-value" style={{ color: '#60a5fa' }}>{open}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #10b981' }}>
          <div className="metric-label">Resolved</div>
          <div className="metric-value" style={{ color: '#34d399' }}>{resolved}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <div className="metric-label">Escalated Risk</div>
          <div className="metric-value" style={{ color: '#f87171' }}>{escalated}</div>
        </div>
      </div>

      <div className="card" style={{ marginTop: '1.5rem' }}>
        <h3 className="card-title">Recent Tickets & AI Diagnoses</h3>

        {loading ? (
          <p style={{ color: '#94a3b8' }}>Loading tickets...</p>
        ) : tickets.length === 0 ? (
          <p style={{ color: '#94a3b8' }}>No tickets submitted yet. Click "Report a Fault" to submit your first issue.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Ticket No</th>
                  <th>Location</th>
                  <th>Description</th>
                  <th>AI Cause Diagnosis</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tickets.slice(0, 6).map(t => (
                  <tr key={t.id}>
                    <td style={{ fontWeight: 600, color: '#60a5fa' }}>{t.ticket_number}</td>
                    <td>{t.location}</td>
                    <td style={{ maxWidth: '220px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {t.description}
                    </td>
                    <td style={{ color: '#a7f3d0' }}>{t.diagnosed_cause || 'Diagnosing...'}</td>
                    <td>
                      <span className={`badge ${t.status === 'Resolved' ? 'badge-low' : t.status === 'Escalated' ? 'badge-critical' : 'badge-medium'}`}>
                        {t.status}
                      </span>
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '0.35rem 0.75rem', fontSize: '0.8rem' }}
                        onClick={() => {
                          setSelectedTicketId(t.id);
                          setCurrentPage('ticket_details');
                        }}
                      >
                        View Proof
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
