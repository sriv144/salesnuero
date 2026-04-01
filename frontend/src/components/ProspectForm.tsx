"use client";

import { useState } from "react";
import { Search, Building2, Sparkles, ArrowRight } from "lucide-react";

interface Props {
  onSubmit: (name: string, company: string) => void;
  loading: boolean;
}

export default function ProspectForm({ onSubmit, loading }: Props) {
  const [name, setName] = useState("");
  const [company, setCompany] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (name.trim() && company.trim() && !loading) {
      onSubmit(name.trim(), company.trim());
    }
  };

  const examples = [
    { name: "Sarah Chen", company: "Stripe" },
    { name: "Marcus Webb", company: "Salesforce" },
    { name: "VP of Engineering", company: "OpenAI" },
  ];

  return (
    <div className="panel p-6 fade-in">
      {/* Header */}
      <div className="mb-5 flex items-center gap-3">
        <div
          className="flex h-9 w-9 items-center justify-center rounded-lg"
          style={{ background: "var(--accent-glow)", border: "1px solid rgba(99,102,241,0.3)" }}
        >
          <Sparkles size={16} style={{ color: "var(--accent-light)" }} />
        </div>
        <div>
          <h2 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>
            New Prospect Analysis
          </h2>
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            4-agent pipeline · Research → Profile → Strategy → Emails
          </p>
        </div>
      </div>

      {/* Form */}
      <form onSubmit={handleSubmit} className="flex flex-col gap-4 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label className="mb-1.5 block text-xs font-medium" style={{ color: "var(--text-secondary)" }}>
            Prospect Name / Title
          </label>
          <div className="relative">
            <Search
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2"
              style={{ color: "var(--text-muted)" }}
            />
            <input
              className="input-dark w-full rounded-lg py-2.5 pl-9 pr-4 text-sm"
              placeholder="e.g. VP of Sales, Jane Smith…"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={loading}
              required
            />
          </div>
        </div>

        <div className="flex-1">
          <label className="mb-1.5 block text-xs font-medium" style={{ color: "var(--text-secondary)" }}>
            Company Name
          </label>
          <div className="relative">
            <Building2
              size={14}
              className="absolute left-3 top-1/2 -translate-y-1/2"
              style={{ color: "var(--text-muted)" }}
            />
            <input
              className="input-dark w-full rounded-lg py-2.5 pl-9 pr-4 text-sm"
              placeholder="e.g. Acme Corp, Stripe…"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
              disabled={loading}
              required
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={loading || !name.trim() || !company.trim()}
          className="btn-glow flex h-10 items-center gap-2 rounded-lg px-5 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-50"
          style={{ minWidth: "140px" }}
        >
          {loading ? (
            <>
              <span className="h-3.5 w-3.5 animate-spin rounded-full border-2 border-white/30 border-t-white" />
              Running…
            </>
          ) : (
            <>
              Run Pipeline
              <ArrowRight size={14} />
            </>
          )}
        </button>
      </form>

      {/* Example chips */}
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="text-xs" style={{ color: "var(--text-muted)" }}>Try:</span>
        {examples.map((ex) => (
          <button
            key={ex.name}
            onClick={() => { setName(ex.name); setCompany(ex.company); }}
            disabled={loading}
            className="rounded-full px-3 py-1 text-xs transition-all"
            style={{
              background: "var(--bg-surface)",
              border: "1px solid var(--border)",
              color: "var(--text-secondary)",
              cursor: loading ? "not-allowed" : "pointer",
            }}
          >
            {ex.name} @ {ex.company}
          </button>
        ))}
      </div>
    </div>
  );
}
