import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { formatCurrency } from '../../utils/formatters';

const COLORS = ['#10b981', '#3b82f6', '#f59e0b', '#8b5cf6', '#ec4899', '#14b8a6', '#f43f5e', '#64748b'];

export default function AllocationChart({ categories }) {
    if (!categories) return null;
    
    const data = Object.values(categories).map((c, i) => ({
        name: c.name,
        value: c.value,
        percentage: c.percentage,
        color: COLORS[i % COLORS.length]
    })).sort((a, b) => b.value - a.value);

    const CustomTooltip = ({ active, payload }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className="bg-white p-3 rounded-lg shadow-lg border border-slate-100 text-sm">
                    <div className="font-semibold text-slate-800">{data.name}</div>
                    <div className="text-slate-600 mt-1">{formatCurrency(data.value)}</div>
                    <div className="text-brand font-medium">{data.percentage.toFixed(1)}%</div>
                </div>
            );
        }
        return null;
    };

    return (
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm h-full flex flex-col">
            <h3 className="text-lg font-bold text-slate-800 mb-6">Asset Allocation</h3>
            <div className="flex-grow min-h-[250px]">
                <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                        <Pie
                            data={data}
                            cx="50%"
                            cy="50%"
                            innerRadius={"60%"}
                            outerRadius={"80%"}
                            paddingAngle={2}
                            dataKey="value"
                            stroke="none"
                        >
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                        </Pie>
                        <Tooltip content={<CustomTooltip />} />
                        <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
}
