import React from 'react';
import { TransformMode } from '../types';

interface ModeSelectorProps {
  selectedMode: TransformMode;
  onModeChange: (mode: TransformMode) => void;
  disabled?: boolean;
}

const ModeSelector: React.FC<ModeSelectorProps> = ({ selectedMode, onModeChange, disabled = false }) => {
  const getButtonClasses = (mode: TransformMode) => {
    const baseClasses = 'w-1/2 py-2 px-4 text-sm font-semibold focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-slate-900 focus:ring-sky-500 transition-colors duration-200';
    if (selectedMode === mode) {
      return `${baseClasses} bg-sky-600 text-white shadow-md`;
    }
    return `${baseClasses} bg-slate-700 text-slate-300 hover:bg-slate-600`;
  };

  return (
    <div className={`w-full flex rounded-lg p-1 bg-slate-800 border-2 border-slate-700 ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}>
      <button
        onClick={() => onModeChange('reimagine')}
        disabled={disabled}
        className={`${getButtonClasses('reimagine')} rounded-l-md`}
        aria-pressed={selectedMode === 'reimagine'}
      >
        Reimagine
      </button>
      <button
        onClick={() => onModeChange('polish')}
        disabled={disabled}
        className={`${getButtonClasses('polish')} rounded-r-md`}
        aria-pressed={selectedMode === 'polish'}
      >
        Polish
      </button>
    </div>
  );
};

export default ModeSelector;
