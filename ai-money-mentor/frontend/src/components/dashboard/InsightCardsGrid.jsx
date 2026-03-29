import React from 'react';
import InsightCard from './InsightCard';

export default function InsightCardsGrid({ insights }) {
    if (!insights || insights.length === 0) return null;

    return (
        <div className="space-y-4">
            {insights.map((insight, idx) => (
                <InsightCard key={insight.id || idx} insight={insight} />
            ))}
        </div>
    );
}
