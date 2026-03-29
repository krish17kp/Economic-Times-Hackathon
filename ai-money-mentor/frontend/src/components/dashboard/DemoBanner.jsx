import React, { useState } from 'react';
import { X, Info, Sparkles } from 'lucide-react';

export default function DemoBanner({ warnings }) {
    const [dismissed, setDismissed] = useState(false);
    if (dismissed) return null;

    const hasWarnings = warnings && warnings.length > 0;
    if (!hasWarnings) return null;

    return (
        <div className="bg-indigo-50 border border-indigo-200 rounded-2xl p-4 mb-6 animate-in fade-in slide-in-from-top-4 duration-500">
            <div className="flex gap-3 pr-8">
                <Info className="w-5 h-5 text-indigo-500 shrink-0 mt-0.5" />
                <div className="space-y-1">
                    {warnings.map((w, i) => (
                        <p key={i} className="text-indigo-600 text-sm">
                            {w}
                        </p>
                    ))}
                </div>
            </div>
            <button
                onClick={() => setDismissed(true)}
                className="absolute top-4 right-4 text-indigo-400 hover:text-indigo-700 p-1 rounded-lg hover:bg-indigo-100 transition-colors"
                aria-label="Dismiss"
            >
                <X className="w-4 h-4" />
            </button>
        </div>
    );
}
