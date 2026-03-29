import React from 'react';
import Select from './ui/Select';
import { useLanguage } from '../hooks/useLanguage';

export default function WasteSelector({ value, onChange, wasteTypes = [] }) {
  const { lang } = useLanguage();

  const options = wasteTypes.map(w => ({
    value: w.id,
    label: `${w.icon} ${lang === 'hi' && w.label_hi ? w.label_hi : w.label_en}`
  }));

  return (
    <Select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      options={options}
    />
  );
}
