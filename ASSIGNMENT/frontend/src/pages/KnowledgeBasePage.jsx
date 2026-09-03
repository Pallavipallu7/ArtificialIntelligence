import React, { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function KnowledgeBasePage() {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);

  // Add rule modal state
  const [modalOpen, setModalOpen] = useState(false);
  const [editingRule, setEditingRule] = useState(null);

  const [ruleId, setRuleId] = useState('R13');
  const [category, setCategory] = useState('AC_POWER');
  const [antecedentsText, setAntecedentsText] = useState('{"power_indicator": "off", "remote_no_response": true}');
  const [consequent, setConsequent] = useState('Main Circuit Breaker Tripped');
  const [priority, setPriority] = useState(8);

  // Tester state
  const [testSymptoms, setTestSymptoms] = useState('{"power_indicator": "off", "remote_no_response": true}');
  const [testResult, setTestResult] = useState(null);

  useEffect(() => {
    loadRules();
  }, []);

  const loadRules = async () => {
    try {
      const data = await api.getRules();
      setRules(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleOpenAdd = () => {
    setEditingRule(null);
    setRuleId(`R${rules.length + 1}`);
    setCategory('AC_POWER');
    setAntecedentsText('{"power_indicator": "off", "remote_no_response": true}');
    setConsequent('Main Circuit Breaker Tripped');
    setPriority(8);
    setModalOpen(true);
  };

  const handleOpenEdit = (rule) => {
    setEditingRule(rule);
    setRuleId(rule.rule_id);
    setCategory(rule.category);
    setAntecedentsText(JSON.stringify(rule.antecedents));
    setConsequent(rule.consequent);
    setPriority(rule.priority || 1);
    setModalOpen(true);
  };

  const handleSaveRule = async (e) => {
    e.preventDefault();
    try {
      const parsedAnt = JSON.parse(antecedentsText);
      if (editingRule) {
        await api.updateRule(ruleId, {
          category,
          antecedents: parsedAnt,
          consequent,
          priority: parseInt(priority, 10)
        });
        alert(`Rule ${ruleId} updated successfully!`);
      } else {
        await api.addRule({
          rule_id: ruleId,
          category,
          antecedents: parsedAnt,
          consequent,
          priority: parseInt(priority, 10),
          active: true
        });
        alert(`Rule ${ruleId} created successfully!`);
      }
      setModalOpen(false);
      loadRules();
    } catch (err) {
      alert('Invalid JSON in antecedents or server error: ' + err.message);
    }
  };

  const handleToggleRuleActive = async (rule) => {
    try {
      await api.updateRule(rule.rule_id, { active: !rule.active });
      loadRules();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDeleteRule = async (rId) => {
    if (!window.confirm(`Delete rule ${rId}?`)) return;
    try {
      await api.deleteRule(rId);
      loadRules();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleTestKB = async () => {
    try {
      const parsedSyms = JSON.parse(testSymptoms);
      const res = await api.testRule(parsedSyms);
      setTestResult(res);
    } catch (err) {
      alert('Invalid JSON in symptoms test input: ' + err.message);
    }
  };

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 700 }}>Knowledge Base & Inference Rules Engine</h2>
          <p style={{ color: '#94a3b8' }}>Manage production rules (R1-R12+), edit antecedents, toggle rule activation, and run inference test suites.</p>
        </div>
        <button className="btn btn-primary" onClick={handleOpenAdd}>
          + Add New Production Rule
        </button>
      </div>

      {/* Interactive Rule Tester */}
      <div className="card" style={{ backgroundColor: '#0b1329', border: '1px solid #334155' }}>
        <h4 style={{ color: '#60a5fa', marginBottom: '0.75rem' }}>🧪 Test Knowledge Base Inference</h4>
        <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '0.75rem' }}>
          <input
            type="text"
            value={testSymptoms}
            onChange={(e) => setTestSymptoms(e.target.value)}
            placeholder='{"power_indicator": "off", "remote_no_response": true}'
          />
          <button className="btn btn-primary" onClick={handleTestKB}>
            Run Inference Engine
          </button>
        </div>

        {testResult && (
          <div className="code-block" style={{ marginTop: '0.75rem' }}>
            <div><strong>Derived Cause:</strong> {testResult.diagnosis_result?.diagnosis || 'No match found'}</div>
            <div><strong>Confidence:</strong> {Math.round((testResult.diagnosis_result?.confidence || 0) * 100)}%</div>
            <div><strong>Matched Rule:</strong> {testResult.diagnosis_result?.proof_trace[0]?.matched_rule || 'N/A'}</div>
            <div><strong>Contradictions Detected:</strong> {testResult.contradictions_detected?.length || 0}</div>
          </div>
        )}
      </div>

      {/* Rules Table */}
      <div className="card">
        <h3 className="card-title">Production Rules (R1 - R12+)</h3>

        {loading ? (
          <p style={{ color: '#94a3b8' }}>Loading rules...</p>
        ) : (
          <div className="table-container">
            <table>
              <thead>
                <tr>
                  <th>Rule ID</th>
                  <th>Category</th>
                  <th>IF Antecedents (Conditions)</th>
                  <th>THEN Consequent (Diagnosis)</th>
                  <th>Priority</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {rules.map(r => (
                  <tr key={r.id || r.rule_id}>
                    <td style={{ fontWeight: 700, color: '#60a5fa' }}>{r.rule_id}</td>
                    <td>{r.category}</td>
                    <td style={{ fontFamily: 'var(--font-mono)', fontSize: '0.85rem', color: '#fef08a' }}>
                      {JSON.stringify(r.antecedents)}
                    </td>
                    <td style={{ color: '#a7f3d0', fontWeight: 600 }}>{r.consequent}</td>
                    <td>{r.priority}</td>
                    <td>
                      <button
                        className={`badge ${r.active ? 'badge-low' : 'badge-high'}`}
                        style={{ border: 'none', cursor: 'pointer' }}
                        onClick={() => handleToggleRuleActive(r)}
                      >
                        {r.active ? 'ACTIVE' : 'INACTIVE'}
                      </button>
                    </td>
                    <td>
                      <div style={{ display: 'flex', gap: '0.4rem' }}>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                          onClick={() => handleOpenEdit(r)}
                        >
                          Edit
                        </button>
                        <button
                          className="btn btn-danger"
                          style={{ padding: '0.2rem 0.5rem', fontSize: '0.75rem' }}
                          onClick={() => handleDeleteRule(r.rule_id)}
                        >
                          Delete
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add / Edit Rule Modal */}
      {modalOpen && (
        <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(0,0,0,0.7)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 100 }}>
          <div className="card" style={{ width: '100%', maxWidth: '520px', backgroundColor: '#1e293b' }}>
            <h3 className="card-title">{editingRule ? `Edit Rule ${ruleId}` : '+ Add New Production Rule'}</h3>

            <form onSubmit={handleSaveRule}>
              <div className="grid-cols-2">
                <div className="form-group">
                  <label>Rule ID</label>
                  <input type="text" value={ruleId} onChange={(e) => setRuleId(e.target.value)} required disabled={!!editingRule} />
                </div>
                <div className="form-group">
                  <label>Category</label>
                  <input type="text" value={category} onChange={(e) => setCategory(e.target.value)} required />
                </div>
              </div>

              <div className="form-group">
                <label>IF Antecedents (JSON format)</label>
                <textarea rows="3" value={antecedentsText} onChange={(e) => setAntecedentsText(e.target.value)} required />
              </div>

              <div className="form-group">
                <label>THEN Consequent (Diagnosis Cause)</label>
                <input type="text" value={consequent} onChange={(e) => setConsequent(e.target.value)} required />
              </div>

              <div className="form-group">
                <label>Priority Level (1 - 10)</label>
                <input type="number" min="1" max="10" value={priority} onChange={(e) => setPriority(e.target.value)} required />
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', marginTop: '1.5rem' }}>
                <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>Cancel</button>
                <button type="submit" className="btn btn-primary">{editingRule ? 'Update Rule' : 'Save Rule'}</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
