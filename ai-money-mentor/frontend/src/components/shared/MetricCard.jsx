import React from 'react';

export default function MetricCard({ title, value, subtitle, subtitleColor = "text-slate-500" }) {
    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col">
            <h3 className="text-sm font-medium text-slate-500 mb-2">{title}</h3>
            <div className="text-2xl font-bold text-slate-900">{value}</div>
            {subtitle && (
                <div className={`text-sm mt-2 font-medium ${subtitleColor}`}>
                    {subtitle}
                </div>
            )}
        </div>
    );
}
