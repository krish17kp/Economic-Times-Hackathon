import React from 'react';

export default function PlainEnglishSummary({ summary, aiGenerated }) {
    if (!summary) return null;

    return (
        <div className="bg-gradient-to-br from-brand-light/30 to-blue-50/50 border border-brand-light rounded-3xl p-8 relative">
            <h3 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
                <span className="text-2xl">📝</span> In Plain English
            </h3>
            <p className="text-lg text-slate-700 leading-relaxed" style={{ fontFamily: 'Georgia, serif' }}>
                "{summary}"
            </p>
            {aiGenerated && (
                <div className="mt-6 flex justify-end">
                    <span className="inline-flex items-center gap-1 bg-white/60 text-slate-500 text-xs px-2 py-1 rounded-full border border-slate-200">
                        ✨ AI Generated
                    </span>
                </div>
            )}
        </div>
    );
}
