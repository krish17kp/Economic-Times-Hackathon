export function formatWeight(kg) {
  if (kg === undefined || kg === null) return '0 kg';
  if (kg >= 1000) return `${(kg / 1000).toFixed(1)} Tonnes`;
  return `${Math.round(kg)} kg`;
}
