import React from "react";

export default function QueryInput({
  query, setQuery,
  dbType, setDbType,
  llmProvider, setLlmProvider,
  useLlm, setUseLlm,
  onAnalyze, loading,
  caps
}) {
  const openaiEnabled = !!caps?.providers?.openai;

  return (
    <div className="bg-slate-800 rounded-lg border border-slate-700 p-6">
      <label className="block text-sm font-medium text-slate-300 mb-2">SQL Query</label>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        className="w-full h-40 bg-slate-900 text-white rounded border border-slate-600 p-3 font-mono text-sm"
      />

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">Database</label>
          <select
            value={dbType}
            onChange={(e) => setDbType(e.target.value)}
            className="w-full bg-slate-900 text-white rounded border border-slate-600 p-2"
          >
            <option value="postgresql">PostgreSQL</option>
            <option value="mysql">MySQL</option>
            <option value="sqlite">SQLite</option>
            <option value="sqlserver">SQL Server</option>
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-300 mb-2">AI Provider</label>
          <select
            value={llmProvider}
            onChange={(e) => setLlmProvider(e.target.value)}
            className="w-full bg-slate-900 text-white rounded border border-slate-600 p-2"
          >
            <option value="huggingface">Hugging Face (default)</option>
            <option value="openai" disabled={!openaiEnabled}>
              OpenAI {openaiEnabled ? "" : "(not enabled on server)"}
            </option>
          </select>
        </div>

        <div className="flex items-end gap-3">
          <label className="text-slate-300 text-sm flex items-center gap-2">
            <input
              type="checkbox"
              checked={useLlm}
              onChange={(e) => setUseLlm(e.target.checked)}
            />
            Use AI insights
          </label>
        </div>
      </div>

      <button
        onClick={onAnalyze}
        disabled={loading || !query.trim()}
        className="mt-4 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-600 text-white px-6 py-2 rounded font-medium"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </div>
  );
}
