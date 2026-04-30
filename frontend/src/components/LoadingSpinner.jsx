import React from 'react';

const LoadingSpinner = ({ size = 'medium', className = '' }) => {
  const sizeStyles = {
    small: 'h-4 w-4 border-2',
    medium: 'h-8 w-8 border-4',
    large: 'h-12 w-12 border-4',
  };
  
  return (
    <div className={`inline-block animate-spin rounded-full border-indigo-500 border-t-transparent ${sizeStyles[size]} ${className}`} />
  );
};

export default LoadingSpinner;
