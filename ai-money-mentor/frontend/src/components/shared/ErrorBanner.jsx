import React from 'react';
import { AlertCircle, X } from 'lucide-react';

export default function ErrorBanner({ title, message, onDismiss, suggestion }) {
    return (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 flex items-start gap-3">
            <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
            <div className="flex-grow">
                {title && <h3 className="text-sm font-semibold text-red-800">{title}</h3>}
                <p className="text-sm text-red-700 mt-1">{message}</p>
                {suggestion && <p className="text-sm text-red-600 mt-2 font-medium">💡 {suggestion}</p>}
            </div>
            {onDismiss && (
                <button onClick={onDismiss} className="text-red-500 hover:text-red-700">
                    <X className="w-5 h-5" />
                </button>
            )}
        </div>
    );
}
