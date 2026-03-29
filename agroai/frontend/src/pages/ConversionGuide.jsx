import React from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import Header from '../components/Header';
import BottomNav from '../components/BottomNav';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import { formatCurrency } from '../utils/formatCurrency';
import { useLanguage } from '../hooks/useLanguage';

export default function ConversionGuide() {
  const { type } = useParams();
  const location = useLocation();
  const navigate = useNavigate();
  const { t } = useLanguage();
  
  const rec = location.state;

  if (!rec) {
    return (
      <div className="min-h-screen p-4 flex flex-col items-center justify-center">
        <p>{t('no_data')}</p>
        <Button onClick={() => navigate(-1)}>{t('back')}</Button>
      </div>
    );
  }

  return (
    <div className="min-h-screen pb-20 bg-gray-50">
      <Header title={t('conversion_guide')} />
      <main className="p-4 space-y-4 max-w-lg mx-auto">
        <Button variant="outline" className="w-full justify-start py-2" onClick={() => navigate(-1)}>
          ← {t('back')}
        </Button>

        <Card className="p-5 border-t-4 border-t-blue-500">
          <h2 className="text-xl font-bold capitalize mb-4">{t('how_to_make')} {t(type.replace('_', ' '))}</h2>
          
          <div className="space-y-4">
            <div className="bg-blue-50 p-4 rounded-lg flex justify-between">
              <div>
                <p className="text-xs text-gray-500 uppercase font-bold">{t('est_output')}</p>
                <p className="font-bold text-lg text-blue-900">{rec.output_quantity_kg} {t('kg')}</p>
              </div>
              <div className="text-right">
                <p className="text-xs text-gray-500 uppercase font-bold">{t('est_time')}</p>
                <p className="font-bold text-lg text-blue-900">{rec.processing_time_days} {t('days')}</p>
              </div>
            </div>

            <div className="border border-gray-200 rounded-lg overflow-hidden">
              <div className="bg-gray-50 p-3 border-b border-gray-200">
                <h3 className="font-bold text-sm text-gray-800">{t('fin_breakdown')}</h3>
              </div>
              <div className="p-3 bg-white space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">{t('exp_revenue')}</span>
                  <span className="font-semibold">{formatCurrency(rec.gross_revenue)}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">{t('proc_cost')}</span>
                  <span className="font-semibold text-red-500">-{formatCurrency(rec.processing_cost)}</span>
                </div>
                <div className="flex justify-between pt-2 border-t font-bold">
                  <span className="text-gray-800">{t('est_net_profit')}</span>
                  <span className="text-green-600">{formatCurrency(rec.net_profit)}</span>
                </div>
              </div>
            </div>

            <div className="pt-4 space-y-3 border-t">
              <h3 className="font-bold text-gray-800 text-lg">👨‍🌾 {t('ask_ai_guide')}</h3>
              <p className="text-sm text-gray-600 leading-relaxed mb-3">
                {t('ai_guide_desc')}<span className="capitalize font-bold">{t(type.replace('_', ' '))}</span>
              </p>
              <Button 
                className="w-full font-bold text-lg bg-indigo-600 hover:bg-indigo-700 mb-2 py-3 shadow border-0" 
                onClick={() => {
                  const toTopic = type === 'briquette' ? 'equipment' 
                                : type === 'mushroom_substrate' ? 'quality_tips' 
                                : 'how_to_convert';
                  navigate('/assistant', { state: { defaultTopic: toTopic } });
                }}
              >
                {t('chat_with_agroai')}
              </Button>
            </div>

            <div className="pt-4 space-y-3">
              <h3 className="font-bold text-gray-800">{t('resources')}</h3>
              <p className="text-sm text-gray-600 leading-relaxed">
                {t('contact_kvk_1')}<span className="capitalize">{t(type.replace('_', ' '))}</span>{t('contact_kvk_2')}
              </p>
              <a 
                href="https://icar.org.in/en/krishi-vigyan-kendras" 
                target="_blank" 
                rel="noreferrer"
                className="w-full flex justify-center py-2 px-4 border border-green-600 outline-none text-green-700 bg-white hover:bg-green-50 rounded-lg shadow-sm font-medium transition-colors"
                style={{textDecoration: 'none'}}
              >
                {t('find_kvk')}
              </a>
            </div>
          </div>
        </Card>
      </main>
      <BottomNav />
    </div>
  );
}
