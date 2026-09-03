import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function AdminDashboard({ setCurrentPage, setSelectedTicketId }) {
  const [tickets, setTickets] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [auditLogs, setAuditLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  // Override Modal state
  const [overrideModalOpen, setOverrideModalOpen] = useState(false);
  const [overrideTicketId, setOverrideTicketId] = useState('');
  const [overrideField, setOverrideField] = useState('assigned_staff_id');
  const [overrideValue, setOverrideValue] = useState('1');
  const [overrideReason, setOverrideReason] = useState('Admin override due to urgent staff availability');

  useEffect(() => {
    loadAdminData();
  }, []);

  const loadAdminData = async () => {
    try {
      const [tktData, analyticsData, logsData] = await Promise.all([
        api.getTickets(),
        api.getAnalyticsSummary(),
        api.getAuditLogs()
      ]);
      setTickets(tktData);
      setAnalytics(analyticsData);
      setAuditLogs(logsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOverrideSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.overrideTicket(overrideTicketId, {
        field_to_override: overrideField,
        new_value: overrideValue,
        reason: overrideReason
      });
      alert('AI decision successfully overridden!');
      setOverrideModalOpen(false);
      loadAdminData();
    } catch (err) {
      alert(err.message || 'Override failed');
    }
  };

  const total = tickets.length;
  const escalated = tickets.filter(t => t.escalated || t.status === 'Escalated').length;
  const resolved = tickets.filter(t => t.status === 'Resolved').length;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>System Administration & AI Control Center</h2>
          <p style={{ color: '#94a3b8' }}>Monitor AI model metrics, override decisions, manage Knowledge Base rules, and view PySpark analytics.</p>
        </div>
        <div style={{ display: 'flex', gap: '0.75rem' }}>
          <button className="btn btn-primary" onClick={() => setOverrideModalOpen(true)}>
            ⚡ AI Decision Override
          </button>
          <button className="btn btn-secondary" onClick={() => setCurrentPage('knowledge_base')}>
            🧠 Manage Rules
          </button>
        </div>
      </div>

      <div className="grid-cols-4">
        <div className="metric-card">
          <div className="metric-label">Total System Tickets</div>
          <div className="metric-value">{total}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #10b981' }}>
          <div className="metric-label">Resolution Rate</div>
          <div className="metric-value" style={{ color: '#34d399' }}>
            {total > 0 ? Math.round((resolved / total) * 100) : 100}%
          </div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <div className="metric-label">Escalated Risk Rate</div>
          <div className="metric-value" style={{ color: '#f87171' }}>
            {total > 0 ? Math.round((escalated / total) * 100) : 0}%
          </div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #8b5cf6' }}>
          <div className="metric-label">PySpark Status</div>
          <div className="metric-value" style={{ color: '#c084fc', fontSize: '1.25rem' }}>Active Engine</div>
        </div>
      </div>

      {/* Override Log & Tickets */}
      <div className="grid-cols-2" style={{ marginTop: '1.5rem' }}>
        <div className="card">
          <h3 className="card-title">All System Tickets & AI Assignments</h3>
          {loading ? (
            <p style={{ color: '#94a3b8' }}>Loading...</p>
          ) : (
            <div className="table-container" style={{ maxHeight: '350px' }}>
              <table>
                <thead>
                  <tr>
                    <th>Ticket ID</th>
                    <th>Category</th>
                    <th>Diagnosis</th>
                    <th>Assigned Staff</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {tickets.slice(0, 8).map(t => (
                    <tr key={t.id}>
                      <td style={{ fontWeight: 600, color: '#60a5fa' }}>{t.ticket_number}</td>
                      <td>{t.category || 'AC_POWER'}</td>
                      <td style={{ color: '#a7f3d0' }}>{t.diagnosed_cause}</td>
                      <td>Staff #{t.assigned_staff_id}</td>
                      <td>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                          onClick={() => {
                            setOverrideTicketId(t.id);
                            setOverrideModalOpen(true);
                          }}
                        >
                          Override
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>

        <div className="card">
          <h3 className="card-title">Audit Logs (AI Overrides History)</h3>
          {auditLogs.length === 0 ? (
            <p style={{ color: '#94a3b8' }}>No manual AI overrides logged yet.</p>
          ) : (
            <div className="table-container" style={{ maxHeight: '350px' }}>
              <table>
                <thead>
                  <tr>
                    <th>Ticket ID</th>
                    <th>Old Value</th>
                    <th>New Value</th>
                    <th>Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {auditLogs.map(l => (
                    <tr key={l.id}>
                      <td>#{l.ticket_id}</td>
                      <td style={{ color: '#f87171' }}>{l.old_value}</td>
                      <td style={{ color: '#34d399' }}>{l.new_value}</td>
                      <td style={{ fontSize: '0.8rem' }}>{l.reason}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {/* AI Decision Override Modal */}
      {overrideModalOpen && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
          <div className="card" style={{ width: '100%', maxWidth: '500px', backgroundColor: '#1e293b' }}>
            <h3 className="card-title">⚡ AI Decision Manual Override</h3>

            <form onSubmit={handleOverrideSubmit}>
              <div className="form-group">
                <label>Select Ticket</label>
                <select value={overrideTicketId} onChange={(e) => setOverrideTicketId(e.target.value)} required>
                  <option value="">-- Choose Ticket --</option>
                  {tickets.map(t => (
                    <option key={t.id} value={t.id}>{t.ticket_number} - {t.diagnosed_cause}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label>Field to Override</label>
                <select value={overrideField} onChange={(e) => setOverrideField(e.target.value)}>
                  <option value="assigned_staff_id">Assigned Maintenance Staff</option>
                  <option value="priority">Ticket Priority</option>
                  <option value="category">Fault Category</option>
                  <option value="status">Ticket Status</option>
                </select>
              </div>

              <div className="form-group">
                <label>New Override Value</label>
                <input type="text" value={overrideValue} onChange={(e) => setOverrideValue(e.target.value)} required />
              </div>

              <div className="form-group">
                <label>Reason for Override</label>
                <textarea rows="2" value={overrideReason} onChange={(e) => setOverrideReason(e.target.value)} required />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setOverrideModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Apply Admin Override</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
