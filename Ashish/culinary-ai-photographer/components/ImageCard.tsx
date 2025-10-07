import React from 'react';
import Spinner from './Spinner';
import PhotoIcon from './icons/PhotoIcon';
import SparklesIcon from './icons/SparklesIcon';

interface ImageCardProps {
  title: string;
  imageUrl: string | null;
  isLoading?: boolean;
  isResult?: boolean;
  loadingText?: string;
  onClick?: () => void;
}

const ImageCard: React.FC<ImageCardProps> = ({ title, imageUrl, isLoading = false, isResult = false, loadingText = "Generating...", onClick }) => {
  const Icon = isResult ? SparklesIcon : PhotoIcon;

  const cardContent = (
    <>
      {isLoading && (
        <div className="absolute inset-0 bg-black bg-opacity-60 flex flex-col items-center justify-center z-10">
          <Spinner />
          <p className="mt-4 text-slate-300">{loadingText}</p>
        </div>
      )}
      {imageUrl ? (
        <img src={imageUrl} alt={title} className="w-full h-full object-cover" />
      ) : (
        !isLoading && (
          <div className="text-slate-500 flex flex-col items-center">
            <Icon className="w-16 h-16" />
            <p className="mt-2 text-sm">{isResult ? "AI-generated image will appear here" : "Your uploaded image will appear here"}</p>
          </div>
        )
      )}
    </>
  );

  return (
    <div className="w-full">
      <h3 className="text-lg font-semibold text-sky-300 mb-2 flex items-center gap-2">
        <Icon className="w-6 h-6" />
        {title}
      </h3>
      <div 
        className={`aspect-square w-full bg-slate-800 rounded-lg shadow-lg flex items-center justify-center overflow-hidden relative border-2 border-slate-700 ${onClick && imageUrl ? 'cursor-pointer transition-transform duration-200 hover:scale-[1.02]' : ''}`}
        onClick={onClick}
        onKeyDown={(e) => onClick && e.key === 'Enter' && onClick()}
        role={onClick ? "button" : undefined}
        tabIndex={onClick ? 0 : -1}
        aria-label={onClick ? `Enlarge ${title}` : title}
      >
        {cardContent}
      </div>
    </div>
  );
};

export default ImageCard;