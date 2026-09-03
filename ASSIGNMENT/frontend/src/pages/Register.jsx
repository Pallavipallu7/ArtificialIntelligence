import React, { useState } from 'react';
import { api, setAuthToken, setUser } from '../services/api';

export default function Register({ onLoginSuccess, switchToLogin }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [department, setDepartment] = useState('CSE');
  const [role, setRole] = useState('USER');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      // 1. Register user
      const userRes = await api.register({
        name,
        email,
        password,
        department,
        role
      });

      // 2. Automatically log in after registration
      const loginRes = await api.login({ email, password });
      setAuthToken(loginRes.access_token);
      setUser(loginRes.user);
      onLoginSuccess(loginRes.user);
    } catch (err) {
      setError(err.message || 'Registration failed.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0f172a', padding: '1rem' }}>
      <div className="card" style={{ width: '100%', maxWidth: '480px', padding: '2.5rem' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
          <div className="brand-icon" style={{ width: '48px', height: '48px', margin: '0 auto 1rem auto', fontSize: '1.2rem' }}>AI</div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Create Campus Account</h2>
          <p style={{ color: '#94a3b8', fontSize: '0.875rem' }}>Register as Student, Staff, or System Administrator</p>
        </div>

        {error && (
          <div style={{ backgroundColor: 'rgba(239, 68, 68, 0.15)', border: '1px solid #ef4444', color: '#fca5a5', padding: '0.75rem', borderRadius: '8px', marginBottom: '1.25rem', fontSize: '0.85rem' }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Full Name</label>
            <input type="text" placeholder="e.g. Vikram Sharma" value={name} onChange={(e) => setName(e.target.value)} required />
          </div>

          <div className="form-group">
            <label>Campus Email Address</label>
            <input type="email" placeholder="e.g. vikram@campus.edu" value={email} onChange={(e) => setEmail(e.target.value)} required />
          </div>

          <div className="form-group">
            <label>Password</label>
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          </div>

          <div className="grid-cols-2">
            <div className="form-group">
              <label>Department</label>
              <select value={department} onChange={(e) => setDepartment(e.target.value)}>
                <option value="CSE">CSE</option>
                <option value="ECE">ECE</option>
                <option value="EEE">EEE</option>
                <option value="Mechanical">Mechanical</option>
                <option value="Biotechnology">Biotechnology</option>
                <option value="IT">IT Administration</option>
              </select>
            </div>

            <div className="form-group">
              <label>Account Role</label>
              <select value={role} onChange={(e) => setRole(e.target.value)}>
                <option value="USER">Student / Staff User</option>
                <option value="STAFF">Maintenance Staff</option>
                <option value="ADMIN">System Administrator</option>
              </select>
            </div>
          </div>

          <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '0.5rem' }} disabled={loading}>
            {loading ? 'Creating Account...' : 'Register Account'}
          </button>
        </form>

        <div style={{ marginTop: '1.5rem', textAlign: 'center' }}>
          <button
            onClick={switchToLogin}
            style={{ background: 'none', border: 'none', color: '#60a5fa', fontSize: '0.875rem', cursor: 'pointer', textDecoration: 'underline' }}
          >
            Already have an account? Sign In
          </button>
        </div>
      </div>
    </div>
  );
}
