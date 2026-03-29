import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import BottomNav from '../components/BottomNav';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Loader from '../components/ui/Loader';
import { useLanguage } from '../hooks/useLanguage';
import { useApi } from '../hooks/useApi';
import { buyerService } from '../services/buyerService';
import { formatCurrency } from '../utils/formatCurrency';
import { formatDistance } from '../utils/formatDistance';

export default function BuyerList() {
  const { t } = useLanguage();
  const location = useLocation();
  const navigate = useNavigate();
  const [buyers, setBuyers] = useState([]);
  
  const { execute: fetchBuyers, loading, error } = useApi(buyerService.getNearbyBuyers);

  useEffect(() => {
    if (!location.state) return navigate('/');
    
    // Only use fallback coords if there is absolutely no location data
    let lat = location.state.latitude;
    let lon = location.state.longitude;
    const pin = location.state.pincode;

    if (!lat && !pin) {
      lat = 30.73;
      lon = 76.77;
    }

    const params = {
      waste_type: location.state.waste_type,
      min_qty: parseFloat(location.state.quantity_kg),
      radius_km: 250 // Ensure reasonable coverage 
    };

    if (lat) params.lat = lat;
    if (lon) params.long = lon;
    if (pin) params.pincode = pin;

    fetchBuyers(params).then(res => setBuyers(res.buyers)).catch(() => {});
  }, [location.state, navigate, fetchBuyers]);

  return (
    <div className="min-h-screen pb-20 bg-gray-50">
      <Header title={t('nearby_buyers')} />
      <main className="p-4 space-y-4 max-w-lg mx-auto">
        <Button variant="outline" className="w-full justify-start py-2" onClick={() => navigate(-1)}>
          ← {t('back')}
        </Button>

        {loading && <Loader />}
        
        {/* Only show actual errors (like 500s or network drops) */}
        {error && !loading && <p className="text-red-500">{t('error_occurred')}</p>}

        {/* Empty state when NO FALLBACKS were even found */}
        {!loading && !error && buyers.length === 0 && (
          <Card className="p-8 text-center text-gray-500 bg-white">
            <div className="text-4xl mb-4">🏭</div>
            <p className="font-semibold text-gray-700 mb-2">{t('no_buyers_pilot')}</p>
          </Card>
        )}

        {/* Render Pilot Network Note if fallback array kicks in */}
        {!loading && buyers.length > 0 && buyers.some(b => b.is_fallback) && (
          <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg text-yellow-800 text-sm">
            <p className="font-bold mb-1">{t('no_buyers_radius')}</p>
            <p>{t('showing_distant')}</p>
          </div>
        )}

        {!loading && buyers.map(buyer => (
          <Card key={buyer.id} className={`p-5 border-l-4 ${buyer.is_fallback ? 'border-l-yellow-400' : 'border-l-green-500'} relative overflow-hidden`}>
            {buyer.is_fallback && (
               <span className="absolute top-0 right-0 bg-yellow-400 text-white text-[10px] uppercase font-bold px-2 py-1 rounded-bl-lg">
                 {t('pilot_network')}
               </span>
            )}
            <div className="flex justify-between items-start mb-2 mt-1">
              <div>
                <h3 className="font-bold text-lg text-gray-800 flex items-center gap-2">
                  {t(buyer.business_name)}
                  {buyer.is_verified && <span className="text-blue-500 text-sm" title="Verified">✓</span>}
                </h3>
                <p className="text-sm text-gray-500 capitalize leading-relaxed">
                  {t(buyer.buyer_type) !== buyer.buyer_type ? t(buyer.buyer_type) : buyer.buyer_type.replace('_', ' ')} <br/>
                  <span className="text-xs text-gray-400 font-medium">📍 {buyer.district ? `${t(buyer.district)}, ` : ''}{t(buyer.state)}</span>
                </p>
              </div>
              <div className="text-right mt-1">
                <span className={`${buyer.is_fallback ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'} text-xs font-bold px-2 py-1 rounded block`}>
                  {formatDistance(buyer.distance_km)}
                </span>
                <a 
                  href={`https://maps.google.com/?q=${buyer.latitude},${buyer.longitude}`} 
                  target="_blank" 
                  rel="noreferrer"
                  className="mt-2 text-xs text-blue-600 font-semibold block hover:underline"
                >
                  🗺️ {t('map')}
                </a>
              </div>
            </div>
            
            <div className="grid grid-cols-2 gap-4 my-4 mb-5 border-t border-b py-3 border-gray-100">
              <div>
                <p className="text-xs text-gray-500 uppercase">{t('offering_price')}</p>
                <p className="font-bold text-green-700">{formatCurrency(buyer.price_per_kg)}/kg</p>
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase">{t('pickup')}</p>
                <p className="font-medium text-gray-800">{buyer.provides_pickup ? t('pickup_provided') : t('pickup_self')}</p>
              </div>
            </div>

            <a 
              href={`tel:${buyer.phone}`}
              className={`mt-2 w-full flex items-center justify-center gap-2 ${buyer.is_fallback ? 'bg-yellow-500 hover:bg-yellow-600' : 'bg-green-600 hover:bg-green-700'} text-white py-3 rounded-lg font-bold transition`}
            >
              📞 {t('call_buyer')}
            </a>
          </Card>
        ))}
      </main>
      <BottomNav />
    </div>
  );
}
