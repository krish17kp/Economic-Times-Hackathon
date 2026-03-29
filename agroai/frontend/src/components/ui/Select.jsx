import React from 'react';
import { useLanguage } from '../../hooks/useLanguage';

export default function Select({ label, options, error, ...props }) {
  const { t } = useLanguage();

  return (
    <div className="flex flex-col gap-1 w-full">
      {label && <label className="text-sm font-medium text-gray-700">{label}</label>}
      <select 
        className={`border rounded-lg px-3 py-2 bg-white focus:ring-2 focus:ring-green-500 focus:border-green-500 ${error ? 'border-red-500' : 'border-gray-300'}`}
        {...props}
      >
        <option value="" disabled>{t('select_option')}</option>
        {options.map(opt => (
           <option key={opt.value} value={opt.value}>{opt.label}</option>
        ))}
      </select>
      {error && <span className="text-xs text-red-500">{error}</span>}
    </div>
  );
}
