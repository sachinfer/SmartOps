import React from 'react';

export function Button({ children, onClick, className }: { children: React.ReactNode, onClick?: () => void, className?: string }) {
  return (
    <button
      onClick={onClick}
      className={`bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 ${className || ''}`.trim()}
    >
      {children}
    </button>
  );
} 