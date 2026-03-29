import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import Header from '../components/Header';
import BottomNav from '../components/BottomNav';
import Input from '../components/ui/Input';
import Button from '../components/ui/Button';
import Select from '../components/ui/Select';
import { useApi } from '../hooks/useApi';
import { useLanguage } from '../hooks/useLanguage';
import { assistantService } from '../services/assistantService';

export default function Assistant() {
  const { t, lang } = useLanguage();
  const location = useLocation();
  const defaultTopic = location.state?.defaultTopic || 'how_to_convert';
  const [topic, setTopic] = useState(defaultTopic);
  const [query, setQuery] = useState('');
  const [chat, setChat] = useState([]);
  
  const { execute: askQuestion, loading } = useApi(assistantService.askQuestion);

  const getWelcomeMessage = (category, currentLang) => {
    if (currentLang === 'hi') {
      switch(category) {
        case "how_to_convert":
          return "🙏 नमस्ते!\n\nआपने बायोचार गाइड चुना है।\n\nमैं आपकी मदद कर सकता हूँ:\n• बायोचार कैसे बनाएं\n• खर्च और सेटअप\n• अनुमानित मुनाफा\n\nअपना सवाल पूछें या नीचे से चुनें 👇";
        case "equipment":
          return "🔥 नमस्ते!\n\nआपने ब्रिकेट जानकारी चुनी है।\n\nमैं आपकी मदद कर सकता हूँ:\n• ब्रिकेट कैसे बनाएं\n• आवश्यक मशीनें\n• बिक्री मूल्य\n\nअपना सवाल पूछें या नीचे से चुनें 👇";
        case "quality_tips":
          return "🍄 नमस्ते!\n\nआपने मशरूम की खेती चुनी है।\n\nमैं आपकी मदद कर सकता हूँ:\n• सेटअप की प्रक्रिया\n• उत्पादन खर्च\n• मुनाफे की संभावना\n\nअपना सवाल पूछें या नीचे से चुनें 👇";
        case "general_policy":
        default:
          return "📜 नमस्ते!\n\nआपने सरकारी योजनाएं चुनी हैं।\n\nमैं आपकी मदद कर सकता हूँ:\n• सब्सिडी और योजनाएं\n• जुर्माने के नियम\n• कार्बन क्रेडिट्स\n\nअपना सवाल पूछें या नीचे से चुनें 👇";
      }
    } else {
      switch(category) {
        case "how_to_convert":
          return "🙏 Namaste!\n\nYou selected Biochar Guide.\n\nI can help you with:\n• How to make biochar\n• Cost and setup\n• Profit potential\n\nAsk your question or choose below 👇";
        case "equipment":
          return "🔥 Namaste!\n\nYou selected Briquette Info.\n\nI can help you with:\n• Making briquettes\n• Machines required\n• Selling price\n\nAsk your question or choose below 👇";
        case "quality_tips":
          return "🍄 Namaste!\n\nYou selected Mushroom Cultivation.\n\nI can help you with:\n• Setup process\n• Production cost\n• Profit margin\n\nAsk your question or choose below 👇";
        case "general_policy":
        default:
          return "📜 Namaste!\n\nYou selected General Policy.\n\nI can help you with:\n• Subsidies & Schemes\n• Penalty rules\n• Carbon credits\n\nAsk your question or choose below 👇";
      }
    }
  };

  const getQuickOptions = (category, currentLang) => {
    if (currentLang === 'hi') {
      switch(category) {
        case "how_to_convert":
          return ["बायोचार कैसे बनाएं?", "सेटअप का खर्च क्या है?", "इससे कितना मुनाफा होगा?"];
        case "equipment":
          return ["ब्रिकेट कैसे बनाएं?", "कौन सी मशीन चाहिए?", "ब्रिकेट का बिक्री मूल्य?"];
        case "quality_tips":
          return ["मशरूम कैसे उगाएं?", "सेटअप में कितना खर्च आएगा?", "क्या यह लाभदायक है?"];
        case "general_policy":
        default:
          return ["सरकारी सब्सिडी क्या है?", "पराली जलाने पर क्या जुर्माना है?", "लोन के लिए कैसे आवेदन करें?"];
      }
    } else {
      switch(category) {
        case "how_to_convert":
          return ["How to make biochar?", "Cost of biochar setup?", "Profit from biochar?"];
        case "equipment":
          return ["How to make briquettes?", "Machines required?", "Selling price of briquettes?"];
        case "quality_tips":
          return ["How to grow mushrooms?", "Cost to setup?", "Profit from mushrooms?"];
        case "general_policy":
        default:
          return ["Government subsidies?", "Penalty for burning?", "Apply for loans?"];
      }
    }
  };

  // Initialize with welcome message on mount and reset chat on language switch
  useEffect(() => {
    setChat([{ sender: 'bot', text: getWelcomeMessage(topic, lang) }]);
    // We do NOT clear query here so user doesn't lose a typed string just by changing language
  }, [lang]);

  const handleCategoryChange = (newCategory) => {
    setTopic(newCategory);
    setQuery('');
    setChat([{ sender: 'bot', text: getWelcomeMessage(newCategory, lang) }]);
  };

  const handleQuickQuestion = (questionText) => {
    setQuery(questionText);
    submitQuestion(questionText);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    submitQuestion(query);
  };

  const submitQuestion = async (textToSubmit) => {
    if (!textToSubmit.trim()) return;

    const userMessage = { sender: 'user', text: textToSubmit };
    setChat(prev => [...prev, userMessage]);
    setQuery('');

    try {
      const response = await askQuestion({
        question: userMessage.text,
        question_category: topic,
        language: lang,
        context: null
      });
      setChat(prev => [...prev, { sender: 'bot', text: response.answer }]);
    } catch (err) {
      setChat(prev => [...prev, { sender: 'bot', text: t('assistant_error') }]);
    }
  };

  return (
    <div className="min-h-screen pb-24 bg-gray-50 flex flex-col">
      <Header title={t('ai_assistant')} />
      
      <div className="p-4 bg-white border-b sticky top-0 z-40 shadow-sm">
        <Select 
          value={topic}
          onChange={(e) => handleCategoryChange(e.target.value)}
          options={[
            { value: 'how_to_convert', label: t('topic_biochar') },
            { value: 'equipment', label: t('topic_briquette') },
            { value: 'quality_tips', label: t('topic_mushroom') },
            { value: 'general_policy', label: t('topic_policy') }
          ]}
        />
      </div>

      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {chat.map((msg, i) => (
          <div key={i} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] p-4 rounded-2xl text-[15px] leading-relaxed shadow-sm whitespace-pre-wrap ${
              msg.sender === 'user' 
                ? 'bg-green-600 text-white rounded-tr-none' 
                : 'bg-[#f1f5f9] border border-slate-200 text-slate-800 rounded-tl-none'
            }`}>
              {msg.text}
            </div>
          </div>
        ))}

        {!loading && chat.length === 1 && (
          <div className="flex flex-wrap gap-2 mt-4 ml-2 max-w-[85%]">
            {getQuickOptions(topic, lang).map((opt, idx) => (
              <button 
                key={idx} 
                onClick={() => handleQuickQuestion(opt)}
                className="px-4 py-2 bg-white border border-green-200 text-green-700 text-sm rounded-full shadow-sm hover:bg-green-50 transition-colors active:scale-95 text-left"
              >
                {opt}
              </button>
            ))}
          </div>
        )}

        {loading && (
          <div className="flex justify-start">
            <div className="bg-[#f1f5f9] border border-slate-200 text-slate-500 p-4 rounded-2xl rounded-tl-none text-[15px] animate-pulse">
              {t('consulting_docs')}
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="p-3 bg-white border-t border-gray-200 flex gap-2 fixed bottom-14 w-full shadow-[0_-4px_6px_-1px_rgba(0,0,0,0.05)]">
        <Input 
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder={t('type_question')}
          className="flex-1 bg-gray-50 border-gray-200 focus:border-green-500 focus:ring-green-500 rounded-xl"
        />
        <Button type="submit" disabled={!query.trim() || loading} className="px-6 rounded-xl font-medium shadow-sm active:scale-95 transition-transform">
          {t('send')}
        </Button>
      </form>
      
      <BottomNav />
    </div>
  );
}
