import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function MyTicketsPage({ setCurrentPage, setSelectedTicketId }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      const data = await api.getTickets();
      setTickets(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>My Campus Helpdesk Tickets</h2>
          <p style={{ color: '#94a3b8' }}>View ticket lifecycle status, AI diagnosis proof traces, and resolution updates.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setCurrentPage('report')}>
          + New Ticket
        </button>
      </div>

      <div className="card">
        {loading ? (
          <p style={{ color: '#94a3b8' }}>Loading ticket history...</p>
        ) : tickets.length === 0 ? (
          <p style={{ color: '#94a3b8' }}>No tickets found. Submit a new fault report or use the AI Assistant!</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Department</th>
                  <th>Location</th>
                  <th>Diagnosed Cause</th>
                  <th>Assigned Staff</th>
                  <th>Status</th>
                  <th>Created</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map(t => (
                  <tr key={t.id}>
                    <td style={{ fontWeight: 600, color: '#60a5fa' }}>{t.ticket_number}</td>
                    <td>{t.department}</td>
                    <td>{t.location}</td>
                    <td style={{ color: '#a7f3d0' }}>{t.diagnosed_cause || 'N/A'}</td>
                    <td>Staff #{t.assigned_staff_id || 'Auto-Routing'}</td>
                    <td>
                      <span className={`badge ${t.status === 'Resolved' ? 'badge-low' : t.status === 'Escalated' ? 'badge-critical' : 'badge-medium'}`}>
                        {t.status}
                      </span>
                    </td>
                    <td style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
                      {new Date(t.created_at).toLocaleDateString()}
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '0.3rem 0.6rem', fontSize: '0.75rem' }}
                        onClick={() => {
                          setSelectedTicketId(t.id);
                          setCurrentPage('ticket_details');
                        }}
                      >
                        Inspect Proof
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
