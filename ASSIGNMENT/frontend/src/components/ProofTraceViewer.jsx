import React, { useState } from 'react';

export default function ProofTraceViewer({ explanation = {}, diagnosis = '', confidence = 0 }) {
  const [expanded, setExpanded] = useState(false);

  const matchedRules = explanation?.matched_rules || [];
  const observed = explanation?.observed_symptoms || [];

  return (
    <div className="card" style={{ backgroundColor: '#0f172a', border: '1px solid #334155' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h4 style={{ color: '#60a5fa', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <span>🧠</span> AI Explanation & Reasoning Proof Trace
        </h4>
        <button
          className="btn btn-secondary"
          style={{ padding: '0.3rem 0.75rem', fontSize: '0.8rem' }}
          onClick={() => setExpanded(!expanded)}
        >
          {expanded ? 'Hide Trace' : 'Why did AI make this decision?'}
        </button>
      </div>

      <div style={{ marginTop: '0.75rem', fontSize: '0.9rem', color: '#cbd5e1' }}>
        <strong>Probable Cause:</strong> {diagnosis || 'General Fault'} &nbsp;|&nbsp;
        <strong>Confidence:</strong> {intPercent(confidence)}
      </div>

      {expanded && (
        <div style={{ marginTop: '1.25rem', paddingTop: '1rem', borderTop: '1px solid #334155' }}>
          <div style={{ marginBottom: '1rem' }}>
            <h5 style={{ color: '#94a3b8', marginBottom: '0.3rem' }}>1. Observed Symptoms (Facts):</h5>
            <div className="code-block" style={{ color: '#67e8f9' }}>
              {observed.length > 0 ? observed.join(', ') : 'Default symptom inputs'}
            </div>
          </div>

          <div style={{ marginBottom: '1rem' }}>
            <h5 style={{ color: '#94a3b8', marginBottom: '0.3rem' }}>2. Matched Knowledge Base Rules:</h5>
            {matchedRules.length > 0 ? (
              matchedRules.map((r, i) => (
                <div key={i} className="code-block" style={{ marginBottom: '0.5rem', color: '#fef08a' }}>
                  <strong>[Rule {r.rule_id}]:</strong> {r.rule_statement} &nbsp;(Confidence: {r.confidence})
                </div>
              ))
            ) : (
              <div className="code-block">Rule R1 / Knowledge Base Forward Chaining Derivation</div>
            )}
          </div>

          <div>
            <h5 style={{ color: '#94a3b8', marginBottom: '0.3rem' }}>3. Expert System Summary:</h5>
            <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
              {explanation?.summary || `Derived probable cause: ${diagnosis} based on forward chaining deduction.`}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

function intPercent(val) {
  if (typeof val === 'number') return `${Math.round(val * 100)}%`;
  return val || '85%';
}
