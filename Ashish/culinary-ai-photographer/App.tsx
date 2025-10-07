import React, { useState, useCallback, useRef } from 'react';
import { AppStatus, TransformMode } from './types';
import { transformFoodImage } from './services/geminiService';
import Header from './components/Header';
import ImageCard from './components/ImageCard';
import FileUpload from './components/FileUpload';
import SparklesIcon from './components/icons/SparklesIcon';
import DownloadIcon from './components/icons/DownloadIcon';
import ImageModal from './components/ImageModal';
import ModeSelector from './components/ModeSelector';


// Helper to convert file to base64
const fileToBase64 = (file: File): Promise<string> => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result as string);
    reader.onerror = (error) => reject(error);
  });
};

const App: React.FC = () => {
  const [originalImage, setOriginalImage] = useState<string | null>(null);
  const [originalMimeType, setOriginalMimeType] = useState<string>('');
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);
  const [status, setStatus] = useState<AppStatus>(AppStatus.IDLE);
  const [error, setError] = useState<string | null>(null);
  const [foodLabel, setFoodLabel] = useState<string>('');
  const [enlargedImage, setEnlargedImage] = useState<string | null>(null);
  const [transformMode, setTransformMode] = useState<TransformMode>('reimagine');
  
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = useCallback(async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setStatus(AppStatus.UPLOADING);
    handleClear();
    try {
      const dataUrl = await fileToBase64(file);
      setOriginalImage(dataUrl);
      setOriginalMimeType(file.type);
      setStatus(AppStatus.IDLE);
    } catch (err) {
      setError('Failed to read the selected file.');
      setStatus(AppStatus.ERROR);
    }
    if (event.target) {
      event.target.value = '';
    }
  }, []);
  
  const triggerFileUpload = () => {
    if (status !== AppStatus.PROCESSING) {
        fileInputRef.current?.click();
    }
  };

  const handleTransformClick = useCallback(async () => {
    if (!originalImage) {
      setError("Please upload an image first.");
      return;
    }

    setStatus(AppStatus.PROCESSING);
    setError(null);
    setGeneratedImage(null);

    try {
      const base64Data = originalImage.split(',')[1];
      const resultBase64 = await transformFoodImage(base64Data, originalMimeType, transformMode, foodLabel);
      const resultUrl = `data:image/jpeg;base64,${resultBase64}`;
      setGeneratedImage(resultUrl);
      setStatus(AppStatus.SUCCESS);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred.';
      setError(errorMessage);
      setStatus(AppStatus.ERROR);
    }
  }, [originalImage, originalMimeType, foodLabel, transformMode]);

  const handleClear = () => {
    setOriginalImage(null);
    setOriginalMimeType('');
    setGeneratedImage(null);
    setStatus(AppStatus.IDLE);
    setError(null);
    setFoodLabel('');
    if (fileInputRef.current) {
        fileInputRef.current.value = '';
    }
  };

  const handleDownload = () => {
    if (!generatedImage) return;
    const link = document.createElement('a');
    link.href = generatedImage;
    link.download = 'professional-food-photo.jpeg';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  const isProcessing = status === AppStatus.PROCESSING;

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center p-4">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        className="hidden"
        accept="image/png, image/jpeg, image/webp"
        disabled={isProcessing}
      />
      <Header />
      <main className="w-full max-w-6xl mx-auto flex-grow flex flex-col items-center justify-center">
        {error && (
          <div className="bg-red-500/20 border border-red-500 text-red-300 px-4 py-3 rounded-lg relative my-4 max-w-xl text-center" role="alert">
            <strong className="font-bold">Oops! </strong>
            <span className="block sm:inline">{error}</span>
          </div>
        )}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 w-full p-4">
          <div 
            className="cursor-pointer"
            onClick={triggerFileUpload}
            onKeyDown={(e) => e.key === 'Enter' && triggerFileUpload()}
            role="button"
            tabIndex={0}
            aria-label="Upload original food photo"
            >
            <ImageCard title="Original Food Photo" imageUrl={originalImage} />
          </div>
          <div>
            <ImageCard
              title="Professional AI Photo"
              imageUrl={generatedImage}
              isLoading={isProcessing}
              isResult={true}
              loadingText={`AI is creating your image...`}
              onClick={() => generatedImage && setEnlargedImage(generatedImage)}
            />
            {generatedImage && !isProcessing && (
              <button 
                onClick={handleDownload}
                className="w-full mt-4 bg-slate-700 hover:bg-slate-600 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center transition-colors duration-200"
              >
                <DownloadIcon className="w-5 h-5 mr-2" />
                Download Photo
              </button>
            )}
          </div>
        </div>
        <div className="w-full max-w-sm md:max-w-md mt-8 flex flex-col items-center gap-4">
          <div className="w-full flex items-stretch gap-4">
            <FileUpload onClick={triggerFileUpload} disabled={isProcessing} />
            <button
              onClick={handleClear}
              disabled={!originalImage && !generatedImage && status === AppStatus.IDLE}
              className="bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:text-slate-600 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center transition-colors duration-200"
              aria-label="Clear selection"
            >
              Clear
            </button>
          </div>
          <input
            type="text"
            value={foodLabel}
            onChange={(e) => setFoodLabel(e.target.value)}
            placeholder="Optional: Enter menu item name (e.g., Signature Angus Burger)"
            aria-label="Food label"
            className="w-full bg-slate-800 border-2 border-slate-700 text-white placeholder-slate-500 text-base rounded-lg focus:ring-sky-500 focus:border-sky-500 block p-3 transition-colors duration-200"
            disabled={isProcessing}
          />
          <ModeSelector selectedMode={transformMode} onModeChange={setTransformMode} disabled={isProcessing} />
          <button
            onClick={handleTransformClick}
            disabled={!originalImage || isProcessing}
            className="w-full bg-gradient-to-r from-sky-500 to-emerald-500 hover:from-sky-600 hover:to-emerald-600 disabled:from-slate-600 disabled:to-slate-700 disabled:cursor-not-allowed text-white font-bold py-4 px-4 rounded-lg flex items-center justify-center transition-all duration-300 transform hover:scale-105 disabled:scale-100 shadow-lg"
          >
            {isProcessing ? (
              'Creating...'
            ) : (
              <>
                <SparklesIcon className="w-5 h-5 mr-2" />
                Make it Professional
              </>
            )}
          </button>
        </div>
      </main>
      <footer className="text-center p-4 text-slate-500 text-sm">
        <p>Helping restaurants create beautiful menus.</p>
      </footer>
      {enlargedImage && (
        <ImageModal imageUrl={enlargedImage} onClose={() => setEnlargedImage(null)} />
      )}
    </div>
  );
};

export default App;