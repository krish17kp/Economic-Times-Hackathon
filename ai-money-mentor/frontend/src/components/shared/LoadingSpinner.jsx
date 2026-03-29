import React from 'react';

export default function LoadingSpinner({ size = "md" }) {
    const sizeClasses = {
        sm: "w-4 h-4 border-2",
        md: "w-8 h-8 border-3",
        lg: "w-12 h-12 border-4"
    };

    return (
        <div className={`animate-spin rounded-full border-t-brand border-slate-200 ${sizeClasses[size]}`}></div>
    );
}
