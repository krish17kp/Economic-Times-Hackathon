import api from './api';

export const buyerService = {
  getNearbyBuyers: (params) => api.get('/buyers/nearby', { params }),
};
