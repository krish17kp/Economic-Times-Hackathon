import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function Header({ title }) {
  const navigate = useNavigate();
  // Check if we are on the home page context based on title
  const isHome = title === 'AgroAI' || title === 'एग्रो AI';

  return (
    <header className="bg-white p-3 shadow-md flex items-center justify-between sticky top-0 z-50 border-b-2 border-green-600 h-16">
      <div 
        className="flex items-center gap-3 cursor-pointer" 
        onClick={() => navigate('/')}
      >
        <img 
          src="/images/logo.png" 
          alt="Agro AI Logo" 
          className="h-12 w-auto object-contain drop-shadow-sm transition-transform active:scale-95" 
          onError={(e) => {
            // Fallback while generating/missing
            e.target.style.display = 'none';
            if (isHome) e.target.nextSibling.style.display = 'block';
          }}
        />
        <h1 
          className={`text-xl font-bold font-sans text-green-700 tracking-tight ${isHome ? 'hidden sm:block' : 'block'}`}
        >
          {!isHome ? title : title}
        </h1>
      </div>
      
      <div className="w-9 h-9 bg-green-100 rounded-full flex items-center justify-center text-sm font-bold shadow-inner ring-2 ring-green-500 ring-offset-1 text-green-800">
        👨‍🌾
      </div>
    </header>
  );
}
