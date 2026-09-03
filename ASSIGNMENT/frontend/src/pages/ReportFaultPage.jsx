import React, { useState } from 'react';
import { api, getUser } from '../services/api';

export default function ReportFaultPage({ setCurrentPage, setSelectedTicketId }) {
  const user = getUser();
  const [department, setDepartment] = useState(user?.department || 'CSE');
  const [location, setLocation] = useState(`${user?.department || 'CSE'} Lab 2`);
  const [description, setDescription] = useState('AC power indicator is OFF and remote does not respond.');
  const [symptoms, setSymptoms] = useState({ power_indicator: 'off', remote_no_response: true });
  const [aiPreview, setAiPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  const handleDiagnosePreview = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await api.diagnose(symptoms);
      setAiPreview(res);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    try {
      const created = await api.createTicket({
        department,
        location,
        description,
        symptoms
      });
      setSelectedTicketId(created.id);
      setCurrentPage('ticket_details');
    } catch (err) {
      setError(err.message || 'Failed to submit ticket');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h2 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>Report a Campus Facility Fault</h2>
      <p style={{ color: '#94a3b8', marginBottom: '1.5rem' }}>
        Submit a facility fault ticket. The Knowledge Reasoning engine and ML models will diagnose, classify, predict risk, and recommend staff routing automatically.
      </p>

      {error && (
        <div style={{ backgroundColor: 'rgba(239,68,68,0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '0.75rem', borderRadius: '8px', marginBottom: '1.25rem' }}>
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="card">
        <div className="grid-cols-2">
          <div className="form-group">
            <label>Department</label>
            <select value={department} onChange={(e) => setDepartment(e.target.value)}>
              <option value="CSE">CSE</option>
              <option value="ECE">ECE</option>
              <option value="EEE">EEE</option>
              <option value="Mechanical">Mechanical</option>
              <option value="Biotechnology">Biotechnology</option>
            </select>
          </div>

          <div className="form-group">
            <label>Location / Room</label>
            <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} required />
          </div>
        </div>

        <div className="form-group">
          <label>Problem Description</label>
          <textarea rows="3" value={description} onChange={(e) => setDescription(e.target.value)} required />
        </div>

        <div style={{ padding: '1rem', backgroundColor: '#0b1329', borderRadius: '8px', marginBottom: '1.25rem', border: '1px solid #334155' }}>
          <h4 style={{ color: '#60a5fa', marginBottom: '0.75rem' }}>Symptom Checklist (Knowledge Reasoning Inputs)</h4>
          <div className="grid-cols-2" style={{ fontSize: '0.85rem' }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input type="checkbox" checked={symptoms.power_indicator === 'off'} onChange={(e) => setSymptoms(s => ({ ...s, power_indicator: e.target.checked ? 'off' : 'on' }))} />
              Power Indicator OFF
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input type="checkbox" checked={!!symptoms.remote_no_response} onChange={(e) => setSymptoms(s => ({ ...s, remote_no_response: e.target.checked }))} />
              Remote No Response
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input type="checkbox" checked={!!symptoms.compressor_no_sound} onChange={(e) => setSymptoms(s => ({ ...s, compressor_no_sound: e.target.checked }))} />
              Compressor Silent (No Sound)
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', cursor: 'pointer' }}>
              <input type="checkbox" checked={!!symptoms.cooling_low} onChange={(e) => setSymptoms(s => ({ ...s, cooling_low: e.target.checked }))} />
              Cooling Low / Ineffective
            </label>
          </div>

          <div style={{ marginTop: '0.75rem' }}>
            <button type="button" className="btn btn-secondary" style={{ padding: '0.4rem 0.8rem', fontSize: '0.8rem' }} onClick={handleDiagnosePreview} disabled={loading}>
              {loading ? 'Evaluating KB Rules...' : '🧪 Preview AI Reasoning Diagnosis'}
            </button>
          </div>
        </div>

        {aiPreview && (
          <div style={{ backgroundColor: 'rgba(59,130,246,0.1)', border: '1px solid #3b82f6', borderRadius: '8px', padding: '1rem', marginBottom: '1.25rem' }}>
            <h5 style={{ color: '#60a5fa' }}>AI Forward-Chaining Preview Result:</h5>
            <div style={{ fontSize: '0.9rem', color: '#a7f3d0' }}>
              Diagnosed Cause: <strong>{aiPreview.diagnosis || 'General Fault'}</strong> (Confidence: {Math.round((aiPreview.confidence || 0.85) * 100)}%)
            </div>
          </div>
        )}

        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'flex-end' }}>
          <button type="button" className="btn btn-secondary" onClick={() => setCurrentPage('dashboard')}>
            Cancel
          </button>
          <button type="submit" className="btn btn-primary" disabled={submitting}>
            {submitting ? 'Creating Ticket & AI Pipeline...' : 'Submit & Execute AI Pipeline'}
          </button>
        </div>
      </form>
    </div>
  );
}
