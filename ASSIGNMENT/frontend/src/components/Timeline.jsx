import React from 'react';

export default function Timeline({ status = 'Reported' }) {
  const steps = ['Reported', 'Diagnosed', 'Assigned', 'Resolved'];
  const isEscalated = status === 'Escalated';

  const getStepState = (stepName) => {
    if (isEscalated && stepName === 'Resolved') return 'escalated';
    
    const order = ['Reported', 'Diagnosed', 'Assigned', 'Resolved', 'Escalated'];
    const currentIdx = order.indexOf(status);
    const stepIdx = order.indexOf(stepName);

    if (currentIdx === stepIdx) return 'active';
    if (currentIdx > stepIdx) return 'completed';
    return 'pending';
  };

  return (
    <div className="timeline">
      {steps.map((step, idx) => {
        const state = getStepState(step);
        return (
          <div key={idx} className={`timeline-step ${state}`}>
            {state === 'completed' && '✓ '}
            {step}
          </div>
        );
      })}
      {isEscalated && (
        <div className="timeline-step active" style={{ borderColor: '#ef4444', color: '#ef4444' }}>
          🚨 Escalated
        </div>
      )}
    </div>
  );
}
