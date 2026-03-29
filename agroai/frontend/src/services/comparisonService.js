import api from './api';

export const comparisonService = {
  compareOptions: (data) => api.post('/compare', data),
  getRecommendation: (data) => api.post('/recommend', data),
};
