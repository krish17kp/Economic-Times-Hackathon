import React, { useEffect, useState } from 'react';

export default function HealthScoreCard({ score = 0, label = "", color = "#10b981", title="Health Score" }) {
    const [displayScore, setDisplayScore] = useState(0);

    useEffect(() => {
        let current = 0;
        const target = score;
        if(target === 0) return;
        
        const duration = 1500;
        const increment = target / (duration / 16);
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                setDisplayScore(target);
                clearInterval(timer);
            } else {
                setDisplayScore(Math.floor(current));
            }
        }, 16);
        return () => clearInterval(timer);
    }, [score]);

    return (
        <div className="bg-slate-900 rounded-3xl p-8 flex flex-col items-center justify-center text-white relative overflow-hidden shadow-xl h-full">
            <h3 className="text-slate-300 text-lg font-medium mb-6 z-10">{title}</h3>
            
            <div className="relative w-48 h-48 flex items-center justify-center z-10">
                <svg className="absolute inset-0 w-full h-full -rotate-90">
                    <circle 
                        cx="96" cy="96" r="80" 
                        fill="transparent" 
                        stroke="rgba(255,255,255,0.1)" 
                        strokeWidth="16" 
                    />
                    <circle 
                        cx="96" cy="96" r="80" 
                        fill="transparent" 
                        stroke={color} 
                        strokeWidth="16" 
                        strokeDasharray={2 * Math.PI * 80}
                        strokeDashoffset={2 * Math.PI * 80 * (1 - displayScore / 100)}
                        className="transition-all duration-1000 ease-out"
                        strokeLinecap="round"
                    />
                </svg>
                <div className="flex flex-col items-center">
                    <span className="text-6xl font-bold">{displayScore}</span>
                    <span className="text-slate-400 text-sm mt-1">/ 100</span>
                </div>
            </div>
            
            <div className="mt-8 px-6 py-2 rounded-full font-semibold border z-10" style={{ color: color, borderColor: `${color}40`, backgroundColor: `${color}10` }}>
                {label}
            </div>
        </div>
    );
}
