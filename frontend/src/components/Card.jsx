import React from 'react';

const Card = ({ children, className = '', variant = 'default', ...props }) => {
  const baseStyles = 'rounded-2xl shadow-sm border';
  
  const variantStyles = {
    default: 'bg-white border-slate-100',
    glass: 'bg-white/85 backdrop-blur-sm border-white/30',
    dark: 'bg-indigo-900 text-white border-indigo-800',
  };
  
  return (
    <div className={`${baseStyles} ${variantStyles[variant]} ${className}`} {...props}>
      {children}
    </div>
  );
};

export default Card;
