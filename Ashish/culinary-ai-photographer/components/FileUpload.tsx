import React from 'react';
import PhotoIcon from './icons/PhotoIcon';

interface FileUploadProps {
  onClick: () => void;
  disabled?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onClick, disabled = false }) => {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="w-full bg-slate-700 hover:bg-slate-600 disabled:bg-slate-800 disabled:cursor-not-allowed text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center transition-colors duration-200"
    >
      <PhotoIcon className="w-5 h-5 mr-2" />
      Upload Food Photo
    </button>
  );
};

export default FileUpload;