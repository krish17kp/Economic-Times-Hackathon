import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import BottomNav from '../components/BottomNav';
import Card from '../components/ui/Card';
import Input from '../components/ui/Input';
import Select from '../components/ui/Select';
import Button from '../components/ui/Button';
import WasteSelector from '../components/WasteSelector';
import { useLanguage } from '../hooks/useLanguage';
import { useGeolocation } from '../hooks/useGeolocation';
import { useApi } from '../hooks/useApi';
import { wasteService } from '../services/wasteService';

export default function Home() {
  const { t, lang } = useLanguage();
  const navigate = useNavigate();
  const { location, error: geoError, loading: geoLoading, getLocation } = useGeolocation();
  
  const [wasteTypes, setWasteTypes] = useState([]);
  const { execute: fetchWasteTypes } = useApi(wasteService.getWasteTypes);

  const [form, setForm] = useState({
    waste_type: '',
    quantity_kg: '',
    quality: 'dry',
    pincode: ''
  });

  const [errors, setErrors] = useState({});

  useEffect(() => {
    fetchWasteTypes().then(res => setWasteTypes(res.types)).catch(() => {});
  }, [fetchWasteTypes]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Explicit Validation to guide the user properly
    const newErrors = {};
    if (!form.waste_type) {
        newErrors.waste_type = lang === 'hi' ? "कृपया अवशेष का प्रकार चुनें!" : "Please select a waste type!";
    }
    if (!form.quantity_kg) {
        newErrors.quantity_kg = lang === 'hi' ? "कृपया मात्रा दर्ज करें!" : "Please enter quantity!";
    }
    
    if (Object.keys(newErrors).length > 0) {
        setErrors(newErrors);
        return;
    }
    
    // Clear errors if successful
    setErrors({});
    
    // Pass data through navigation state for the analysis (Results Page)
    navigate('/results', { 
      state: { 
        ...form, 
        latitude: location?.latitude, 
        longitude: location?.longitude 
      } 
    });
  };

  return (
    <div className="min-h-screen pb-36 bg-gray-50 relative z-10">
      <Header title={t('app_name')} />
      <div className="relative w-full sm:max-w-md md:max-w-lg mx-auto shadow-md rounded-b-3xl overflow-hidden bg-green-900 border-b-4 border-green-500 mb-2">
        <div 
          className="absolute inset-0 bg-cover bg-center opacity-80"
          style={{ backgroundImage: "url('/images/home-bg.jpeg')" }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent" />
        
        <div className="relative z-10 px-6 pt-16 pb-8 text-center flex flex-col justify-end min-h-[220px]">
          <h2 className="text-3xl font-black text-white mb-2 drop-shadow-lg tracking-wide leading-tight">
            {t('what_waste')}
          </h2>
          <p className="text-green-50 text-xs font-semibold uppercase tracking-widest drop-shadow-md">
            Find the best value for your crop residue
          </p>
        </div>
      </div>

      <main className="px-4 space-y-4 max-w-lg mx-auto relative z-20">

        <form onSubmit={handleSubmit} className="space-y-4">
          <Card className="space-y-4 p-5">
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1">{t('select_waste_type')}</label>
              <div className={errors.waste_type ? 'ring-2 ring-red-500 rounded-lg p-1 animate-pulse' : ''}>
                <WasteSelector 
                  wasteTypes={wasteTypes} 
                  value={form.waste_type} 
                  onChange={(v) => {
                      setForm({...form, waste_type: v});
                      setErrors(prev => ({...prev, waste_type: null}));
                  }} 
                />
              </div>
              {errors.waste_type && <p className="text-red-500 text-xs mt-1 font-bold">{errors.waste_type}</p>}
            </div>
            
            <div>
              <Input 
                label={t('quantity_kg')} 
                type="number" 
                min="100" 
                value={form.quantity_kg}
                onChange={(e) => {
                    setForm({...form, quantity_kg: e.target.value});
                    setErrors(prev => ({...prev, quantity_kg: null}));
                }}
                placeholder="e.g. 5000"
                required
              />
              {errors.quantity_kg && <p className="text-red-500 text-xs mt-1 font-bold">{errors.quantity_kg}</p>}
            </div>
            
            <Select 
              label={t('quality')}
              value={form.quality}
              onChange={(e) => setForm({...form, quality: e.target.value})}
              options={[
                { value: 'dry', label: t('quality_dry') },
                { value: 'semi_dry', label: t('quality_semi') },
                { value: 'wet', label: t('quality_wet') }
              ]}
            />
          </Card>

          <Card className="space-y-4 p-5">
            <div>
              <label className="text-sm font-medium text-gray-700 block mb-1">Your Location</label>
              <div className="flex gap-2 mb-2">
                <Button 
                  type="button" 
                  variant="secondary" 
                  onClick={getLocation}
                  disabled={geoLoading}
                  className="flex-1"
                >
                  📍 {geoLoading ? t('loading') : t('get_location')}
                </Button>
              </div>
              {location && <p className="text-sm text-green-600 mb-2">✅ {t('location_captured')}</p>}
              {geoError && <p className="text-sm text-red-500 mb-2">{geoError}</p>}
              
              <Input 
                placeholder={t('enter_pincode')}
                value={form.pincode}
                onChange={(e) => setForm({...form, pincode: e.target.value})}
                maxLength="6"
              />
            </div>
          </Card>

          <Button 
            type="submit" 
            className="w-full text-lg py-4 relative z-20 shadow-md transition-transform active:scale-[0.98]"
          >
            📊 {t('analyze')}
          </Button>
        </form>
      </main>
      <BottomNav />
    </div>
  );
}
