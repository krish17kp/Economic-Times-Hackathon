import api from './api';

export const wasteService = {
  getWasteTypes: () => api.get('/waste/types'),
  submitWaste: (data) => api.post('/waste/submit', data),
};
