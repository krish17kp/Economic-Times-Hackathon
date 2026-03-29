import React from 'react';

export default function InsightCard({ insight }) {
    if (!insight) return null;
    
    const typeStyles = {
        warning: 'bg-amber-50 border-amber-200 text-amber-900',
        positive: 'bg-green-50 border-green-200 text-green-900',
        suggestion: 'bg-blue-50 border-blue-200 text-blue-900',
        info: 'bg-slate-50 border-slate-200 text-slate-900'
    };

    const currentStyle = typeStyles[insight.type] || typeStyles.info;

    return (
        <div className={`p-5 rounded-2xl border flex items-start gap-4 ${currentStyle}`}>
            <span className="text-2xl mt-1">{insight.icon || '📌'}</span>
            <div>
                <h4 className="font-semibold text-lg mb-1">{insight.title}</h4>
                <p className="text-sm opacity-90 leading-relaxed">{insight.description}</p>
            </div>
        </div>
    );
}
