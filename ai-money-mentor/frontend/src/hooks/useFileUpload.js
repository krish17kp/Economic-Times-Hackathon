import { useState } from 'react';
import { uploadFile } from '../services/api';

export function useFileUpload() {
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleUpload = async (selectedFile) => {
        setIsUploading(true);
        setError(null);
        try {
            const data = await uploadFile(selectedFile);
            if (!data.success) {
                setError(data.message || 'Failed to parse file. Try using CSV format or enter manually.');
                return null;
            }
            return data;
        } catch (err) {
            setError(err.response?.data?.detail || err.response?.data?.message || err.message || 'Network error — is the backend running?');
            return null;
        } finally {
            setIsUploading(false);
        }
    };

    return { file, setFile, isUploading, error, setError, handleUpload };
}
