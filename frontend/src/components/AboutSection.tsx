'use client';

import React from 'react';
import { Cpu, ShieldCheck, Database, Layers, ArrowRight } from 'lucide-react';

export const AboutSection: React.FC = () => {
  const techStack = [
    { category: 'Frontend', tech: 'Next.js 14, React 18, TypeScript, Tailwind CSS, Lucide Icons' },
    { category: 'Backend API', tech: 'Python 3.13, FastAPI, Uvicorn ASGI Server, Pydantic v2' },
    { category: 'Machine Learning', tech: 'Scikit-learn 1.9, RandomForestRegressor, ColumnTransformer' },
    { category: 'Data & Serialization', tech: 'Pandas 3.1, NumPy 2.5, Joblib Pipeline' },
    { category: 'Deployment Ready', tech: 'Vercel (Frontend Serverless) & Render (Backend Cloud)' },
  ];

  return (
    <div className="space-y-8">
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        {/* Left Side: Overview & ML Architecture */}
        <div className="lg:col-span-7 bg-navy-850/80 rounded-2xl p-6 sm:p-8 border border-white/10 shadow-2xl backdrop-blur-xl space-y-6">
          <div>
            <h3 className="text-xl font-bold text-white flex items-center gap-2">
              <Cpu className="text-gold-400" size={20} />
              <span>Project Architecture & Machine Learning Approach</span>
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Engineered as a full-stack, decoupled AI application adhering to modern enterprise design principles.
            </p>
          </div>

          <div className="space-y-4 text-xs sm:text-sm text-slate-300 leading-relaxed">
            <p>
              The Indian residential property market is characterized by extreme geographical price dispersion, non-linear floor rise premiums, and varying amenity valuations. <strong className="text-white">ESTATIQ</strong> resolves traditional pricing subjectivity by formulating real estate valuation as an empirical <strong>Supervised Machine Learning Regression</strong> problem.
            </p>

            <div className="p-4 bg-navy-900/70 rounded-xl border border-white/5 space-y-3">
              <h4 className="font-bold text-gold-400 text-xs uppercase tracking-wider">
                Algorithms Benchmark & Selection
              </h4>
              <ul className="space-y-2 text-xs">
                <li className="flex items-start gap-2">
                  <span className="text-gold-400 font-bold">•</span>
                  <span>
                    <strong className="text-white">Linear Regression (Baseline):</strong> Modeled prices parametrically via Ordinary Least Squares ($R^2 = 0.8179$, MAE = ₹32.78L).
                  </span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-gold-400 font-bold">•</span>
                  <span>
                    <strong className="text-white">Random Forest Regressor (Production Model):</strong> An ensemble of 100 decorrelated decision trees with feature sub-sampling. Attained an $R^2$ of <strong className="text-emerald-400">0.8754</strong> and reduced prediction error by <strong>25.5%</strong> (MAE = ₹24.41L).
                  </span>
                </li>
              </ul>
            </div>

            <p>
              The pipeline ensures <strong>Zero Data Leakage</strong>: missing values are imputed via median/mode, categoricals are one-hot encoded with <code className="text-gold-300 font-mono text-xs">handle_unknown='ignore'</code>, and numerical features are standardized strictly using parameters learned from the training distribution.
            </p>
          </div>
        </div>

        {/* Right Side: Tech Stack Matrix & Pipeline Flow */}
        <div className="lg:col-span-5 space-y-6">
          {/* Tech Stack Card */}
          <div className="bg-navy-850/80 rounded-2xl p-6 border border-white/10 shadow-xl backdrop-blur-xl">
            <h4 className="text-xs font-bold text-gold-400 uppercase tracking-widest pb-3 mb-4 border-b border-white/10 flex items-center gap-2">
              <Layers size={14} /> Technology Stack Matrix
            </h4>
            <div className="space-y-3 text-xs">
              {techStack.map((item) => (
                <div key={item.category} className="p-3 bg-navy-900/60 rounded-xl border border-white/5">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">{item.category}</div>
                  <div className="text-slate-200 font-medium mt-0.5">{item.tech}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Dataset Governance Card */}
          <div className="bg-navy-850/80 rounded-2xl p-6 border border-white/10 shadow-xl backdrop-blur-xl">
            <h4 className="text-xs font-bold text-gold-400 uppercase tracking-widest pb-3 mb-3 border-b border-white/10 flex items-center gap-2">
              <Database size={14} /> Dataset Governance
            </h4>
            <p className="text-xs text-slate-300 leading-relaxed">
              To guarantee zero reliance on external paywalled APIs and avoid publishing synthetic data as actual broker listings, the model is trained on an algorithmically generated 5,000-sample dataset reflecting genuine Indian real estate economic curves.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

