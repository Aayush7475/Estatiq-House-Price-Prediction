'use client';

import React, { useState, useEffect } from 'react';
import { MapPin, Home, Maximize2, Layers, Shield, Sparkles, Loader2, AlertCircle } from 'lucide-react';

interface PredictionFormProps {
  apiBaseUrl: string;
  onPredictionSuccess: (data: any) => void;
  onError: (msg: string | null) => void;
}

const DEFAULT_OPTIONS = {
  cities: ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata', 'Ahmedabad', 'Jaipur', 'Lucknow'],
  localities: {
    Mumbai: ['Andheri West', 'Bandra', 'Powai', 'Thane', 'Navi Mumbai', 'Goregaon', 'Malad', 'Borivali'],
    Delhi: ['Dwarka', 'Rohini', 'Saket', 'Vasant Kunj', 'Lajpat Nagar', 'Noida', 'Gurgaon', 'Greater Noida'],
    Bangalore: ['Whitefield', 'Electronic City', 'Koramangala', 'HSR Layout', 'Marathahalli', 'Sarjapur Road', 'Yelahanka', 'Bannerghatta Road'],
    Hyderabad: ['Gachibowli', 'Kondapur', 'Madhapur', 'Kukatpally', 'Miyapur', 'Secunderabad', 'Begumpet', 'LB Nagar'],
    Chennai: ['Adyar', 'Velachery', 'OMR', 'Anna Nagar', 'T Nagar', 'Porur', 'Tambaram', 'Sholinganallur'],
    Pune: ['Hinjewadi', 'Kharadi', 'Wakad', 'Baner', 'Viman Nagar', 'Hadapsar', 'Kothrud', 'Pimpri-Chinchwad'],
    Kolkata: ['Salt Lake', 'New Town', 'Alipore', 'Dum Dum', 'Howrah', 'Garia', 'Rajarhat', 'Behala'],
    Ahmedabad: ['SG Highway', 'Prahlad Nagar', 'Vastrapur', 'Bopal', 'Satellite', 'Chandkheda', 'Maninagar', 'Navrangpura'],
    Jaipur: ['Vaishali Nagar', 'Malviya Nagar', 'Mansarovar', 'Jagatpura', 'C-Scheme', 'Tonk Road', 'Pratap Nagar', 'Sirsi Road'],
    Lucknow: ['Gomti Nagar', 'Hazratganj', 'Aliganj', 'Indira Nagar', 'Vikas Nagar', 'Jankipuram', 'Mahanagar', 'Alambagh']
  } as Record<string, string[]>,
  property_types: ['Apartment', 'Independent House', 'Villa', 'Builder Floor'],
  furnishing_statuses: ['Furnished', 'Semi-Furnished', 'Unfurnished'],
  bhk_range: [1, 5],
  bathroom_range: [1, 6],
  area_range: [400, 4000],
  floor_range: [0, 30],
  parking_range: [0, 3],
};

