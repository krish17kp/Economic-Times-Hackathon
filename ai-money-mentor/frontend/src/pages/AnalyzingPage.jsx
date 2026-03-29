import React, { useEffect, useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Container from '../components/layout/Container';
import Header from '../components/layout/Header';
import ProgressSteps from '../components/shared/ProgressSteps';
import ErrorBanner from '../components/shared/ErrorBanner';
import { analyzePortfolio } from '../services/api';

const STEPS = [
    { label: "Parsing your portfolio data" },
    { label: "Calculating XIRR & metrics" },
    { label: "Detecting overlaps & costs" },
    { label: "Building your dashboard" },
];

export default function AnalyzingPage() {
    const navigate = useNavigate();
    const location = useLocation();
    const portfolioData = location.state?.portfolioData;
    const uploadWarnings = location.state?.warnings || [];

    const [step, setStep] = useState(0);
    const [hasError, setHasError] = useState(false);

    useEffect(() => {
        if (!portfolioData) {
            navigate('/');
            return;
        }

        const run = async () => {
            setStep(0);
            await delay(600);
            setStep(1);

            let result = null;
            try {
                result = await analyzePortfolio(portfolioData);
            } catch (e) {
                result = null;
            }

            if (result && result.success) {
                setStep(2);
                await delay(500);
                setStep(3);
                await delay(400);
                navigate('/dashboard', {
                    state: {
                        analysisData: result,
                        isSample: portfolioData.source === 'sample_fallback',
                        warnings: uploadWarnings,
                        portfolio: portfolioData,
                    }
                });
            } else {
                setHasError(true);
            }
        };

        run();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    if (hasError) {
        return (
            <div className="min-h-screen bg-slate-50 flex flex-col">
                <Header />
                <Container className="max-w-xl mt-20 text-center">
                    <ErrorBanner
                        title="Backend not reachable"
                        message="Please make sure the FastAPI server is running."
                        suggestion="In your backend folder, run: python run.py"
                    />
                    <button onClick={() => navigate('/')}
                        className="mt-6 px-6 py-3 bg-brand text-white rounded-xl font-semibold hover:bg-brand-dark transition-colors">
                        Go Back
                    </button>
                </Container>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-slate-50 flex flex-col">
            <Header />
            <Container className="max-w-xl mt-16">
                <div className="bg-white rounded-3xl p-10 border border-slate-200 shadow-xl">
                    <div className="flex justify-center mb-6">
                        <div className="w-12 h-12 rounded-full bg-brand-light flex items-center justify-center">
                            <span className="text-2xl animate-spin inline-block" style={{ animationDuration: '2s' }}>⚙️</span>
                        </div>
                    </div>
                    <h2 className="text-2xl font-bold text-slate-800 mb-8 text-center">
                        Analysing your portfolio...
                    </h2>
                    <ProgressSteps steps={STEPS} currentStep={step} />
                    <p className="text-center text-slate-400 mt-8 italic text-sm">
                        Calculating XIRR, overlap analysis & rebalancing plan...
                    </p>
                </div>
            </Container>
        </div>
    );
}

const delay = ms => new Promise(r => setTimeout(r, ms));
