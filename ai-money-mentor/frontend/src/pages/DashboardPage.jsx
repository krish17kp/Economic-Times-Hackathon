import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Container from '../components/layout/Container';
import Header from '../components/layout/Header';
import HealthScoreCard from '../components/dashboard/HealthScoreCard';
import SubScoreGrid from '../components/dashboard/SubScoreGrid';
import PortfolioSummary from '../components/dashboard/PortfolioSummary';
import AllocationChart from '../components/dashboard/AllocationChart';
import InsightCardsGrid from '../components/dashboard/InsightCardsGrid';
import PlainEnglishSummary from '../components/dashboard/PlainEnglishSummary';
import DemoBanner from '../components/dashboard/DemoBanner';
import { formatCurrency } from '../utils/formatters';

export default function DashboardPage() {
    const location = useLocation();
    const navigate = useNavigate();
    const data = location.state?.analysisData;
    const warnings = location.state?.warnings || [];
    const portfolio = location.state?.portfolio;  // raw portfolio for fund table

    if (!data) {
        navigate('/');
        return null;
    }

    const { metrics, health_score, insights, xirr, expense_data, overlaps, rebalancing } = data;

    return (
        <div className="min-h-screen flex flex-col bg-slate-50">
            <Header />
            <Container className="flex-grow max-w-7xl">

                <DemoBanner warnings={warnings} />

                {/* Page header */}
                <div className="flex justify-between items-end mb-6">
                    <div>
                        <h2 className="text-3xl font-bold text-slate-900 tracking-tight">Portfolio X-Ray</h2>
                        <p className="text-slate-500 mt-1">
                            Full analysis across <span className="font-semibold text-slate-700">{metrics.fund_count} funds</span>
                        </p>
                    </div>
                    <button onClick={() => navigate('/')}
                        className="text-sm font-semibold text-brand hover:text-brand-dark px-4 py-2 rounded-xl hover:bg-brand-light/30 border border-transparent hover:border-brand-light transition-all">
                        ↑ Analyse Another
                    </button>
                </div>

                {/* Health Score + Sub-scores */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-6">
                    <div className="lg:col-span-4 h-[300px]">
                        <HealthScoreCard score={health_score.overall} label={health_score.label} color={health_score.color} />
                    </div>
                    <div className="lg:col-span-8 h-[300px]">
                        <SubScoreGrid subScores={health_score.sub_scores} />
                    </div>
                </div>

                {/* Key metrics row */}
                <div className="mb-6">
                    <PortfolioSummary metrics={metrics} xirr={xirr} />
                </div>

                {/* Chart + Insights */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                    <AllocationChart categories={metrics.categories} />
                    <InsightCardsGrid insights={insights} />
                </div>

                {/* EXPENSE RATIO Section */}
                {expense_data && (
                    <ExpenseSection expense={expense_data} />
                )}

                {/* OVERLAP Section */}
                {overlaps && overlaps.length > 0 && (
                    <OverlapSection overlaps={overlaps} />
                )}

                {/* REBALANCING PLAN */}
                {rebalancing && rebalancing.length > 0 && (
                    <RebalancingSection rebalancing={rebalancing} />
                )}

                {/* Fund table from raw portfolio */}
                {portfolio?.funds && portfolio.funds.length > 0 && (
                    <FundTable funds={portfolio.funds} />
                )}

                {/* Plain English Summary */}
                <div className="mb-12">
                    <PlainEnglishSummary summary={data.plain_english_summary} aiGenerated={data.ai_generated} />
                </div>

            </Container>
        </div>
    );
}

/* ──────────────────────────────────────────────────── */
/*  Section Components                                  */
/* ──────────────────────────────────────────────────── */

function ExpenseSection({ expense }) {
    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-6">
            <div className="flex justify-between items-start mb-4">
                <h3 className="text-lg font-bold text-slate-800">💰 Expense Ratio Analysis</h3>
                <div className="text-right">
                    <div className="text-2xl font-bold text-slate-800">₹{expense.total_annual_cost.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</div>
                    <div className="text-xs text-slate-500">annual cost</div>
                </div>
            </div>
            {expense.potential_annual_saving > 500 && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 mb-4 text-sm text-amber-800">
                    💡 Switching {expense.regular_plan_count} regular plan(s) to direct could save you
                    <strong> ₹{expense.potential_annual_saving.toLocaleString('en-IN', { maximumFractionDigits: 0 })}/year</strong>
                </div>
            )}
            <table className="w-full text-sm">
                <thead>
                    <tr className="text-slate-500 border-b border-slate-100">
                        <th className="pb-2 font-medium text-left">Fund</th>
                        <th className="pb-2 font-medium text-right">Expense Ratio</th>
                        <th className="pb-2 font-medium text-right">Annual Cost</th>
                        <th className="pb-2 font-medium text-right">Plan</th>
                    </tr>
                </thead>
                <tbody className="divide-y divide-slate-50">
                    {expense.fund_costs.sort((a, b) => b.annual_cost - a.annual_cost).map((fc, i) => (
                        <tr key={i} className="hover:bg-slate-50">
                            <td className="py-2 text-slate-700 max-w-xs truncate">{fc.fund_name}</td>
                            <td className="py-2 text-right font-medium text-slate-600">{fc.expense_ratio.toFixed(2)}%</td>
                            <td className="py-2 text-right text-slate-600">₹{fc.annual_cost.toLocaleString('en-IN', { maximumFractionDigits: 0 })}</td>
                            <td className="py-2 text-right">
                                <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                                    fc.is_direct ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-600'
                                }`}>
                                    {fc.is_direct ? 'Direct' : 'Regular'}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

function OverlapSection({ overlaps }) {
    const highSeverity = overlaps.filter(o => o.severity === 'high');
    const medSeverity = overlaps.filter(o => o.severity === 'medium');
    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-6">
            <h3 className="text-lg font-bold text-slate-800 mb-4">🔍 Fund Overlap Analysis</h3>
            {highSeverity.length > 0 && (
                <div className="mb-3">
                    <h4 className="text-sm font-semibold text-red-600 mb-2">High Overlap</h4>
                    {highSeverity.map((o, i) => (
                        <div key={i} className="bg-red-50 border border-red-200 rounded-xl px-4 py-3 mb-2">
                            <div className="font-medium text-red-800 text-sm">{o.message}</div>
                            <div className="text-xs text-red-600 mt-1">{o.funds.join(' • ')}</div>
                        </div>
                    ))}
                </div>
            )}
            {medSeverity.map((o, i) => (
                <div key={i} className="bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 mb-2">
                    <div className="font-medium text-amber-800 text-sm">{o.message}</div>
                    <div className="text-xs text-amber-600 mt-1">{o.funds.slice(0, 4).join(' • ')}</div>
                </div>
            ))}
        </div>
    );
}

function RebalancingSection({ rebalancing }) {
    const COLOR_MAP = { reduce: 'red', increase: 'green', hold: 'blue' };
    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-6">
            <h3 className="text-lg font-bold text-slate-800 mb-4">⚖️ Rebalancing Plan</h3>
            <div className="space-y-3">
                {rebalancing.map((r, i) => {
                    const color = COLOR_MAP[r.action] || 'slate';
                    return (
                        <div key={i} className={`flex items-start gap-4 p-4 rounded-xl border bg-${color}-50 border-${color}-200`}>
                            <div className={`mt-0.5 text-lg shrink-0`}>
                                {r.action === 'reduce' ? '🔻' : r.action === 'increase' ? '🔺' : '✅'}
                            </div>
                            <div className="flex-grow">
                                <div className={`font-semibold text-${color}-800 text-sm`}>
                                    {r.action.toUpperCase()} {r.asset}
                                    {r.amount > 0 && (
                                        <span className="ml-1 font-normal">
                                            — ₹{r.amount >= 100000
                                                ? `${(r.amount / 100000).toFixed(2)}L`
                                                : r.amount.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                                        </span>
                                    )}
                                </div>
                                <div className={`text-xs text-${color}-700 mt-1`}>{r.detail}</div>
                            </div>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}

function FundTable({ funds }) {
    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm mb-6 overflow-hidden">
            <h3 className="text-lg font-bold text-slate-800 mb-4">📋 Your Funds</h3>
            <div className="overflow-x-auto">
                <table className="w-full text-sm">
                    <thead>
                        <tr className="text-slate-500 border-b border-slate-100">
                            <th className="pb-2 font-medium text-left">Fund Name</th>
                            <th className="pb-2 font-medium text-right">Category</th>
                            <th className="pb-2 font-medium text-right">Invested</th>
                            <th className="pb-2 font-medium text-right">Current Value</th>
                            <th className="pb-2 font-medium text-right">Return</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-50">
                        {funds.map((f, i) => {
                            const ret = f.purchase_value > 0
                                ? ((f.current_value - f.purchase_value) / f.purchase_value * 100) : 0;
                            return (
                                <tr key={i} className="hover:bg-slate-50">
                                    <td className="py-3 font-medium text-slate-800 max-w-xs truncate" title={f.fund_name}>
                                        {f.fund_name}
                                    </td>
                                    <td className="py-3 text-right">
                                        <span className="bg-slate-100 text-slate-600 text-xs px-2 py-0.5 rounded-full">{f.category}</span>
                                    </td>
                                    <td className="py-3 text-right text-slate-600">
                                        {formatCurrency(f.purchase_value)}
                                    </td>
                                    <td className="py-3 text-right font-semibold text-slate-800">
                                        {formatCurrency(f.current_value)}
                                    </td>
                                    <td className={`py-3 text-right font-semibold ${ret >= 0 ? 'text-green-600' : 'text-red-500'}`}>
                                        {ret > 0 ? '+' : ''}{ret.toFixed(1)}%
                                    </td>
                                </tr>
                            );
                        })}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
