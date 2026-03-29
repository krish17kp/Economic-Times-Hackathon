import React from 'react';
import { Landmark } from 'lucide-react';

export default function Header() {
    return (
        <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-10">
            <div className="max-w-6xl mx-auto px-4 h-16 flex items-center gap-2">
                <div className="bg-brand-light p-2 rounded-lg text-brand-dark">
                    <Landmark size={24} />
                </div>
                <h1 className="text-xl font-bold tracking-tight text-slate-800">
                    AI Money Mentor
                </h1>
            </div>
        </header>
    );
}
