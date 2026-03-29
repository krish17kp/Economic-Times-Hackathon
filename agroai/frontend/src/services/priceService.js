import api from './api';

export const priceService = {
  getPrice: (wasteType, region = 'Punjab', days = 30) => api.get(`/price/${wasteType}?region=${region}&days=${days}`),
};
