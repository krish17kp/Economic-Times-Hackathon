import React from 'react';
import { formatCurrency } from '../utils/formatCurrency';

// Accepts the full `options` array from the compare API response
export default function ComparisonTable({ options = [] }) {
  if (!options || options.length === 0) {
    return <p className="text-sm text-gray-400 text-center p-4">No options available.</p>;
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-200">
      <table className="min-w-full text-left bg-white text-sm">
        <thead className="bg-gray-50 border-b">
          <tr>
            <th className="p-3 font-semibold text-gray-700">Option</th>
            <th className="p-3 font-semibold text-gray-700">Net Profit</th>
            <th className="p-3 font-semibold text-gray-700">Time</th>
          </tr>
        </thead>
        <tbody>
          {options.map((opt) => (
            <tr key={opt.option_type} className="border-b last:border-0">
              <td className="p-3 font-medium text-gray-800">{opt.label_en}</td>
              <td className="p-3 font-bold text-green-700">{formatCurrency(opt.net_profit)}</td>
              <td className="p-3 text-gray-500">{opt.time_to_money_days}d</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
