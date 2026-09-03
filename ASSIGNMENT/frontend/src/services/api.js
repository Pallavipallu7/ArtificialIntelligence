const API_BASE = '/api';

export const getAuthToken = () => localStorage.getItem('token');
export const setAuthToken = (token) => localStorage.setItem('token', token);
export const removeAuthToken = () => localStorage.removeItem('token');

export const getUser = () => {
  const u = localStorage.getItem('user');
  return u ? JSON.parse(u) : null;
};
export const setUser = (user) => localStorage.setItem('user', JSON.stringify(user));

async function request(endpoint, options = {}) {
  const token = getAuthToken();
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    removeAuthToken();
    localStorage.removeItem('user');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'API Request failed');
  }
  return data;
}

export const api = {
  // Auth
  login: (credentials) => request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (userData) => request('/auth/register', { method: 'POST', body: JSON.stringify(userData) }),
  getMe: () => request('/users/me'),
  getUsers: () => request('/users'),

  // Tickets
  createTicket: (ticket) => request('/tickets', { method: 'POST', body: JSON.stringify(ticket) }),
  getTickets: () => request('/tickets'),
  getTicketDetails: (id) => request(`/tickets/${id}`),
  updateTicketStatus: (id, payload) => request(`/tickets/${id}`, { method: 'PUT', body: JSON.stringify(payload) }),
  resolveTicket: (id, notes) => request(`/tickets/${id}/resolve`, { method: 'POST', body: JSON.stringify({ resolution_notes: notes }) }),
  escalateTicket: (id) => request(`/tickets/${id}/escalate`, { method: 'POST' }),
  overrideTicket: (id, payload) => request(`/tickets/${id}/override`, { method: 'POST', body: JSON.stringify(payload) }),

  // Chatbot
  sendChatMessage: (payload) => request('/chat', { method: 'POST', body: JSON.stringify(payload) }),

  // AI & Reasoning
  diagnose: (symptoms) => request('/ai/diagnose', { method: 'POST', body: JSON.stringify({ symptoms }) }),
  classify: (payload) => request('/ai/classify', { method: 'POST', body: JSON.stringify(payload) }),
  escalationRisk: (payload) => request('/ai/escalation-risk', { method: 'POST', body: JSON.stringify(payload) }),
  recommendRouting: (payload) => request('/routing/recommend', { method: 'POST', body: JSON.stringify(payload) }),

  // Knowledge Base
  getRules: () => request('/knowledge-base/rules'),
  addRule: (rule) => request('/knowledge-base/rules', { method: 'POST', body: JSON.stringify(rule) }),
  updateRule: (id, rule) => request(`/knowledge-base/rules/${id}`, { method: 'PUT', body: JSON.stringify(rule) }),
  deleteRule: (id) => request(`/knowledge-base/rules/${id}`, { method: 'DELETE' }),
  testRule: (symptoms) => request('/knowledge-base/test', { method: 'POST', body: JSON.stringify(symptoms) }),

  // Analytics & Metrics
  getAnalyticsSummary: () => request('/analytics/summary'),
  getModelMetrics: () => request('/models/metrics'),
  getRLMetrics: () => request('/rl/metrics'),
  getNotifications: () => request('/notifications'),
  getAuditLogs: () => request('/audit-logs'),
};
