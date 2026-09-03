import React, { useEffect, useState } from 'react';
import { api } from '../services/api';
import Timeline from '../components/Timeline';
import ProofTraceViewer from '../components/ProofTraceViewer';

export default function TicketDetailsPage({ ticketId, setCurrentPage }) {
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (ticketId) {
      loadTicketDetails();
    }
  }, [ticketId]);

  const loadTicketDetails = async () => {
    try {
      const data = await api.getTicketDetails(ticketId);
      setTicket(data);
    } catch (err) {
      setError(err.message || 'Failed to load ticket');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={{ color: '#94a3b8' }}>Loading ticket details...</div>;
  if (error || !ticket) return <div style={{ color: '#ef4444' }}>Error: {error || 'Ticket not found'}</div>;

  return (
    <div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' }}>
        <button className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }} onClick={() => setCurrentPage('tickets')}>
          ← Back to Tickets
        </button>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Ticket Details: {ticket.ticket_number}</h2>
        <span className={`badge ${ticket.status === 'Resolved' ? 'badge-low' : ticket.status === 'Escalated' ? 'badge-critical' : 'badge-medium'}`}>
          {ticket.status}
        </span>
      </div>

      <div className="card">
        <h4 style={{ color: '#94a3b8', marginBottom: '0.5rem' }}>Ticket Lifecycle Progress</h4>
        <Timeline status={ticket.status} />
      </div>

      <div className="grid-cols-2">
        <div className="card">
          <h3 className="card-title">📌 Ticket Overview</h3>
          <div style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
            <div><strong>Department:</strong> {ticket.department}</div>
            <div><strong>Location:</strong> {ticket.location}</div>
            <div><strong>Description:</strong> {ticket.description}</div>
            <div><strong>Created At:</strong> {new Date(ticket.created_at).toLocaleString()}</div>
            {ticket.resolution_notes && (
              <div style={{ marginTop: '0.5rem', padding: '0.75rem', backgroundColor: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '8px', color: '#34d399' }}>
                <strong>Staff Resolution Notes:</strong> {ticket.resolution_notes}
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <h3 className="card-title">🤖 AI Predictions & Model Outputs</h3>
          <div style={{ fontSize: '0.9rem', lineHeight: '1.8' }}>
            <div>
              <strong>Diagnosed Cause:</strong> <span style={{ color: '#a7f3d0' }}>{ticket.diagnosed_cause || 'General Fault'}</span>
            </div>
            <div>
              <strong>Confidence:</strong> {Math.round((ticket.diagnosis_confidence || 0.85) * 100)}%
            </div>
            <div>
              <strong>Decision Tree Category & Priority:</strong> {ticket.category || 'AC_POWER'} ({ticket.priority || 'MEDIUM'})
            </div>
            <div>
              <strong>Escalation Risk Probability:</strong> {(ticket.escalation_probability * 100).toFixed(1)}% &nbsp;
              <span className={`badge ${ticket.escalated ? 'badge-critical' : 'badge-low'}`}>
                {ticket.escalated ? 'HIGH RISK' : 'LOW RISK'}
              </span>
            </div>
            <div>
              <strong>Q-Learning Staff Routing:</strong> Staff #{ticket.assigned_staff_id || 'Auto'} assigned
            </div>
          </div>
        </div>
      </div>

      {/* AI Explanation & Proof Trace Section */}
      <ProofTraceViewer
        explanation={ticket.ai_explanation || {}}
        diagnosis={ticket.diagnosed_cause}
        confidence={ticket.diagnosis_confidence}
      />
    </div>
  );
}
