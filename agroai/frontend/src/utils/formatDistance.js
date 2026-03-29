export function formatDistance(km) {
  if (km === undefined || km === null) return '0 km';
  return `${Math.round(km)} km`;
}
