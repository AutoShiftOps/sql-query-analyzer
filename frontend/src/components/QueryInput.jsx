import React from 'react';
import { Send, Database } from 'lucide-react';

export default function QueryInput({ query, setQuery, dbType, setDbType, onAnalyze, loading }) {
  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <label className="block text-sm font-medium text-slate-300 mb-2">SQL Query</label>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Paste your SQL query here..."
        className="w-full h-40 bg-slate-900 text-white rounded border border-slate-600 p-3 font-mono text-sm focus:border-blue-500 focus:outline-none"
      />
      
      <div className="flex gap-4 mt-4">
        <div className="flex-1">
          <label className="block text-sm font-medium text-slate-300 mb-2">Database Type</label>
          <select
            value={dbType}
            onChange={(e) => setDbType(e.target.value)}
            className="w-full bg-slate-900 text-white rounded border border-slate-600 p-2 focus:border-blue-500 focus:outline-none"
          >
            <option value="postgresql">PostgreSQL</option>
            <option value="mysql">MySQL</option>
            <option value="sqlite">SQLite</option>
            <option value="sqlserver">SQL Server</option>
          </select>
        </div>
        
        <div className="flex items-end">
          <button
            onClick={onAnalyze}
            disabled={loading || !query.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white px-6 py-2 rounded font-medium flex items-center gap-2 transition"
          >
            <Send className="w-4 h-4" />
            {loading ? 'Analyzing...' : 'Analyze'}
          </button>
        </div>
      </div>
    </div>
  );
}
