import React, { useState } from 'react';
import { Plus, Trash2, ChevronDown } from 'lucide-react';

const CATEGORIES = [
    "Large Cap Equity",
    "Mid Cap Equity",
    "Small Cap Equity",
    "Large & Mid Cap Equity",
    "Flexi Cap Equity",
    "ELSS",
    "Index Fund",
    "International Equity",
    "Debt - Liquid",
    "Debt - Short Duration",
    "Debt - Long Duration",
    "Debt - Gilt",
    "Hybrid - Aggressive",
    "Hybrid - Conservative",
    "Sectoral/Thematic Equity",
    "Uncategorized",
];

const EMPTY_FUND = {
    fund_name: '',
    category: 'Large Cap Equity',
    purchase_value: '',
    current_value: '',
    purchase_date: '',
};

export default function ManualEntryForm({ onSubmit, isLoading }) {
    const [funds, setFunds] = useState([{ ...EMPTY_FUND }]);
    const [investorName, setInvestorName] = useState('');
    const [error, setError] = useState('');

    const addFund = () => setFunds([...funds, { ...EMPTY_FUND }]);

    const removeFund = (idx) => {
        if (funds.length === 1) return;
        setFunds(funds.filter((_, i) => i !== idx));
    };

    const updateFund = (idx, field, value) => {
        const updated = [...funds];
        updated[idx] = { ...updated[idx], [field]: value };
        setFunds(updated);
    };

    const handleSubmit = () => {
        setError('');
        const validFunds = funds.filter(f => f.fund_name.trim() && f.purchase_value && f.current_value);
        if (validFunds.length === 0) {
            setError('Please fill in at least one fund with name, invested amount, and current value.');
            return;
        }

        const portfolio = {
            investor_name: investorName.trim() || 'Investor',
            funds: validFunds.map((f, i) => ({
                fund_name: f.fund_name.trim(),
                category: f.category,
                asset_type: f.category.toLowerCase().includes('debt') ? 'debt'
                    : f.category.toLowerCase().includes('hybrid') ? 'hybrid' : 'equity',
                purchase_value: parseFloat(f.purchase_value) || 0,
                current_value: parseFloat(f.current_value) || 0,
                purchase_date: f.purchase_date || null,
                folio: `manual_${i + 1}`,
                units: null,
                nav: null,
            })),
            fund_count: validFunds.length,
            parse_confidence: 'high',
            source: 'manual_entry',
        };

        onSubmit(portfolio);
    };

    return (
        <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
            <div>
                <label className="block text-sm font-semibold text-slate-700 mb-1">Your Name (optional)</label>
                <input
                    type="text"
                    placeholder="e.g. Rajesh Kumar"
                    value={investorName}
                    onChange={e => setInvestorName(e.target.value)}
                    className="w-full border border-slate-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand focus:border-transparent transition"
                />
            </div>

            <div className="space-y-4">
                {funds.map((fund, idx) => (
                    <div key={idx} className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 relative">
                        <div className="flex gap-3 mb-3 items-start">
                            <div className="flex-grow">
                                <label className="text-xs font-semibold text-slate-500 mb-1 block">FUND NAME *</label>
                                <input
                                    type="text"
                                    placeholder="e.g. Axis Bluechip Fund Direct Growth"
                                    value={fund.fund_name}
                                    onChange={e => updateFund(idx, 'fund_name', e.target.value)}
                                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand transition"
                                />
                            </div>
                            {funds.length > 1 && (
                                <button
                                    onClick={() => removeFund(idx)}
                                    className="mt-5 text-red-400 hover:text-red-600 transition p-1"
                                >
                                    <Trash2 size={16} />
                                </button>
                            )}
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                            <div>
                                <label className="text-xs font-semibold text-slate-500 mb-1 block">CATEGORY</label>
                                <div className="relative">
                                    <select
                                        value={fund.category}
                                        onChange={e => updateFund(idx, 'category', e.target.value)}
                                        className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm appearance-none focus:outline-none focus:ring-2 focus:ring-brand transition bg-white"
                                    >
                                        {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
                                    </select>
                                    <ChevronDown size={12} className="absolute right-2 top-3 text-slate-400 pointer-events-none" />
                                </div>
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-slate-500 mb-1 block">INVESTED (₹) *</label>
                                <input
                                    type="number"
                                    placeholder="50000"
                                    value={fund.purchase_value}
                                    onChange={e => updateFund(idx, 'purchase_value', e.target.value)}
                                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand transition"
                                />
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-slate-500 mb-1 block">CURRENT VALUE (₹) *</label>
                                <input
                                    type="number"
                                    placeholder="65000"
                                    value={fund.current_value}
                                    onChange={e => updateFund(idx, 'current_value', e.target.value)}
                                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand transition"
                                />
                            </div>
                            <div>
                                <label className="text-xs font-semibold text-slate-500 mb-1 block">PURCHASE DATE</label>
                                <input
                                    type="date"
                                    value={fund.purchase_date}
                                    onChange={e => updateFund(idx, 'purchase_date', e.target.value)}
                                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand transition"
                                />
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {error && (
                <div className="text-red-600 text-sm bg-red-50 border border-red-200 rounded-xl p-3">
                    {error}
                </div>
            )}

            <div className="flex gap-3">
                <button
                    onClick={addFund}
                    className="flex items-center gap-2 px-4 py-2 border border-slate-300 rounded-xl text-sm font-medium text-slate-600 hover:border-brand hover:text-brand transition-colors"
                >
                    <Plus size={16} /> Add Fund
                </button>
                <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="flex-grow bg-brand text-white rounded-xl py-2 font-semibold text-sm hover:bg-brand-dark transition-colors disabled:opacity-75 flex items-center justify-center gap-2"
                >
                    {isLoading ? (
                        <><span className="animate-spin">⟳</span> Analysing...</>
                    ) : (
                        '✨ Generate My Analysis'
                    )}
                </button>
            </div>
        </div>
    );
}
