import React, { useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';

export default function FileUploadCard({ onFileSelect, isUploading, error }) {
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef(null);

    const handleDrag = (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") setIsDragging(true);
        else if (e.type === "dragleave") setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleFile = (file) => {
        if (!file.name.endsWith('.pdf') && !file.name.endsWith('.csv')) {
            alert('Please upload a PDF or CSV file');
            return;
        }
        if (file.size > 10 * 1024 * 1024) {
            alert('File size exceeds 10MB limit');
            return;
        }
        onFileSelect(file);
    };

    return (
        <form 
            onDragEnter={handleDrag} 
            onDragLeave={handleDrag} 
            onDragOver={handleDrag} 
            onDrop={handleDrop}
            className={`cursor-pointer rounded-2xl border-2 border-dashed p-10 text-center transition-colors ${
                isDragging ? 'border-brand bg-brand-light/30' : 
                error ? 'border-red-300 bg-red-50' : 'border-slate-300 bg-white hover:border-brand-light hover:bg-slate-50'
            }`}
            onClick={() => fileInputRef.current?.click()}
        >
            <input 
                type="file" 
                ref={fileInputRef} 
                className="hidden" 
                accept=".pdf,.csv" 
                onChange={handleChange} 
            />
            <div className="flex justify-center mb-4">
                <div className="bg-slate-100 p-4 rounded-full">
                    <UploadCloud className="w-10 h-10 text-brand" />
                </div>
            </div>
            <h3 className="text-xl font-semibold mb-2">Drop your CAMS statement</h3>
            <p className="text-slate-500">Supports: PDF, CSV (up to 10MB)</p>
            {isUploading && <p className="text-blue-600 mt-4 font-medium animate-pulse">Uploading...</p>}
        </form>
    );
}
