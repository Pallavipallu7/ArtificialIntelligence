import React, { useEffect, useState } from 'react';
import { api, getUser } from '../services/api';

export default function StaffDashboard({ setSelectedTicketId, setCurrentPage }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [resolveNotes, setResolveNotes] = useState('');
  const [resolvingId, setResolvingId] = useState(null);

  // Feedback modal state
  const [feedbackTicketId, setFeedbackTicketId] = useState(null);
  const [feedbackRating, setFeedbackRating] = useState('Accurate');
  const [feedbackNotes, setFeedbackNotes] = useState('');

  const user = getUser();

  useEffect(() => {
    loadAssignedTickets();
  }, []);

  const loadAssignedTickets = async () => {
    try {
      const data = await api.getTickets();
      setTickets(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleStartWork = async (ticketId) => {
    try {
      await api.updateTicketStatus(ticketId, { status: 'Diagnosed' });
      loadAssignedTickets();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleResolve = async (ticketId) => {
    if (!resolveNotes.trim()) {
      alert('Please enter resolution notes before resolving.');
      return;
    }
    try {
      await api.resolveTicket(ticketId, resolveNotes);
      setResolvingId(null);
      setResolveNotes('');
      loadAssignedTickets();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleEscalate = async (ticketId) => {
    try {
      await api.escalateTicket(ticketId);
      loadAssignedTickets();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleSubmitFeedback = (e) => {
    e.preventDefault();
    alert(`Feedback submitted for ticket #${feedbackTicketId}: ${feedbackRating} - ${feedbackNotes}`);
    setFeedbackTicketId(null);
    setFeedbackNotes('');
  };

  const assignedCount = tickets.length;
  const highRiskCount = tickets.filter(t => t.escalated || t.priority === 'CRITICAL' || t.priority === 'HIGH').length;

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Maintenance Staff Dashboard</h2>
        <p style={{ color: '#94a3b8' }}>Welcome {user?.name || 'Staff'}. Manage assigned tickets, view AI diagnosis traces, update resolution, provide AI accuracy feedback, or escalate issues.</p>
      </div>

      <div className="grid-cols-3" style={{ marginBottom: '1.5rem' }}>
        <div className="metric-card">
          <div className="metric-label">Assigned Workload</div>
          <div className="metric-value">{assignedCount} active</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <div className="metric-label">High Priority / Risk</div>
          <div className="metric-value" style={{ color: '#f87171' }}>{highRiskCount}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #10b981' }}>
          <div className="metric-label">Avg Resolution Target</div>
          <div className="metric-value" style={{ color: '#34d399' }}>&lt; 4.0 hrs</div>
        </div>
      </div>

      <div className="card">
        <h3 className="card-title">Assigned Tickets Queue</h3>

        {loading ? (
          <p style={{ color: '#94a3b8' }}>Loading assigned tickets...</p>
        ) : tickets.length === 0 ? (
          <p style={{ color: '#94a3b8' }}>No assigned tickets at the moment.</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Ticket ID</th>
                  <th>Location</th>
                  <th>Description</th>
                  <th>AI Cause Diagnosis</th>
                  <th>Priority / Risk</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {tickets.map(t => (
                  <tr key={t.id}>
                    <td style={{ fontWeight: 600, color: '#60a5fa' }}>{t.ticket_number}</td>
                    <td>{t.location}</td>
                    <td style={{ maxWidth: '180px' }}>{t.description}</td>
                    <td style={{ color: '#a7f3d0' }}>{t.diagnosed_cause || 'N/A'}</td>
                    <td>
                      <span className={`badge ${t.priority === 'CRITICAL' || t.escalated ? 'badge-critical' : t.priority === 'HIGH' ? 'badge-high' : 'badge-medium'}`}>
                        {t.priority || 'MEDIUM'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${t.status === 'Resolved' ? 'badge-low' : 'badge-medium'}`}>
                        {t.status}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                          onClick={() => {
                            setSelectedTicketId(t.id);
                            setCurrentPage('ticket_details');
                          }}
                        >
                          Proof
                        </button>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', backgroundColor: '#3b82f6', color: 'white' }}
                          onClick={() => setFeedbackTicketId(t.id)}
                        >
                          Feedback
                        </button>

                        {t.status !== 'Resolved' && (
                          <>
                            <button
                              className="btn btn-primary"
                              style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                              onClick={() => handleStartWork(t.id)}
                            >
                              Start
                            </button>
                            <button
                              className="btn btn-primary"
                              style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem', backgroundColor: '#10b981' }}
                              onClick={() => setResolvingId(t.id)}
                            >
                              Resolve
                            </button>
                            <button
                              className="btn btn-danger"
                              style={{ padding: '0.25rem 0.5rem', fontSize: '0.75rem' }}
                              onClick={() => handleEscalate(t.id)}
                            >
                              Escalate
                            </button>
                          </>
                        )}
                      </div>

                      {resolvingId === t.id && (
                        <div style={{ marginTop: '0.75rem', padding: '0.75rem', backgroundColor: '#0f172a', borderRadius: '8px', border: '1px solid #334155' }}>
                          <textarea
                            rows="2"
                            placeholder="Enter resolution details..."
                            value={resolveNotes}
                            onChange={(e) => setResolveNotes(e.target.value)}
                            style={{ marginBottom: '0.5rem' }}
                          />
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button className="btn btn-primary" style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }} onClick={() => handleResolve(t.id)}>
                              Confirm Resolution
                            </button>
                            <button className="btn btn-secondary" style={{ padding: '0.25rem 0.6rem', fontSize: '0.75rem' }} onClick={() => setResolvingId(null)}>
                              Cancel
                            </button>
                          </div>
                        </div>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Staff AI Feedback Modal */}
      {feedbackTicketId && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
          <div className="card" style={{ width: '100%', maxWidth: '460px', backgroundColor: '#1e293b' }}>
            <h3 className="card-title">📝 Provide AI Diagnosis Feedback</h3>

            <form onSubmit={handleSubmitFeedback}>
              <div className="form-group">
                <label>AI Diagnosis Accuracy Assessment</label>
                <select value={feedbackRating} onChange={(e) => setFeedbackRating(e.target.value)}>
                  <option value="Accurate">Accurate - Correct Cause Derived</option>
                  <option value="Partially Accurate">Partially Accurate - Symptom Matched</option>
                  <option value="Inaccurate">Inaccurate - Incorrect Diagnosis</option>
                </select>
              </div>

              <div className="form-group">
                <label>Staff Feedback / Ground Truth Notes</label>
                <textarea
                  rows="3"
                  placeholder="Enter notes on actual physical cause found during repair..."
                  value={feedbackNotes}
                  onChange={(e) => setFeedbackNotes(e.target.value)}
                  required
                />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.25rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setFeedbackTicketId(null)}>Cancel</button>
                <button type="submit" className="btn btn-primary">Submit Feedback</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
