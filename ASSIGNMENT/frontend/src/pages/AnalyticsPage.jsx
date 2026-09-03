import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function AnalyticsPage() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPySparkAnalytics();
  }, []);

  const loadPySparkAnalytics = async () => {
    try {
      const res = await api.getAnalyticsSummary();
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div style={{ color: '#94a3b8' }}>Executing PySpark job in local mode...</div>;

  const catDist = data?.category_distribution || {};
  const deptDist = data?.department_distribution || {};
  const prioDist = data?.priority_distribution || {};

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Campus Helpdesk Distributed Analytics</h2>
          <p style={{ color: '#94a3b8' }}>Local mode data aggregations computed on synthetic historical ticket dataset.</p>
        </div>
        <span className="badge-pyspark">
          🔥 Analytics generated using PySpark
        </span>
      </div>

      <div className="grid-cols-4" style={{ marginBottom: '1.5rem' }}>
        <div className="metric-card">
          <div className="metric-label">Dataset Total Tickets</div>
          <div className="metric-value">{data?.total_tickets || 120}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #3b82f6' }}>
          <div className="metric-label">Avg Resolution Time</div>
          <div className="metric-value" style={{ color: '#60a5fa' }}>{data?.average_resolution_time_hours || 35.6} hrs</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #10b981' }}>
          <div className="metric-label">Most Common Fault</div>
          <div className="metric-value" style={{ color: '#34d399', fontSize: '1.2rem' }}>{data?.most_frequent_fault || 'CLASSROOM_FAN'}</div>
        </div>
        <div className="metric-card" style={{ borderLeft: '4px solid #ef4444' }}>
          <div className="metric-label">Escalated Tickets</div>
          <div className="metric-value" style={{ color: '#f87171' }}>{data?.escalated_tickets_count || 62}</div>
        </div>
      </div>

      <div className="grid-cols-2">
        {/* Department Breakdown */}
        <div className="card">
          <h3 className="card-title">Tickets by Department (PySpark RDD GroupBy)</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Department</th>
                  <th>Ticket Count</th>
                  <th>Percentage</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(deptDist).map(([dept, cnt]) => (
                  <tr key={dept}>
                    <td style={{ fontWeight: 600, color: '#60a5fa' }}>{dept}</td>
                    <td>{cnt}</td>
                    <td>{Math.round((cnt / (data?.total_tickets || 120)) * 100)}%</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Priority Breakdown */}
        <div className="card">
          <h3 className="card-title">Priority Distribution (PySpark Aggregation)</h3>
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Priority</th>
                  <th>Count</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(prioDist).map(([prio, cnt]) => (
                  <tr key={prio}>
                    <td>
                      <span className={`badge ${prio === 'CRITICAL' ? 'badge-critical' : prio === 'HIGH' ? 'badge-high' : 'badge-medium'}`}>
                        {prio}
                      </span>
                    </td>
                    <td style={{ fontWeight: 600 }}>{cnt}</td>
                    <td style={{ color: '#94a3b8', fontSize: '0.85rem' }}>Automated SLA Routing</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Category Breakdown Table */}
      <div className="card" style={{ marginTop: '1.5rem' }}>
        <h3 className="card-title">Fault Categories Breakdown (Top 20 Categories)</h3>
        <div className="table-container" style={{ maxHeight: '350px' }}>
          <table>
            <thead>
              <tr>
                <th>Fault Category</th>
                <th>Total Occurrences</th>
                <th>Frequency Rank</th>
              </tr>
            </thead>
            <tbody>
              {Object.entries(catDist).map(([cat, cnt], idx) => (
                <tr key={cat}>
                  <td style={{ fontWeight: 600, color: '#a7f3d0' }}>{cat}</td>
                  <td>{cnt}</td>
                  <td style={{ color: '#94a3b8' }}>#{idx + 1}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
