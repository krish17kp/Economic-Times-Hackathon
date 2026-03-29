import React from 'react';
import { formatCurrency, formatPercentage } from '../../utils/formatters';

export default function FundTable({ funds }) {
    if (!funds || funds.length === 0) return null;

    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm overflow-hidden flex flex-col h-full">
            <h3 className="text-lg font-bold text-slate-800 mb-4">Your Funds</h3>
            <div className="overflow-x-auto">
                <table className="w-full text-left text-sm whitespace-nowrap">
                    <thead>
                        <tr className="text-slate-500 border-b border-slate-100">
                            <th className="pb-3 font-medium">Fund Name</th>
                            <th className="pb-3 font-medium">Category</th>
                            <th className="pb-3 font-medium text-right">Invested</th>
                            <th className="pb-3 font-medium text-right">Current Value</th>
                            <th className="pb-3 font-medium text-right">Return %</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100">
                        {funds.map((fund, idx) => (
                            <tr key={idx} className="hover:bg-slate-50 transition-colors">
                                <td className="py-4 font-medium text-slate-800 truncate max-w-xs" title={fund.fund_name}>{fund.fund_name}</td>
                                <td className="py-4 text-slate-500">
                                    <span className="bg-slate-100 px-2 py-1 rounded text-xs">{fund.category}</span>
                                </td>
                                <td className="py-4 text-right text-slate-600">{formatCurrency(fund.purchase_value)}</td>
                                <td className="py-4 text-right font-medium text-slate-800">{formatCurrency(fund.current_value)}</td>
                                <td className={`py-4 text-right font-medium ${fund.return_percentage >= 0 ? 'text-green-600' : 'text-red-500'}`}>
                                    {formatPercentage(fund.return_percentage)}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
