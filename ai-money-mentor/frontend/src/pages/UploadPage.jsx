import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import Container from '../components/layout/Container';
import Header from '../components/layout/Header';
import FileUploadCard from '../components/upload/FileUploadCard';

import ManualEntryForm from '../components/upload/ManualEntryForm';
import ErrorBanner from '../components/shared/ErrorBanner';
import { useFileUpload } from '../hooks/useFileUpload';
import { analyzePortfolio } from '../services/api';

const TABS = [
    { id: 'upload', label: '📄 Upload Statement' },
    { id: 'manual', label: '✏️ Enter Manually' },
];

export default function UploadPage() {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState('upload');
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const { isUploading, error, setError, handleUpload } = useFileUpload();

    const onFileSelect = async (file) => {
        const data = await handleUpload(file);
        if (data && data.portfolio) {
            navigate('/analyzing', {
                state: { portfolioData: data.portfolio, warnings: data.warnings || [] }
            });
        }
    };

    const onManualSubmit = async (portfolio) => {
        setIsAnalyzing(true);
        setError(null);
        try {
            const result = await analyzePortfolio(portfolio);
            navigate('/dashboard', {
                state: { analysisData: result, isSample: false, warnings: [], portfolio }
            });
        } catch (err) {
            setError('Analysis failed — is the backend running on port 8000?');
        } finally {
            setIsAnalyzing(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-white to-emerald-50/30">
            <Header />
            <Container className="max-w-3xl mt-8">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-extrabold text-slate-800 mb-3 tracking-tight">
                        Your personal portfolio analyst
                    </h1>
                    <p className="text-lg text-slate-600 max-w-xl mx-auto">
                        Get a comprehensive health check, XIRR, overlap analysis, and a tailored rebalancing plan — in seconds.
                    </p>
                </div>

                {/* Tab switcher */}
                <div className="flex gap-1 bg-slate-100 rounded-2xl p-1 mb-6">
                    {TABS.map(tab => (
                        <button
                            key={tab.id}
                            onClick={() => { setActiveTab(tab.id); setError(null); }}
                            className={`flex-1 py-2.5 rounded-xl text-sm font-semibold transition-all ${
                                activeTab === tab.id
                                    ? 'bg-white shadow-sm text-slate-900'
                                    : 'text-slate-500 hover:text-slate-700'
                            }`}
                        >
                            {tab.label}
                        </button>
                    ))}
                </div>

                {error && (
                    <div className="mb-4">
                        <ErrorBanner message={error} onDismiss={() => setError(null)}
                            suggestion="Try the 'Enter Manually' tab to bypass file parsing entirely." />
                    </div>
                )}

                {activeTab === 'upload' && (
                    <div className="space-y-4">
                        <FileUploadCard onFileSelect={onFileSelect} isUploading={isUploading} error={!!error} />
                        <p className="text-center text-xs text-slate-400">
                            If your PDF doesn't parse correctly, use the "✏️ Enter Manually" tab instead
                        </p>
                    </div>
                )}

                {activeTab === 'manual' && (
                    <div>
                        <p className="text-sm text-slate-500 mb-4 text-center">
                            Enter your mutual fund holdings directly. Find values on your fund app, CAMS, or MF Central.
                        </p>
                        <ManualEntryForm onSubmit={onManualSubmit} isLoading={isAnalyzing} />
                    </div>
                )}


                <p className="text-center text-xs text-slate-400 mt-6 flex items-center justify-center gap-1">
                    🔒 Your data is processed locally and never stored.
                </p>
            </Container>
        </div>
    );
}
