'use client';

import React from 'react';
import { Award, CheckCircle2, AlertTriangle, ArrowUpRight, Building2, MapPin, Ruler, BedDouble } from 'lucide-react';

interface PredictionResultProps {
  result: {
    predicted_price: number;
    formatted_inr: string;
    price_lakhs: string;
    price_crores?: string;
    price_per_sqft: number;
    property_summary: {
      city: string;
      locality: string;
      property_type: string;
      bhk: number;
      bathrooms: number;
      super_builtup_area: number;
      carpet_area: number;
      property_age: number;
      furnishing_status: string;
      floor_no: number;
      total_floors: number;
      parking: number;
      lift: boolean;
      gated_community: boolean;
    };
    model_name: string;
    timestamp: string;
  };
  onReset: () => void;
}

export const PredictionResult: React.FC<PredictionResultProps> = ({ result, onReset }) => {
  const { property_summary: p } = result;

  return (
    <div className="bg-gradient-to-b from-navy-850 to-navy-900 border-2 border-gold-500 rounded-3xl p-6 sm:p-10 shadow-gold-card relative overflow-hidden animate-fade-in my-8">
      {/* Background Accent Glow */}
      <div className="absolute top-0 right-0 w-96 h-96 bg-gold-500/10 rounded-full blur-[100px] pointer-events-none" />

      {/* Verified Badge */}
      <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-white/10">
        <div className="inline-flex items-center gap-2 bg-gradient-to-r from-gold-400 to-gold-600 text-navy-950 font-extrabold text-xs uppercase tracking-widest px-4 py-1.5 rounded-full shadow-sm">
          <Award size={14} />
          <span>ESTATIQ Verified AI Valuation</span>
        </div>
        <div className="text-xs text-slate-400 flex items-center gap-1.5">
          <CheckCircle2 size={14} className="text-emerald-400" />
          <span>Inference Engine: {result.model_name}</span>
        </div>
      </div>

      {/* Main Price Headline */}
      <div className="text-center py-8">
        <div className="text-xs uppercase tracking-[0.2em] text-slate-400 font-bold mb-2">
          Estimated Fair Market Valuation
        </div>
        <div className="text-4xl sm:text-6xl font-extrabold text-white tracking-tight serif-font my-2">
          <span className="gold-gradient-text">{result.formatted_inr}</span>
        </div>

        {/* Currency Pill Chips */}
        <div className="flex flex-wrap items-center justify-center gap-3 mt-4">
          <span className="bg-gold-500/15 border border-gold-500/40 text-gold-300 font-bold px-4 py-1.5 rounded-xl text-sm">
            💰 {result.price_lakhs}
          </span>
          {result.price_crores && (
            <span className="bg-gold-500/15 border border-gold-500/40 text-gold-300 font-bold px-4 py-1.5 rounded-xl text-sm">
              💎 {result.price_crores}
            </span>
          )}
          <span className="bg-navy-800 border border-white/10 text-slate-300 font-semibold px-4 py-1.5 rounded-xl text-sm">
            📐 ₹{result.price_per_sqft.toLocaleString()}/sq.ft.
          </span>
        </div>
      </div>

      {/* Spec Tags Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-navy-950/60 p-4 rounded-2xl border border-white/5 my-6 text-xs">
        <div className="flex items-center gap-2.5">
          <MapPin size={16} className="text-gold-400 shrink-0" />
          <div>
            <span className="text-slate-400 block text-[10px]">Location</span>
            <span className="text-white font-semibold truncate block">{p.locality}, {p.city}</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Building2 size={16} className="text-gold-400 shrink-0" />
          <div>
            <span className="text-slate-400 block text-[10px]">Property Type</span>
            <span className="text-white font-semibold block">{p.property_type}</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <BedDouble size={16} className="text-gold-400 shrink-0" />
          <div>
            <span className="text-slate-400 block text-[10px]">Configuration</span>
            <span className="text-white font-semibold block">{p.bhk} BHK • {p.bathrooms} Bath</span>
          </div>
        </div>

        <div className="flex items-center gap-2.5">
          <Ruler size={16} className="text-gold-400 shrink-0" />
          <div>
            <span className="text-slate-400 block text-[10px]">Built-Up Area</span>
            <span className="text-white font-semibold block">{p.super_builtup_area.toLocaleString()} sq.ft.</span>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <div className="bg-navy-950/80 border border-white/10 rounded-xl p-4 flex items-start gap-3 text-xs text-slate-400 leading-relaxed">
        <AlertTriangle size={18} className="text-amber-400 shrink-0 mt-0.5" />
        <div>
          <strong className="text-slate-300">Valuation Notice:</strong> This valuation is derived mathematically using a trained Random Forest supervised regression model ($R^2 = 0.8754$). Actual transaction prices may vary depending on micro-market sentiment, building condition, interior finishes, and registration taxes.
        </div>
      </div>

      {/* Actions */}
      <div className="mt-6 flex justify-end">
        <button
          onClick={onReset}
          className="text-xs font-bold text-gold-400 hover:text-gold-300 uppercase tracking-wider flex items-center gap-1 px-4 py-2 rounded-lg hover:bg-white/5 transition-all"
        >
          <span>Calculate Another Property</span>
          <ArrowUpRight size={14} />
        </button>
      </div>
    </div>
  );
};

