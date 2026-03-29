import React from 'react';

export default function SubScoreCard({ name, score, label, detail, color }) {
    return (
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex flex-col gap-2 relative overflow-hidden h-full">
            <div className="absolute left-0 top-0 bottom-0 w-1.5" style={{ backgroundColor: color }}></div>
            <div className="text-slate-500 font-medium text-sm pl-2">{name}</div>
            <div className="flex items-end gap-3 pl-2">
                <span className="text-3xl font-bold text-slate-800 leading-none">{score}</span>
                <span className="text-sm font-semibold mb-0.5" style={{ color }}>{label}</span>
            </div>
            <div className="text-sm text-slate-500 mt-auto pl-2">{detail}</div>
        </div>
    );
}
