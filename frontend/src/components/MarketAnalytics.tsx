'use client';

import React, { useState } from 'react';
import { BarChart3, TrendingUp, PieChart, Award, CheckCircle2 } from 'lucide-react';

export const MarketAnalytics: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'city' | 'bhk' | 'property' | 'models'>('city');

  // Verified Actual Dataset Statistics
  const cityData = [
    { city: 'Mumbai', avgLakhs: 248.5, barWidth: '100%', baseRate: '₹18,000/sq.ft.' },
    { city: 'Delhi', avgLakhs: 184.2, barWidth: '74%', baseRate: '₹14,000/sq.ft.' },
    { city: 'Bangalore', avgLakhs: 136.8, barWidth: '55%', baseRate: '₹10,000/sq.ft.' },
    { city: 'Chennai', avgLakhs: 121.4, barWidth: '49%', baseRate: '₹9,000/sq.ft.' },
    { city: 'Pune', avgLakhs: 114.7, barWidth: '46%', baseRate: '₹8,500/sq.ft.' },
    { city: 'Hyderabad', avgLakhs: 108.9, barWidth: '44%', baseRate: '₹8,000/sq.ft.' },
    { city: 'Kolkata', avgLakhs: 88.3, barWidth: '35%', baseRate: '₹6,500/sq.ft.' },
    { city: 'Ahmedabad', avgLakhs: 74.6, barWidth: '30%', baseRate: '₹5,500/sq.ft.' },
    { city: 'Jaipur', avgLakhs: 61.2, barWidth: '25%', baseRate: '₹4,500/sq.ft.' },
    { city: 'Lucknow', avgLakhs: 54.8, barWidth: '22%', baseRate: '₹4,000/sq.ft.' },
  ];

  const bhkData = [
    { bhk: '1 BHK', avgLakhs: 38.4, typicalSqft: '400 - 700 sq.ft.', share: '15%' },
    { bhk: '2 BHK', avgLakhs: 86.2, typicalSqft: '650 - 1,200 sq.ft.', share: '35%' },
    { bhk: '3 BHK', avgLakhs: 165.7, typicalSqft: '1,000 - 1,800 sq.ft.', share: '30%' },
    { bhk: '4 BHK', avgLakhs: 284.1, typicalSqft: '1,500 - 2,800 sq.ft.', share: '15%' },
    { bhk: '5 BHK', avgLakhs: 462.5, typicalSqft: '2,200 - 4,000 sq.ft.', share: '5%' },
  ];

  const propertyTypeData = [
    { type: 'Apartment', share: '54%', mult: '1.0x Baseline', desc: 'Standard multi-story residential flat' },
    { type: 'Builder Floor', share: '20%', mult: '0.9x Baseline', desc: 'Low-rise independent floor unit' },
    { type: 'Independent House', share: '16%', mult: '1.3x Baseline', desc: 'Standalone residential bungalow/plot' },
    { type: 'Luxury Villa', share: '10%', mult: '1.8x Baseline', desc: 'Gated luxury estate with private land' },
  ];

  const modelMetrics = [
    {
      metric: 'Test R² Score',
      lr: '0.8179',
      rf: '0.8754',
      advantage: '+5.75% Higher Variance Explained',
      winner: 'Random Forest',
    },
    {
      metric: 'Mean Absolute Error (MAE)',
      lr: '₹32,78,219',
      rf: '₹24,41,376',
      advantage: '₹8,36,843 Lower Error per Unit',
      winner: 'Random Forest',
    },
    {
      metric: 'Root Mean Squared Error (RMSE)',
      lr: '₹52,48,999',
      rf: '₹43,41,260',
      advantage: '₹9,07,739 Lower Extreme Penalties',
      winner: 'Random Forest',
    },
    {
      metric: 'Training R² Score',
      lr: '0.8347',
      rf: '0.9815',
      advantage: 'Superior Non-Linear Expressiveness',
      winner: 'Random Forest',
    },
  ];

  return (
    <div className="space-y-8">
      {/* KPI Stats Bar */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-navy-850/80 p-5 rounded-2xl border border-white/10 shadow-lg">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Average Ticket Size</div>
          <div className="text-2xl font-extrabold text-white mt-1">₹1.40 Crores</div>
          <div className="text-xs text-gold-400 mt-1 font-medium">₹140.28 Lakhs Mean</div>
        </div>

        <div className="bg-navy-850/80 p-5 rounded-2xl border border-white/10 shadow-lg">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Median Price</div>
          <div className="text-2xl font-extrabold text-white mt-1">₹1.07 Crores</div>
          <div className="text-xs text-slate-400 mt-1 font-medium">50th Percentile Benchmark</div>
        </div>

        <div className="bg-navy-850/80 p-5 rounded-2xl border border-white/10 shadow-lg">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Max Property Valuation</div>
          <div className="text-2xl font-extrabold text-white mt-1">₹15.65 Crores</div>
          <div className="text-xs text-gold-400 mt-1 font-medium">Bandra / South Delhi Villas</div>
        </div>

        <div className="bg-navy-850/80 p-5 rounded-2xl border border-white/10 shadow-lg">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Verified Dataset</div>
          <div className="text-2xl font-extrabold text-emerald-400 mt-1">5,000 Units</div>
          <div className="text-xs text-slate-400 mt-1 font-medium">10 Metros • 80 Localities</div>
        </div>
      </div>

      {/* Analytics Tabs & Display */}
      <div className="bg-navy-850/80 rounded-2xl p-6 sm:p-8 border border-white/10 shadow-2xl backdrop-blur-xl">
        {/* Tab Headers */}
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 mb-6 border-b border-white/10">
          <div>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <TrendingUp className="text-gold-400" size={20} />
              <span>Comparative Housing Intelligence</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Data-backed insights across geography, architectural typology, and algorithmic evaluations.
            </p>
          </div>

          <div className="flex bg-navy-900/80 p-1 rounded-xl border border-white/10 text-xs">
            <button
              onClick={() => setActiveTab('city')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                activeTab === 'city' ? 'bg-gold-500 text-navy-950 font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              City Ranking
            </button>
            <button
              onClick={() => setActiveTab('bhk')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                activeTab === 'bhk' ? 'bg-gold-500 text-navy-950 font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              BHK Curves
            </button>
            <button
              onClick={() => setActiveTab('property')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                activeTab === 'property' ? 'bg-gold-500 text-navy-950 font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Property Types
            </button>
            <button
              onClick={() => setActiveTab('models')}
              className={`px-4 py-2 rounded-lg font-semibold transition-all ${
                activeTab === 'models' ? 'bg-gold-500 text-navy-950 font-bold' : 'text-slate-400 hover:text-white'
              }`}
            >
              Model Benchmarks
            </button>
          </div>
        </div>

        {/* Tab Content: City Ranking */}
        {activeTab === 'city' && (
          <div className="space-y-4">
            <div className="text-xs text-slate-400 mb-2">
              Average residential property ticket size (₹ Lakhs) sorted by metropolitan tier:
            </div>
            {cityData.map((item, idx) => (
              <div key={item.city} className="space-y-1">
                <div className="flex justify-between items-center text-xs">
                  <span className="font-semibold text-white flex items-center gap-2">
                    <span className="text-gold-400 w-4 font-mono">{idx + 1}.</span> {item.city}
                  </span>
                  <div className="flex items-center gap-3">
                    <span className="text-slate-400 text-[11px]">{item.baseRate}</span>
                    <span className="text-gold-400 font-bold">₹{item.avgLakhs} Lakhs</span>
                  </div>
                </div>
                <div className="w-full bg-navy-900 rounded-full h-2.5 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 transition-all duration-500"
                    style={{ width: item.barWidth }}
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab Content: BHK Curves */}
        {activeTab === 'bhk' && (
          <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
            {bhkData.map((item) => (
              <div key={item.bhk} className="bg-navy-900/60 p-5 rounded-xl border border-white/5 space-y-2 text-center">
                <div className="text-sm font-extrabold text-gold-400">{item.bhk}</div>
                <div className="text-2xl font-bold text-white">₹{item.avgLakhs} L</div>
                <div className="text-[11px] text-slate-400">{item.typicalSqft}</div>
                <div className="inline-block bg-navy-800 text-slate-300 px-2 py-0.5 rounded text-[10px] font-semibold mt-2">
                  {item.share} of Database
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab Content: Property Types */}
        {activeTab === 'property' && (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {propertyTypeData.map((item) => (
              <div key={item.type} className="bg-navy-900/60 p-5 rounded-xl border border-white/5 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-base font-bold text-white">{item.type}</span>
                  <span className="text-xs bg-gold-500/10 text-gold-400 font-bold px-2 py-0.5 rounded">
                    {item.share}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
                <div className="text-xs text-gold-300 font-semibold pt-2 border-t border-white/5">
                  Multiplier: {item.mult}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Tab Content: Model Benchmarks */}
        {activeTab === 'models' && (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-white/10 text-slate-400 uppercase tracking-wider text-[11px]">
                  <th className="py-3 px-4">Evaluation Metric</th>
                  <th className="py-3 px-4">Linear Regression</th>
                  <th className="py-3 px-4">Random Forest (Selected)</th>
                  <th className="py-3 px-4">Quantitative Advantage</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {modelMetrics.map((row) => (
                  <tr key={row.metric} className="hover:bg-white/[0.02]">
                    <td className="py-3.5 px-4 font-semibold text-white">{row.metric}</td>
                    <td className="py-3.5 px-4 text-slate-400 font-mono">{row.lr}</td>
                    <td className="py-3.5 px-4 text-emerald-400 font-bold font-mono">{row.rf}</td>
                    <td className="py-3.5 px-4 text-gold-400 flex items-center gap-1.5 font-medium">
                      <CheckCircle2 size={13} className="text-gold-400" />
                      <span>{row.advantage}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

