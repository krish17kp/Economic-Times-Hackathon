import React from 'react';

export default function Button({ children, variant = 'primary', className = '', ...props }) {
  const baseClass = "px-4 py-2 rounded-lg font-medium transition-colors flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100 disabled:hover:bg-opacity-100";
  const variants = {
    primary: "bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-400 disabled:text-white disabled:hover:bg-gray-400",
    secondary: "bg-green-100 text-green-800 hover:bg-green-200 disabled:bg-gray-100 disabled:text-gray-400",
    outline: "border-2 border-green-600 text-green-600 hover:bg-green-50 disabled:border-gray-300 disabled:text-gray-400"
  };

  return (
    <button className={`${baseClass} ${variants[variant]} ${className}`} {...props}>
      {children}
    </button>
  );
}
