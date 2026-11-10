'use client';

import React, { useState, useEffect } from 'react';
import { Building2, Activity, ShieldCheck, Menu, X } from 'lucide-react';

interface NavbarProps {
  activeSection: string;
  onNavigate: (sectionId: string) => void;
  apiStatus: 'checking' | 'online' | 'offline';
}

export const Navbar: React.FC<NavbarProps> = ({ activeSection, onNavigate, apiStatus }) => {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navItems = [
    { id: 'hero', label: 'Home' },
    { id: 'predict', label: 'Predict Price' },
    { id: 'analytics', label: 'Market Analytics' },
    { id: 'about', label: 'About' },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-navy-950/90 backdrop-blur-md border-b border-gold-500/15 py-3 shadow-lg'
          : 'bg-transparent py-5'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between">
          {/* Brand Logo */}
          <div
            onClick={() => onNavigate('hero')}
            className="flex items-center gap-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-gold-400 via-gold-500 to-gold-600 flex items-center justify-center font-extrabold text-navy-950 text-xl shadow-gold-glow group-hover:scale-105 transition-transform">
              E
            </div>
            <div>
              <span className="text-xl font-extrabold tracking-widest text-white uppercase block leading-none">
                ESTATIQ
              </span>
              <span className="text-[10px] text-gold-400 tracking-[0.2em] font-semibold uppercase block mt-1">
                AI Valuation Engine
              </span>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center gap-1 bg-navy-900/60 p-1.5 rounded-full border border-white/5 backdrop-blur-md">
            {navItems.map((item) => (
              <button
                key={item.id}
                onClick={() => onNavigate(item.id)}
                className={`px-5 py-2 rounded-full text-sm font-semibold transition-all duration-200 ${
                  activeSection === item.id
                    ? 'bg-gradient-to-r from-gold-400 to-gold-500 text-navy-950 shadow-sm'
                    : 'text-slate-300 hover:text-white hover:bg-white/5'
                }`}
              >
                {item.label}
              </button>
            ))}
          </nav>

          {/* Right Header Status Widget */}
          <div className="hidden lg:flex items-center gap-4">
            <div className="flex items-center gap-2 bg-navy-800/80 px-3.5 py-1.5 rounded-full border border-white/10 text-xs">
              <span
                className={`w-2 h-2 rounded-full ${
                  apiStatus === 'online'
                    ? 'bg-emerald-400 animate-pulse'
                    : apiStatus === 'offline'
                    ? 'bg-rose-500'
                    : 'bg-amber-400 animate-ping'
                }`}
              />
              <span className="text-slate-400 font-medium">
                {apiStatus === 'online'
                  ? 'ML Engine Online'
                  : apiStatus === 'offline'
                  ? 'API Offline'
                  : 'Connecting...'}
              </span>
            </div>

            <button
              onClick={() => onNavigate('predict')}
              className="bg-gold-500 hover:bg-gold-400 text-navy-950 text-xs font-bold uppercase tracking-wider px-4 py-2.5 rounded-lg shadow-gold-glow hover:-translate-y-0.5 transition-all"
            >
              Get Valuation
            </button>
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-slate-300 hover:text-white p-2"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Drawer */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-navy-950/95 border-b border-gold-500/20 px-4 pt-3 pb-6 space-y-3 mt-3 backdrop-blur-xl">
          {navItems.map((item) => (
            <button
              key={item.id}
              onClick={() => {
                onNavigate(item.id);
                setMobileMenuOpen(false);
              }}
              className="block w-full text-left px-4 py-2.5 rounded-lg text-sm font-semibold text-slate-300 hover:text-white hover:bg-navy-800"
            >
              {item.label}
            </button>
          ))}
          <div className="pt-2">
            <button
              onClick={() => {
                onNavigate('predict');
                setMobileMenuOpen(false);
              }}
              className="w-full bg-gold-500 text-navy-950 font-bold py-2.5 rounded-lg text-sm uppercase tracking-wider"
            >
              Get Valuation
            </button>
          </div>
        </div>
      )}
    </header>
  );
};

