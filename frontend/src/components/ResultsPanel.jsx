import React, { useState } from "react";

export default function ResultsPanel({ title, content, subtitle }) {
  const [copied, setCopied] = useState(false);

  const text =
    typeof content === "string" ? content : JSON.stringify(content, null, 2);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), 1200);
    } catch (e) {
      console.error("Copy failed", e);
    }
  };

  return (
    <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="text-lg font-bold text-white">{title}</h3>
          {subtitle ? (
            <p className="text-slate-400 text-sm mt-1">{subtitle}</p>
          ) : null}
        </div>

        <button
          onClick={copy}
          className="text-slate-200 text-sm bg-slate-700 hover:bg-slate-600 px-3 py-2 rounded"
          type="button"
        >
          {copied ? "Copied" : "Copy"}
        </button>
      </div>

      <pre className="mt-4 bg-slate-900 text-slate-100 p-4 rounded overflow-auto text-sm">
        <code>{text}</code>
      </pre>
    </div>
  );
}
