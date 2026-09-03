import React, { useState } from 'react';
import { api, setAuthToken, setUser } from '../services/api';

export default function Login({ onLoginSuccess, switchToRegister }) {
  const [email, setEmail] = useState('student@campus.edu');
  const [password, setPassword] = useState('student123');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await api.login({ email, password });
      setAuthToken(res.access_token);
      setUser(res.user);
      onLoginSuccess(res.user);
    } catch (err) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  const selectAccount = (eMail, pass) => {
    setEmail(eMail);
    setPassword(pass);
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0f172a', padding: '1rem' }}>
      <div className="card" style={{ width: '100%', maxWidth: '440px', padding: '2.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <div className="brand-icon" style={{ width: '52px', height: '52px', margin: '0 auto 1rem auto', fontSize: '1.3rem' }}>AI</div>
          <h2 style={{ fontSize: '1.6rem', fontWeight: 700 }}>Campus Helpdesk</h2>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Intelligent Facility Fault-Diagnosis & Routing Assistant</p>
        </div>

        {error && (
          <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '0.75rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email Address</label>
            <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '0.5rem' }} disabled={loading}>
            {loading ? 'Authenticating...' : 'Sign In'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', paddingTop: '1.25rem', borderTop: '1px solid #334155' }}>
          <label style={{ fontSize: '0.75rem', color: '#94a3b8', marginBottom: '0.5rem', display: 'block', fontWeight: 600 }}>
            QUICK ROLE SELECTION:
          </label>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            <button className="btn btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', flex: 1 }} onClick={() => selectAccount('student@campus.edu', 'student123')}>
              🎓 Student
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', flex: 1 }} onClick={() => selectAccount('staff1@campus.edu', 'staff123')}>
              🔧 Staff (Arun)
            </button>
            <button className="btn btn-secondary" style={{ padding: '0.35rem 0.65rem', fontSize: '0.75rem', flex: 1 }} onClick={() => selectAccount('admin@campus.edu', 'admin123')}>
              🛡️ Admin
            </button>
          </div>
        </div>

        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <button
            onClick={switchToRegister}
            style={{ background: 'none', border: 'none', color: '#60a5fa', fontSize: '0.875rem', cursor: 'pointer', textDecoration: 'underline' }}
          >
            Need a new account? Register Here
          </button>
        </div>
      </div>
    </div>
  );
}
