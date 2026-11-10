'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/Navbar';
import { Hero } from '@/components/Hero';
import { PredictionForm } from '@/components/PredictionForm';
import { PredictionResult } from '@/components/PredictionResult';
import { MarketAnalytics } from '@/components/MarketAnalytics';
import { AboutSection } from '@/components/AboutSection';
import { Footer } from '@/components/Footer';
import { AlertCircle, RefreshCw } from 'lucide-react';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export default function Home() {
  const [activeSection, setActiveSection] = useState('hero');
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [predictionResult, setPredictionResult] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Check backend health on mount
  const checkBackendHealth = async () => {
    setApiStatus('checking');
    try {
      const res = await fetch(`${API_BASE_URL}/health`, { method: 'GET' });
      if (res.ok) {
        const data = await res.json();
        if (data.status === 'healthy') {
          setApiStatus('online');
          return;
        }
      }
      setApiStatus('offline');
    } catch (err) {
      setApiStatus('offline');
    }
  };

  useEffect(() => {
    checkBackendHealth();
  }, []);

  // Smooth scroll handler
  const handleNavigate = (sectionId: string) => {
    setActiveSection(sectionId);
    const element = document.getElementById(sectionId);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };

  const handlePredictionSuccess = (data: any) => {
    setPredictionResult(data);
    setErrorMessage(null);
    // Smooth scroll to result
    setTimeout(() => {
      const resultElem = document.getElementById('prediction-result-anchor');
      if (resultElem) {
        resultElem.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 150);
  };

  return (
    <div className="min-h-screen bg-navy-900 text-slate-100 flex flex-col justify-between">
      {/* Top Navbar */}
      <Navbar
        activeSection={activeSection}
        onNavigate={handleNavigate}
        apiStatus={apiStatus}
      />

      <main className="flex-grow">
        {/* Section 1: Hero */}
        <div id="hero">
          <Hero
            onPredictClick={() => handleNavigate('predict')}
            onAnalyticsClick={() => handleNavigate('analytics')}
          />
        </div>

        {/* Backend Warning Banner if offline */}
        {apiStatus === 'offline' && (
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
            <div className="bg-amber-500/10 border border-amber-500/30 rounded-2xl p-4 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-amber-300">
              <div className="flex items-center gap-3">
                <AlertCircle size={20} className="shrink-0 text-amber-400" />
                <div>
                  <strong>Backend Offline Notice:</strong> FastAPI backend is not reachable at{' '}
                  <code className="bg-navy-950 px-2 py-0.5 rounded text-amber-200">{API_BASE_URL}</code>.
                  To launch the local backend, run:{' '}
                  <code className="bg-navy-950 px-2 py-0.5 rounded text-white font-mono">
                    python -m uvicorn backend.main:app --port 8000
                  </code>
                </div>
              </div>
              <button
                onClick={checkBackendHealth}
                className="inline-flex items-center gap-1.5 bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 px-3 py-1.5 rounded-lg font-semibold transition-colors shrink-0"
              >
                <RefreshCw size={14} />
                <span>Retry Connection</span>
              </button>
            </div>
          </div>
        )}

        {/* Section 2: Property Prediction Studio */}
        <section id="predict" className="py-16 border-t border-white/5 scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <span className="text-xs font-bold text-gold-400 uppercase tracking-widest block mb-2">
                ESTATIQ Real-Time Valuation Studio
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight serif-font">
                Estimate Property Selling Price
              </h2>
              <p className="text-slate-400 text-sm mt-3">
                Provide architectural, geographic, and amenity parameters to generate an accurate price prediction.
              </p>
            </div>

            {/* Error Message Box */}
            {errorMessage && (
              <div className="max-w-3xl mx-auto mb-8 bg-rose-500/10 border border-rose-500/30 text-rose-300 p-4 rounded-xl text-xs flex items-center gap-3">
                <AlertCircle size={18} className="shrink-0 text-rose-400" />
                <div>{errorMessage}</div>
              </div>
            )}

            {/* Prediction Form */}
            <PredictionForm
              apiBaseUrl={API_BASE_URL}
              onPredictionSuccess={handlePredictionSuccess}
              onError={setErrorMessage}
            />

            {/* Prediction Result Anchor & Component */}
            <div id="prediction-result-anchor">
              {predictionResult && (
                <PredictionResult
                  result={predictionResult}
                  onReset={() => setPredictionResult(null)}
                />
              )}
            </div>
          </div>
        </section>

        {/* Section 3: Market Analytics */}
        <section id="analytics" className="py-20 border-t border-white/5 bg-navy-950/40 scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <span className="text-xs font-bold text-gold-400 uppercase tracking-widest block mb-2">
                Market Telemetry &amp; Macro Indicators
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight serif-font">
                Housing Trends &amp; Model Benchmarks
              </h2>
              <p className="text-slate-400 text-sm mt-3">
                Comparative metrics detailing price trends across 10 major metropolitan cities and verified Scikit-learn validation results.
              </p>
            </div>

            <MarketAnalytics />
          </div>
        </section>

        {/* Section 4: About Project */}
        <section id="about" className="py-20 border-t border-white/5 scroll-mt-20">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <span className="text-xs font-bold text-gold-400 uppercase tracking-widest block mb-2">
                Engineering Documentation
              </span>
              <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight serif-font">
                About ESTATIQ System
              </h2>
              <p className="text-slate-400 text-sm mt-3">
                Decoupled microservice architecture integrating Next.js with Python FastAPI and Scikit-learn pipelines.
              </p>
            </div>

            <AboutSection />
          </div>
        </section>
      </main>

      {/* Footer */}
      <Footer />
    </div>
  );
}

