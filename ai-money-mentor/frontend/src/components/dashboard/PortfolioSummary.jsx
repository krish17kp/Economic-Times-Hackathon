import React from 'react';
import { formatCurrency, formatPercentage } from '../../utils/formatters';

export default function PortfolioSummary({ metrics, xirr }) {
    if (!metrics) return null;

    const cards = [
        { title: 'Total Invested', value: formatCurrency(metrics.total_invested) },
        { title: 'Current Value', value: formatCurrency(metrics.current_value) },
        {
            title: 'Absolute Returns',
            value: formatCurrency(metrics.absolute_return),
            subtitle: `${formatPercentage(metrics.return_percentage)} overall return`,
            subtitleColor: metrics.absolute_return >= 0 ? 'text-green-600' : 'text-red-500',
        },
        ...(xirr !== null && xirr !== undefined ? [{
            title: 'XIRR (Annualised)',
            value: `${xirr > 0 ? '+' : ''}${xirr.toFixed(1)}%`,
            subtitle: 'Time-weighted annual return',
            subtitleColor: xirr >= 0 ? 'text-brand' : 'text-red-500',
        }] : []),
    ];

    return (
        <div className={`grid grid-cols-1 md:grid-cols-${cards.length} gap-4`}>
            {cards.map((card, i) => (
                <div key={i} className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm">
                    <h3 className="text-sm font-medium text-slate-500 mb-1">{card.title}</h3>
                    <div className="text-2xl font-bold text-slate-900">{card.value}</div>
                    {card.subtitle && (
                        <div className={`text-sm mt-1 font-medium ${card.subtitleColor || 'text-slate-500'}`}>
                            {card.subtitle}
                        </div>
                    )}
                </div>
            ))}
        </div>
    );
}
