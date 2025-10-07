
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="text-center p-4 md:p-6">
      <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-400">
        Culinary AI Photographer
      </h1>
      <p className="mt-3 text-lg text-slate-300 max-w-2xl mx-auto">
        Turn your simple food photos into delicious, professional-grade masterpieces with the power of AI.
      </p>
    </header>
  );
};

export default Header;
