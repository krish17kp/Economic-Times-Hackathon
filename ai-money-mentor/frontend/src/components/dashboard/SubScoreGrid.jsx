import React from 'react';
import SubScoreCard from './SubScoreCard';

export default function SubScoreGrid({ subScores }) {
    if (!subScores) return null;
    
    const mappings = [
        { key: 'diversification', name: 'Diversification' },
        { key: 'risk_balance', name: 'Risk Balance' },
        { key: 'overlap', name: 'Fund Overlap' },
        { key: 'cost_efficiency', name: 'Cost Efficiency' }
    ];

    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 h-full">
            {mappings.map(({ key, name }) => {
                const s = subScores[key] || { score: 0, label: 'N/A', detail: '', color: '#cbd5e1' };
                return (
                    <SubScoreCard 
                        key={key}
                        name={name}
                        score={s.score}
                        label={s.label}
                        detail={s.detail}
                        color={s.color}
                    />
                );
            })}
        </div>
    );
}
