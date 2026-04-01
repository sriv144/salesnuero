"use client";

import { useState, useEffect } from "react";
import type { RunResult } from "@/lib/types";
import { runPipeline, listProspects } from "@/lib/api";

import Navbar from "@/components/Navbar";
import Sidebar from "@/components/Sidebar";
import ProspectForm from "@/components/ProspectForm";
import LoadingPipeline from "@/components/LoadingPipeline";
import ResultsDashboard from "@/components/ResultsDashboard";

import { LayoutDashboard, Sparkles } from "lucide-react";

type AppState = "idle" | "loading" | "result" | "error";

export default function Home() {
  const [state, setState]             = useState<AppState>("idle");
  const [history, setHistory]         = useState<RunResult[]>([]);
  const [activeResult, setActiveResult] = useState<RunResult | null>(null);
  const [errorMsg, setErrorMsg]       = useState("");
  const [loadingInfo, setLoadingInfo] = useState({ name: "", company: "" });

  /* Load prospect history on mount */
  useEffect(() => {
    listProspects()
      .then((results) => {
        setHistory(results);
        if (results.length > 0) {
          setActiveResult(results[results.length - 1]);
          setState("result");
        }
      })
      .catch(() => {}); // backend may not be running yet
  }, []);

  const activeKey = activeResult
    ? `${activeResult.prospect_name}::${activeResult.company_name}`
    : null;

  const handleRun = async (name: string, company: string) => {
    setState("loading");
    setLoadingInfo({ name, company });
    setErrorMsg("");
    try {
      const response = await runPipeline({ prospect_name: name, company_name: company });
      if (response.status === "success" && response.result) {
        const updated = [...history.filter(
          (r) => !(r.prospect_name === name && r.company_name === company)
        ), response.result];
        setHistory(updated);
        setActiveResult(response.result);
        setState("result");
      } else {
        setErrorMsg(response.error ?? "Unknown error");
        setState("error");
      }
    } catch (err) {
      setErrorMsg(err instanceof Error ? err.message : "Failed to reach backend");
      setState("error");
    }
  };

  const handleSelectHistory = (r: RunResult) => {
    setActiveResult(r);
    setState("result");
  };

  return (
    <div className="flex min-h-screen flex-col" style={{ background: "var(--bg-base)" }}>
      <Navbar />

      <div className="flex flex-1 overflow-hidden">
        {/* ── Sidebar ── */}
        <Sidebar
          history={history}
          activeKey={activeKey}
          onSelect={handleSelectHistory}
        />

        {/* ── Main content ── */}
        <main className="flex-1 overflow-y-auto">
          <div className="mx-auto max-w-4xl space-y-5 px-4 py-6 sm:px-6">

            {/* Page header */}
            <div className="flex items-center gap-2 mb-2">
              <LayoutDashboard size={16} style={{ color: "var(--text-muted)" }} />
              <h1 className="text-sm font-medium" style={{ color: "var(--text-muted)" }}>
                Intelligence Dashboard
              </h1>
            </div>

            {/* Prospect input form */}
            <ProspectForm onSubmit={handleRun} loading={state === "loading"} />

            {/* States */}
            {state === "idle" && history.length === 0 && (
              <EmptyState />
            )}

            {state === "loading" && (
              <LoadingPipeline
                prospectName={loadingInfo.name}
                companyName={loadingInfo.company}
              />
            )}

            {state === "error" && (
              <ErrorBanner message={errorMsg} onDismiss={() => setState("idle")} />
            )}

            {state === "result" && activeResult && (
              <ResultsDashboard result={activeResult} />
            )}
          </div>
        </main>
      </div>
    </div>
  );
}

/* ── Empty state ─────────────────────────────────────────── */
function EmptyState() {
  return (
    <div
      className="flex flex-col items-center gap-5 rounded-2xl py-16 text-center fade-in"
      style={{
        background: "linear-gradient(135deg, rgba(99,102,241,0.05) 0%, rgba(6,182,212,0.03) 100%)",
        border: "1px dashed var(--border)",
      }}
    >
      <div
        className="flex h-16 w-16 items-center justify-center rounded-2xl"
        style={{
          background: "linear-gradient(135deg,rgba(99,102,241,0.15),rgba(139,92,246,0.1))",
          border: "1px solid rgba(99,102,241,0.25)",
          boxShadow: "0 0 32px rgba(99,102,241,0.1)",
        }}
      >
        <Sparkles size={28} style={{ color: "var(--accent-light)" }} />
      </div>

      <div>
        <h2 className="text-lg font-semibold" style={{ color: "var(--text-primary)" }}>
          AI Buyer Psychology Intelligence
        </h2>
        <p className="mt-1.5 max-w-md text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
          Enter a prospect&apos;s name and company above. The 4-agent pipeline will
          research them, build a psychological profile, craft a tailored strategy,
          and generate a personalised 3-email sequence.
        </p>
      </div>

      <div className="flex flex-wrap justify-center gap-3 text-xs">
        {[
          { label: "Research Agent",   desc: "Tavily Search",      color: "#06b6d4" },
          { label: "Profiler Agent",   desc: "Big Five + DISC",    color: "#8b5cf6" },
          { label: "Strategist Agent", desc: "Benefit mapping",    color: "#6366f1" },
          { label: "Copywriter Agent", desc: "3-email sequence",   color: "#f59e0b" },
        ].map((step) => (
          <div
            key={step.label}
            className="flex items-center gap-2 rounded-lg px-3 py-2"
            style={{
              background: `${step.color}10`,
              border: `1px solid ${step.color}25`,
            }}
          >
            <span className="h-1.5 w-1.5 rounded-full" style={{ background: step.color }} />
            <span style={{ color: "var(--text-secondary)" }}>
              <span className="font-medium" style={{ color: step.color }}>{step.label}</span>
              {" · "}
              {step.desc}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}

/* ── Error banner ────────────────────────────────────────── */
function ErrorBanner({ message, onDismiss }: { message: string; onDismiss: () => void }) {
  return (
    <div
      className="flex items-start gap-3 rounded-xl px-5 py-4 fade-in"
      style={{ background: "rgba(239,68,68,0.08)", border: "1px solid rgba(239,68,68,0.25)" }}
    >
      <div
        className="mt-0.5 flex h-6 w-6 shrink-0 items-center justify-center rounded-full text-xs font-bold"
        style={{ background: "rgba(239,68,68,0.15)", color: "var(--danger)" }}
      >
        !
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium" style={{ color: "var(--danger)" }}>Pipeline error</p>
        <p className="mt-0.5 text-xs font-mono" style={{ color: "var(--text-secondary)" }}>{message}</p>
        <p className="mt-1 text-xs" style={{ color: "var(--text-muted)" }}>
          Make sure the backend is running: <code className="font-mono">uvicorn app.main:app --reload --port 8000</code>
        </p>
      </div>
      <button
        onClick={onDismiss}
        className="text-xs px-2 py-1 rounded"
        style={{ color: "var(--text-muted)", background: "var(--bg-surface)" }}
      >
        Dismiss
      </button>
    </div>
  );
}
