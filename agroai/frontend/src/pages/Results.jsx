import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import BottomNav from '../components/BottomNav';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Loader from '../components/ui/Loader';
import { useLanguage } from '../hooks/useLanguage';
import { useApi } from '../hooks/useApi';
import { comparisonService } from '../services/comparisonService';
import { formatCurrency } from '../utils/formatCurrency';

export default function Results() {
  const { t, lang } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const [data, setData] = useState(null);

  const { execute: fetchComparison, loading, error } = useApi(comparisonService.compareOptions);

  useEffect(() => {
    if (!location.state) {
      navigate('/');
      return;
    }
    fetchComparison({
      waste_type: location.state.waste_type,
      quantity_kg: parseFloat(location.state.quantity_kg),
      quality: location.state.quality,
      latitude: location.state.latitude || null,
      longitude: location.state.longitude || null,
      pincode: location.state.pincode || null,
    }).then(res => setData(res)).catch(() => {});
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header title={t('loading')} />
        <Loader />
        <BottomNav />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Header title="Error" />
        <div className="p-4 text-center text-red-500 mt-10">{t('error_occurred')}</div>
        <Button className="mx-auto block mt-4" onClick={() => navigate('/')}>{t('back')}</Button>
        <BottomNav />
      </div>
    );
  }

  if (!data) return null;

  // Use the derived fields from the API response
  const bestNetProfit = data.is_conversion_better
    ? data.best_conversion_net_profit
    : data.raw_sell_net_profit;

  const recommendedLabel = data.is_conversion_better ? t('convert') : t('sell_raw');

  // Find the conversion option to navigate to
  const conversionOption = data.options.find(o => o.option_type !== 'sell_raw');
  const rawOption = data.options.find(o => o.option_type === 'sell_raw');

  return (
    <div className="min-h-screen pb-20 bg-gray-50">
      <Header title="Analysis Results" />
      <main className="p-4 space-y-4 max-w-lg mx-auto">

        {/* Recommendation Banner */}
        <div className="bg-green-600 rounded-xl text-white p-5 shadow-lg mb-4">
          <h2 className="text-xs uppercase tracking-widest font-bold opacity-80 mb-2">
            🎯 {t('recommendation')}
          </h2>
          <p className="text-xl font-bold mb-3">{recommendedLabel}</p>
          <div className="bg-white/20 p-3 rounded-lg text-sm flex justify-between items-center">
            <span>{t('net_profit')}</span>
            <span className="font-bold text-base">{formatCurrency(bestNetProfit)}</span>
          </div>
        </div>

        {/* Options Comparison Table */}
        <Card className="p-4">
          <h3 className="font-bold text-gray-800 mb-3">{t('all_options')}</h3>
          <div className="overflow-x-auto rounded-xl border border-gray-200">
            <table className="min-w-full text-left bg-white text-sm">
              <thead className="bg-gray-50 border-b">
                <tr>
                  <th className="p-3 font-semibold text-gray-700">{t('col_option')}</th>
                  <th className="p-3 font-semibold text-gray-700">{t('net_profit')}</th>
                  <th className="p-3 font-semibold text-gray-700">{t('col_time')}</th>
                </tr>
              </thead>
              <tbody>
                {data.options.map((opt, i) => (
                  <tr
                    key={opt.option_type}
                    className={`border-b ${opt.option_type === data.best_option ? 'bg-green-50' : ''}`}
                  >
                    <td className="p-3 font-medium">
                      {lang === 'hi' && opt.label_hi ? opt.label_hi : opt.label_en}
                      {opt.option_type === data.best_option && (
                        <span className="ml-1 text-xs text-green-700 font-bold">★ Best</span>
                      )}
                    </td>
                    <td className="p-3 font-bold text-green-700">{formatCurrency(opt.net_profit)}</td>
                    <td className="p-3 text-gray-600">{opt.time_to_money_days}d</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>

        {/* Carbon Impact */}
        {data.carbon_impact && (
          <Card className="p-4 bg-blue-50 border-blue-100">
            <h3 className="font-bold text-blue-900 mb-2">🌍 {t('carbon_impact')}</h3>
            <p className="text-sm text-blue-800">{lang === 'hi' ? data.carbon_impact.if_sold?.label_hi : data.carbon_impact.if_sold?.label_en}</p>
            <p className="text-xs text-blue-600 mt-1">{lang === 'hi' ? data.carbon_impact.equivalent_hi : data.carbon_impact.equivalent_en}</p>
          </Card>
        )}

        {/* Action Buttons */}
        <div className="grid grid-cols-2 gap-3 mt-4">
          <Button
            variant="outline"
            className="flex-col h-auto py-4"
            onClick={() => navigate('/buyers', { state: location.state })}
          >
            <span className="text-2xl mb-1">🏭</span>
            <span className="text-sm font-semibold">{t('see_buyers')}</span>
          </Button>

          <Button
            variant="outline"
            className="flex-col h-auto py-4"
            disabled={!conversionOption}
            onClick={() => {
              if (conversionOption) {
                const convType = conversionOption.option_type.replace('convert_', '');
                navigate(`/guide/${convType}`, { state: conversionOption });
              }
            }}
          >
            <span className="text-2xl mb-1">🛠️</span>
            <span className="text-sm font-semibold">{t('learn_convert')}</span>
          </Button>
        </div>

      </main>
      <BottomNav />
    </div>
  );
}
