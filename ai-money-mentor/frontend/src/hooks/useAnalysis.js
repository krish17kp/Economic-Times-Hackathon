import { useState } from 'react';
import { analyzePortfolio } from '../services/api';

export function useAnalysis() {
    const [isAnalyzing, setIsAnalyzing] = useState(false);
    const [error, setError] = useState(null);

    const runAnalysis = async (portfolioData) => {
        setIsAnalyzing(true);
        setError(null);
        try {
            const result = await analyzePortfolio(portfolioData);
            return result;
        } catch (err) {
            setError(err.response?.data?.message || err.message);
            return null;
        } finally {
            setIsAnalyzing(false);
        }
    };

    return { isAnalyzing, error, runAnalysis };
}
