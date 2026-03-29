import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

const api = axios.create({
    baseURL: API_BASE_URL
});

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
    });
    return response.data;
};

export const analyzePortfolio = async (portfolioData) => {
    const response = await api.post('/analyze', { portfolio: portfolioData });
    return response.data;
};

