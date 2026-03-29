import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';

export default function BottomNav() {
  const navigate = useNavigate();
  const location = useLocation();
  const { lang, setLang } = useLanguage();

  const toggleLang = () => setLang(lang === 'en' ? 'hi' : 'en');

  return (
    <div className="fixed bottom-0 w-full bg-white border-t border-gray-200 flex justify-around p-3 pb-safe z-50">
      <button onClick={() => navigate('/')} className={`flex flex-col items-center ${location.pathname === '/' ? 'text-green-600' : 'text-gray-500'}`}>
        <span className="text-xl">🏠</span>
        <span className="text-xs mt-1">Home</span>
      </button>
      <button onClick={() => navigate('/assistant')} className={`flex flex-col items-center ${location.pathname === '/assistant' ? 'text-green-600' : 'text-gray-500'}`}>
        <span className="text-xl">🤖</span>
        <span className="text-xs mt-1">AI</span>
      </button>
      <button onClick={toggleLang} className="flex flex-col items-center text-gray-500">
        <span className="text-xl">🌐</span>
        <span className="text-xs mt-1">{lang === 'en' ? 'हिंदी' : 'EN'}</span>
      </button>
    </div>
  );
}
