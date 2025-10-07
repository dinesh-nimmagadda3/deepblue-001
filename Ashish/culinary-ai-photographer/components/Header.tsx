
import React from 'react';

const Header: React.FC = () => {
  return (
    <header className="text-center p-4 md:p-6">
      <h1 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-sky-400 to-emerald-400">
        MenuReady AI Photo Studio
      </h1>
      <p className="mt-3 text-lg text-slate-300 max-w-3xl mx-auto">
        Create irresistible photos for your menu, delivery apps, and social media in seconds. No expensive photoshoots required. Just upload a photo and let our AI do the rest.
      </p>
    </header>
  );
};

export default Header;