export const PredictionForm: React.FC<PredictionFormProps> = ({
  apiBaseUrl,
  onPredictionSuccess,
  onError,
}) => {
  const [options, setOptions] = useState(DEFAULT_OPTIONS);
  const [loading, setLoading] = useState(false);
  const [fetchingOptions, setFetchingOptions] = useState(true);

  // Form State
  const [city, setCity] = useState('Mumbai');
  const [locality, setLocality] = useState('Andheri West');
  const [propertyType, setPropertyType] = useState('Apartment');
  const [bhk, setBhk] = useState(2);
  const [bathrooms, setBathrooms] = useState(2);
  const [superBuiltupArea, setSuperBuiltupArea] = useState(1100);
  const [carpetArea, setCarpetArea] = useState(825);
  const [propertyAge, setPropertyAge] = useState(4);
  const [furnishingStatus, setFurnishingStatus] = useState('Semi-Furnished');
  const [floorNo, setFloorNo] = useState(5);
  const [totalFloors, setTotalFloors] = useState(18);
  const [parking, setParking] = useState(1);
  const [lift, setLift] = useState(1);
  const [gatedCommunity, setGatedCommunity] = useState(1);

  // Fetch live options from backend if available
  useEffect(() => {
    const fetchOptions = async () => {
      try {
        const res = await fetch(`${apiBaseUrl}/model-info`);
        if (res.ok) {
          const data = await res.json();
          if (data.supported_options) {
            setOptions(data.supported_options);
          }
        }
      } catch (err) {
        console.log('Using preloaded fallback options for input form.');
      } finally {
        setFetchingOptions(false);
      }
    };
    fetchOptions();
  }, [apiBaseUrl]);

  // Sync localities when city changes
  useEffect(() => {
    const locs = options.localities[city] || ['Central Corridor'];
    if (!locs.includes(locality)) {
      setLocality(locs[0] || 'Central Corridor');
    }
  }, [city, options.localities, locality]);

  // Adjust carpet area proportionately if built-up changes
  const handleSuperAreaChange = (val: number) => {
    setSuperBuiltupArea(val);
    setCarpetArea(Math.round(val * 0.75));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    onError(null);

    const payload = {
      city,
      locality,
      property_type: propertyType,
      bhk: Number(bhk),
      bathrooms: Number(bathrooms),
      super_builtup_area: Number(superBuiltupArea),
      carpet_area: Number(carpetArea),
      property_age: Number(propertyAge),
      furnishing_status: furnishingStatus,
      floor_no: Number(floorNo),
      total_floors: Number(totalFloors),
      parking: Number(parking),
      lift: Number(lift),
      gated_community: Number(gatedCommunity),
    };

    try {
      const res = await fetch(`${apiBaseUrl}/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        throw new Error(errorData.detail || `Server responded with status ${res.status}`);
      }

      const data = await res.json();
      onPredictionSuccess(data);
    } catch (err: any) {
      console.error('Prediction failed:', err);
      onError(
        err.message || 'Could not connect to FastAPI backend. Ensure the backend is running at ' + apiBaseUrl
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
      {/* Form Container (8 Cols) */}
      <div className="lg:col-span-8 bg-navy-850/80 rounded-2xl p-6 sm:p-8 border border-white/10 shadow-2xl backdrop-blur-xl">
        <div className="flex items-center justify-between pb-6 mb-6 border-b border-white/10">
          <div>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Sparkles className="text-gold-400" size={20} />
              <span>Valuation Studio Form</span>
            </h3>
            <p className="text-sm text-slate-400 mt-1">
              Configure property attributes to trigger real-time Random Forest inference.
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Section 1: Location & Archetype */}
          <div>
            <div className="text-xs font-bold text-gold-400 uppercase tracking-widest mb-3 flex items-center gap-2">
              <MapPin size={14} /> 1. Location & Property Archetype
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">City</label>
                <select
                  value={city}
                  onChange={(e) => setCity(e.target.value)}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500 transition-colors"
                >
                  {options.cities.map((c) => (
                    <option key={c} value={c} className="bg-navy-950 text-white">
                      {c}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Locality</label>
                <select
                  value={locality}
                  onChange={(e) => setLocality(e.target.value)}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500 transition-colors"
                >
                  {(options.localities[city] || []).map((loc) => (
                    <option key={loc} value={loc} className="bg-navy-950 text-white">
                      {loc}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Property Type</label>
                <select
                  value={propertyType}
                  onChange={(e) => setPropertyType(e.target.value)}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500 transition-colors"
                >
                  {options.property_types.map((t) => (
                    <option key={t} value={t} className="bg-navy-950 text-white">
                      {t}
                    </option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Space & Layout */}
          <div className="pt-4 border-t border-white/5">
            <div className="text-xs font-bold text-gold-400 uppercase tracking-widest mb-3 flex items-center gap-2">
              <Home size={14} /> 2. Space, Layout & Interior
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">BHK Bedrooms</label>
                <select
                  value={bhk}
                  onChange={(e) => {
                    const b = Number(e.target.value);
                    setBhk(b);
                    setBathrooms(Math.min(b + 1, 6));
                  }}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                >
                  {[1, 2, 3, 4, 5].map((num) => (
                    <option key={num} value={num} className="bg-navy-950 text-white">
                      {num} BHK
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Bathrooms</label>
                <input
                  type="number"
                  min="1"
                  max="6"
                  value={bathrooms}
                  onChange={(e) => setBathrooms(Number(e.target.value))}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Furnishing</label>
                <select
                  value={furnishingStatus}
                  onChange={(e) => setFurnishingStatus(e.target.value)}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                >
                  {options.furnishing_statuses.map((f) => (
                    <option key={f} value={f} className="bg-navy-950 text-white">
                      {f}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Area Sliders */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 bg-navy-900/50 p-4 rounded-xl border border-white/5">
              <div>
                <div className="flex justify-between items-center mb-1 text-xs">
                  <span className="text-slate-300 font-semibold">Super Built-Up Area</span>
                  <span className="text-gold-400 font-bold">{superBuiltupArea.toLocaleString()} sq.ft.</span>
                </div>
                <input
                  type="range"
                  min={options.area_range[0]}
                  max={options.area_range[1]}
                  step="50"
                  value={superBuiltupArea}
                  onChange={(e) => handleSuperAreaChange(Number(e.target.value))}
                  className="w-full accent-gold-500 cursor-pointer"
                />
              </div>

              <div>
                <div className="flex justify-between items-center mb-1 text-xs">
                  <span className="text-slate-300 font-semibold">Carpet Area</span>
                  <span className="text-gold-400 font-bold">{carpetArea.toLocaleString()} sq.ft.</span>
                </div>
                <input
                  type="range"
                  min={Math.round(superBuiltupArea * 0.5)}
                  max={Math.round(superBuiltupArea * 0.9)}
                  step="25"
                  value={carpetArea}
                  onChange={(e) => setCarpetArea(Number(e.target.value))}
                  className="w-full accent-gold-500 cursor-pointer"
                />
              </div>
            </div>
          </div>

          {/* Section 3: Elevation & Tower Specs */}
          <div className="pt-4 border-t border-white/5">
            <div className="text-xs font-bold text-gold-400 uppercase tracking-widest mb-3 flex items-center gap-2">
              <Layers size={14} /> 3. Elevation & Tower Specs
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Property Age</label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min="0"
                    max="30"
                    value={propertyAge}
                    onChange={(e) => setPropertyAge(Number(e.target.value))}
                    className="w-full accent-gold-500"
                  />
                  <span className="text-xs text-white font-bold w-12 text-right">{propertyAge} yr</span>
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Floor Level</label>
                <input
                  type="number"
                  min="0"
                  max="30"
                  value={floorNo}
                  onChange={(e) => setFloorNo(Number(e.target.value))}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Total Tower Floors</label>
                <input
                  type="number"
                  min={Math.max(1, floorNo)}
                  max="40"
                  value={totalFloors}
                  onChange={(e) => setTotalFloors(Number(e.target.value))}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Amenities & Security */}
          <div className="pt-4 border-t border-white/5">
            <div className="text-xs font-bold text-gold-400 uppercase tracking-widest mb-3 flex items-center gap-2">
              <Shield size={14} /> 4. Amenities & Security
            </div>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-center">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">Parking Spaces</label>
                <select
                  value={parking}
                  onChange={(e) => setParking(Number(e.target.value))}
                  className="w-full bg-navy-900 border border-white/15 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-gold-500"
                >
                  {[0, 1, 2, 3].map((p) => (
                    <option key={p} value={p} className="bg-navy-950 text-white">
                      {p} Covered Slot{p !== 1 ? 's' : ''}
                    </option>
                  ))}
                </select>
              </div>

              <div className="flex items-center gap-3 bg-navy-900/60 p-3 rounded-xl border border-white/5">
                <input
                  type="checkbox"
                  id="lift_check"
                  checked={lift === 1}
                  onChange={(e) => setLift(e.target.checked ? 1 : 0)}
                  className="w-4 h-4 rounded text-gold-500 focus:ring-gold-500 accent-gold-500"
                />
                <label htmlFor="lift_check" className="text-xs font-medium text-slate-200 cursor-pointer">
                  High-Speed Lift Access
                </label>
              </div>

              <div className="flex items-center gap-3 bg-navy-900/60 p-3 rounded-xl border border-white/5">
                <input
                  type="checkbox"
                  id="gated_check"
                  checked={gatedCommunity === 1}
                  onChange={(e) => setGatedCommunity(e.target.checked ? 1 : 0)}
                  className="w-4 h-4 rounded text-gold-500 focus:ring-gold-500 accent-gold-500"
                />
                <label htmlFor="gated_check" className="text-xs font-medium text-slate-200 cursor-pointer">
                  24/7 Gated Security
                </label>
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="pt-4">
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-gold-400 via-gold-500 to-gold-600 hover:from-gold-300 hover:to-gold-500 text-navy-950 font-bold py-4 rounded-xl text-base shadow-gold-glow hover:-translate-y-0.5 transition-all flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" size={20} />
                  <span>Computing Random Forest Valuation...</span>
                </>
              ) : (
                <>
                  <Sparkles size={18} />
                  <span>CALCULATE ESTIMATED PROPERTY VALUE</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>

      {/* Live Spec Sheet (4 Cols) */}
      <div className="lg:col-span-4 bg-navy-850/80 rounded-2xl p-6 border border-white/10 shadow-xl backdrop-blur-xl space-y-4">
        <h4 className="text-xs font-bold text-gold-400 uppercase tracking-widest pb-3 border-b border-white/10">
          Live Payload Preview
        </h4>

        <div className="space-y-2 text-xs">
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Location</span>
            <span className="text-white font-semibold">{locality}, {city}</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Property Type</span>
            <span className="text-white font-semibold">{propertyType}</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Configuration</span>
            <span className="text-white font-semibold">{bhk} BHK • {bathrooms} Bath</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Built-Up Area</span>
            <span className="text-white font-semibold">{superBuiltupArea.toLocaleString()} sq.ft.</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Carpet Area</span>
            <span className="text-white font-semibold">{carpetArea.toLocaleString()} sq.ft.</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Floor Elevation</span>
            <span className="text-white font-semibold">Floor {floorNo} of {totalFloors}</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Furnishing</span>
            <span className="text-white font-semibold">{furnishingStatus}</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Parking</span>
            <span className="text-white font-semibold">{parking} Dedicated Slot{parking !== 1 ? 's' : ''}</span>
          </div>
          <div className="flex justify-between py-1.5 border-b border-white/5">
            <span className="text-slate-400">Amenities</span>
            <span className="text-white font-semibold">
              {[lift ? 'Lift' : null, gatedCommunity ? 'Gated Security' : null].filter(Boolean).join(' • ') || 'None'}
            </span>
          </div>
        </div>

        <div className="p-3.5 bg-navy-900/60 rounded-xl border border-white/5 text-[11px] text-slate-400 leading-relaxed">
          🔒 <strong className="text-slate-300">Data Leakage Protection:</strong> The backend passes all inputs through a frozen Scikit-learn Pipeline with fitted OneHotEncoder and StandardScaler.
        </div>
      </div>
    </div>
  );
};

