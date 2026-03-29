import api from './api';

export const assistantService = {
  askQuestion: (data) => api.post('/assistant/ask', data),
};
