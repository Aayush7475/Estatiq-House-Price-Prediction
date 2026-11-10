import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ESTATIQ — AI-Powered Indian House Price Intelligence Platform',
  description: 'Enterprise-grade residential property valuation engine powered by Scikit-learn Machine Learning pipelines across top Indian metropolitan cities.',
  keywords: ['Indian Real Estate', 'House Price Prediction', 'Machine Learning', 'FastAPI', 'Next.js', 'PropTech'],
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className="bg-navy-900 text-slate-100 antialiased selection:bg-gold-500 selection:text-navy-950">
        {children}
      </body>
    </html>
  );
}

