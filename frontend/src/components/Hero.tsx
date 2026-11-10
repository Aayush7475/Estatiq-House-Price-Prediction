'use client';

import React from 'react';
import { ArrowRight, Sparkles, Building, TrendingUp, ShieldCheck } from 'lucide-react';

interface HeroProps {
  onPredictClick: () => void;
  onAnalyticsClick: () => void;
}

export const Hero: React.FC<HeroProps> = ({ onPredictClick, onAnalyticsClick }) => {
  return (
    <section className="relative pt-32 pb-20 md:pt-40 md:pb-28 overflow-hidden">
      {/* Background Glow Overlay */}
      <div className="absolute top-1/4 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-gold-500/10 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="max-w-3xl mx-auto text-center">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gold-500/10 border border-gold-500/30 text-gold-300 text-xs font-semibold uppercase tracking-wider mb-6 backdrop-blur-sm animate-fade-in">
            <Sparkles size={14} className="text-gold-400" />
            <span>Next-Gen Machine Learning PropTech</span>
          </div>

          {/* Main Headline */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white mb-6 leading-tight serif-font">
            Find the <span className="gold-gradient-text">True Value</span> of Your Property
          </h1>

          {/* Subtitle */}
          <p className="text-lg sm:text-xl text-slate-300 font-normal leading-relaxed mb-10 max-w-2xl mx-auto">
            ESTATIQ empowers property buyers, sellers, and investors with instant, mathematically verified valuations across India's top metropolitan markets using ensemble machine learning.
          </p>

          {/* Action Button Row */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-16">
            <button
              onClick={onPredictClick}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-gradient-to-r from-gold-400 via-gold-500 to-gold-600 hover:from-gold-300 hover:to-gold-500 text-navy-950 font-bold px-8 py-4 rounded-xl shadow-gold-glow hover:-translate-y-0.5 transition-all text-base"
            >
              <span>Predict Your Property Value</span>
              <ArrowRight size={18} />
            </button>

            <button
              onClick={onAnalyticsClick}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 bg-navy-800/80 hover:bg-navy-800 text-slate-200 hover:text-gold-400 border border-white/10 hover:border-gold-500/30 font-semibold px-7 py-4 rounded-xl transition-all text-base"
            >
              <span>Explore Market Analytics</span>
              <TrendingUp size={18} />
            </button>
          </div>

          {/* Trust Metric Badges */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-left">
            <div className="glass-surface p-4 rounded-xl">
              <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Metros Covered</div>
              <div className="text-xl font-extrabold text-white mt-1">10 Major Cities</div>
              <div className="text-[11px] text-gold-400 mt-0.5">80+ Micro-markets</div>
            </div>

            <div className="glass-surface p-4 rounded-xl">
              <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Model Accuracy</div>
              <div className="text-xl font-extrabold text-emerald-400 mt-1">0.8754 R²</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Random Forest Regressor</div>
            </div>

            <div className="glass-surface p-4 rounded-xl">
              <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Inference Speed</div>
              <div className="text-xl font-extrabold text-white mt-1">&lt; 50 ms</div>
              <div className="text-[11px] text-gold-400 mt-0.5">Sub-second calculations</div>
            </div>

            <div className="glass-surface p-4 rounded-xl">
              <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">Pipeline Safety</div>
              <div className="text-xl font-extrabold text-white mt-1">Zero Leakage</div>
              <div className="text-[11px] text-slate-400 mt-0.5">Strict ColumnTransformer</div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

