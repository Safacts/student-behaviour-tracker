import React from 'react';

const Navigation = ({ currentPage }) => {
  const navItems = [
    { path: '/', label: 'Dashboard', id: 'dashboard' },
    { path: '/dashboard', label: 'Testing', id: 'testing' },
    { path: '/agents', label: 'Agents', id: 'agents' },
    { path: '/monitor', label: 'Monitor', id: 'monitor' },
    { path: '/docs', label: 'Integration', id: 'docs' },
    { path: '/chat', label: 'Chat', id: 'chat' },
    { path: '/api-builder', label: 'API Builder', id: 'api-builder' },
  ];

  const getPageBadge = (pageId) => {
    const badges = {
      dashboard: 'Original Dashboard',
      testing: 'Testing Dashboard',
      agents: 'Agentic AI',
      monitor: 'System Monitor',
      docs: 'API Documentation',
      chat: 'Conversational AI',
      'api-builder': 'API Builder',
    };
    return badges[pageId] || '';
  };

  return (
    <header className="bg-white shadow-sm border-b border-slate-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <h1 className="text-xl font-bold text-indigo-900">Student Behavior Analytics</h1>
            {currentPage && (
              <span className="ml-4 px-3 py-1 bg-indigo-100 text-indigo-800 text-xs font-semibold rounded-full">
                {getPageBadge(currentPage)}
              </span>
            )}
          </div>
          <nav className="flex space-x-8">
            {navItems.map((item) => (
              <a
                key={item.id}
                href={item.path}
                className={
                  currentPage === item.id
                    ? 'text-indigo-600 font-semibold border-b-2 border-indigo-600'
                    : 'text-slate-500 hover:text-indigo-600 transition-colors'
                }
              >
                {item.label}
              </a>
            ))}
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Navigation;
