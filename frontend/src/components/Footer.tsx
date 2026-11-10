'use client';

import React from 'react';
import { ArrowUp } from 'lucide-react';

export const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="mt-28 border-t border-white/10 bg-navy-950 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-6 pb-8 border-b border-white/5">
          {/* Brand */}
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-gold-400 to-gold-600 flex items-center justify-center font-extrabold text-navy-950 text-lg shadow-gold-glow">
              E
            </div>
            <div>
              <span className="text-lg font-extrabold tracking-widest text-white uppercase block leading-none">
                ESTATIQ
              </span>
              <span className="text-[10px] text-gold-400 tracking-[0.2em] font-semibold uppercase block mt-1">
                Real Estate Valuation Platform
              </span>
            </div>
          </div>

          {/* Tagline */}
          <p className="text-xs text-slate-400 text-center md:text-right max-w-md">
            Next.js &amp; Python FastAPI production deployment powered by Scikit-learn Random Forest regression.
          </p>
        </div>

        {/* Bottom Credits & Back to Top */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-8 text-xs text-slate-500">
          <div>
            &copy; {new Date().getFullYear()} ESTATIQ Technologies. Computer Science &amp; Engineering Academic Submission.
          </div>

          <div className="flex items-center gap-4">
            <span>Next.js • FastAPI • Scikit-learn</span>
            <button
              onClick={scrollToTop}
              className="p-2 rounded-lg bg-navy-900 hover:bg-navy-800 text-slate-400 hover:text-gold-400 transition-colors"
              title="Back to Top"
            >
              <ArrowUp size={16} />
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

