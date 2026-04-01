"use client";

import { useEffect, useState } from "react";
import { Search, Brain, Target, Mail, CheckCircle2 } from "lucide-react";

const STEPS = [
  { icon: Search,       label: "Researcher",  desc: "Gathering public intelligence via Tavily Search…" },
  { icon: Brain,        label: "Profiler",    desc: "Analyzing psychology — Big Five & DISC mapping…" },
  { icon: Target,       label: "Strategist",  desc: "Matching product benefits to psychological profile…" },
  { icon: Mail,         label: "Copywriter",  desc: "Drafting 3-email personalized outreach sequence…" },
];

interface Props {
  prospectName: string;
  companyName: string;
}

export default function LoadingPipeline({ prospectName, companyName }: Props) {
  const [activeStep, setActiveStep] = useState(0);
  const [elapsed, setElapsed] = useState(0);

  // Advance steps every ~18s (pipeline takes ~60–90s total)
  useEffect(() => {
    const stepTimer = setInterval(() => {
      setActiveStep((s) => Math.min(s + 1, STEPS.length - 1));
    }, 18000);
    const clockTimer = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => { clearInterval(stepTimer); clearInterval(clockTimer); };
  }, []);

  const fmt = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`;

  return (
    <div className="panel fade-in flex flex-col items-center gap-8 py-12 px-6 text-center">
      {/* Prospect header */}
      <div>
        <p className="text-xs uppercase tracking-widest mb-2" style={{ color: "var(--text-muted)" }}>
          Analysing prospect
        </p>
        <h3 className="text-xl font-semibold" style={{ color: "var(--text-primary)" }}>
          {prospectName}
        </h3>
        <p className="text-sm mt-0.5" style={{ color: "var(--text-secondary)" }}>{companyName}</p>
      </div>

      {/* Step progress */}
      <div className="w-full max-w-md space-y-3">
        {STEPS.map((step, i) => {
          const done    = i < activeStep;
          const active  = i === activeStep;
          const pending = i > activeStep;
          const Icon    = step.icon;

          return (
            <div
              key={step.label}
              className="flex items-center gap-4 rounded-xl px-4 py-3 text-left transition-all duration-500"
              style={{
                background: active  ? "var(--accent-glow)"     :
                            done    ? "rgba(16,185,129,0.06)"   : "var(--bg-surface)",
                border:     active  ? "1px solid rgba(99,102,241,0.35)" :
                            done    ? "1px solid rgba(16,185,129,0.25)" : "1px solid var(--border-subtle)",
                opacity:    pending ? 0.4 : 1,
              }}
            >
              {/* Icon bubble */}
              <div
                className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg"
                style={{
                  background: done   ? "rgba(16,185,129,0.15)" :
                              active ? "rgba(99,102,241,0.2)"  : "var(--bg-card)",
                }}
              >
                {done ? (
                  <CheckCircle2 size={18} style={{ color: "var(--success)" }} />
                ) : (
                  <Icon
                    size={16}
                    style={{
                      color: active ? "var(--accent-light)" : "var(--text-muted)",
                      animation: active ? "pulse 2s ease-in-out infinite" : "none",
                    }}
                  />
                )}
              </div>

              {/* Text */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span
                    className="text-sm font-medium"
                    style={{ color: done ? "var(--success)" : active ? "var(--accent-light)" : "var(--text-muted)" }}
                  >
                    {step.label}
                  </span>
                  {active && (
                    <span className="text-xs px-1.5 py-0.5 rounded-full"
                      style={{ background: "rgba(99,102,241,0.15)", color: "var(--accent-light)", border: "1px solid rgba(99,102,241,0.25)" }}>
                      Running
                    </span>
                  )}
                  {done && (
                    <span className="text-xs" style={{ color: "var(--success)" }}>Done</span>
                  )}
                </div>
                {active && (
                  <p className="text-xs mt-0.5 truncate" style={{ color: "var(--text-muted)" }}>{step.desc}</p>
                )}
              </div>

              {/* Active spinner */}
              {active && (
                <div className="h-4 w-4 shrink-0 animate-spin rounded-full border-2 border-transparent"
                  style={{ borderTopColor: "var(--accent-light)", borderRightColor: "var(--accent-light)" }} />
              )}
            </div>
          );
        })}
      </div>

      {/* Elapsed */}
      <div className="flex items-center gap-2" style={{ color: "var(--text-muted)" }}>
        <span className="text-xs">Elapsed:</span>
        <span className="font-mono text-sm" style={{ color: "var(--text-secondary)" }}>{fmt(elapsed)}</span>
        <span className="text-xs">· Typical run: 60–90s</span>
      </div>

      {/* Progress bar */}
      <div className="w-full max-w-md">
        <div className="h-1 rounded-full overflow-hidden" style={{ background: "var(--bg-surface)" }}>
          <div
            className="h-full rounded-full transition-all duration-[18000ms] ease-linear"
            style={{
              width: `${((activeStep + 1) / STEPS.length) * 100}%`,
              background: "linear-gradient(90deg, var(--accent), var(--accent-cyan))",
            }}
          />
        </div>
        <p className="mt-2 text-xs text-center" style={{ color: "var(--text-muted)" }}>
          Step {activeStep + 1} of {STEPS.length}
        </p>
      </div>
    </div>
  );
}
