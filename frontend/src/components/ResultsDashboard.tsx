"use client";

import { useState } from "react";
import {
  Search, Brain, Target, Mail,
  ChevronDown, ChevronUp, User, Building2,
} from "lucide-react";
import type { RunResult } from "@/lib/types";
import PsychologyRadar from "./PsychologyRadar";
import EmailSequence from "./EmailSequence";

/* ── Section wrapper ─────────────────────────────────────── */
function Section({
  icon: Icon,
  title,
  subtitle,
  accent,
  defaultOpen = true,
  children,
}: {
  icon: React.ElementType;
  title: string;
  subtitle?: string;
  accent: string;
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);

  return (
    <div
      className="panel overflow-hidden"
      style={{ border: `1px solid var(--border)` }}
    >
      {/* Header */}
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-3 px-5 py-4 text-left transition-colors"
        style={{ borderBottom: open ? "1px solid var(--border-subtle)" : "none" }}
      >
        <div
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg"
          style={{ background: `${accent}18`, border: `1px solid ${accent}35` }}
        >
          <Icon size={15} style={{ color: accent }} />
        </div>
        <div className="flex-1">
          <h3 className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>{title}</h3>
          {subtitle && <p className="text-xs" style={{ color: "var(--text-muted)" }}>{subtitle}</p>}
        </div>
        {open
          ? <ChevronUp size={15} style={{ color: "var(--text-muted)" }} />
          : <ChevronDown size={15} style={{ color: "var(--text-muted)" }} />
        }
      </button>

      {/* Body */}
      {open && <div className="px-5 py-4">{children}</div>}
    </div>
  );
}

/* ── Markdown-ish renderer ───────────────────────────────── */
function RawText({ text }: { text: string }) {
  return (
    <div className="prose-sm space-y-2">
      {text.split("\n").map((line, i) => {
        if (!line.trim()) return <div key={i} className="h-2" />;
        if (line.startsWith("## "))
          return <h4 key={i} className="mt-3 text-sm font-semibold" style={{ color: "var(--accent-light)" }}>{line.slice(3)}</h4>;
        if (line.startsWith("# "))
          return <h3 key={i} className="mt-4 text-base font-bold" style={{ color: "var(--text-primary)" }}>{line.slice(2)}</h3>;
        if (line.startsWith("- ") || line.startsWith("* "))
          return (
            <div key={i} className="flex gap-2 text-sm">
              <span style={{ color: "var(--accent)" }}>·</span>
              <span style={{ color: "var(--text-secondary)" }}>{line.slice(2)}</span>
            </div>
          );
        if (/^\d+\./.test(line))
          return (
            <div key={i} className="flex gap-2 text-sm">
              <span className="font-mono shrink-0" style={{ color: "var(--accent-light)" }}>{line.match(/^\d+/)?.[0]}.</span>
              <span style={{ color: "var(--text-secondary)" }}>{line.replace(/^\d+\.\s*/, "")}</span>
            </div>
          );
        if (line.startsWith("**") && line.endsWith("**"))
          return <p key={i} className="text-sm font-semibold" style={{ color: "var(--text-primary)" }}>{line.slice(2, -2)}</p>;
        return <p key={i} className="text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>{line}</p>;
      })}
    </div>
  );
}

/* ── Main component ──────────────────────────────────────── */
interface Props { result: RunResult }

export default function ResultsDashboard({ result }: Props) {
  return (
    <div className="fade-in space-y-4">
      {/* Prospect header */}
      <div
        className="flex items-center gap-4 rounded-xl px-5 py-4"
        style={{
          background: "linear-gradient(135deg, rgba(99,102,241,0.08) 0%, rgba(6,182,212,0.05) 100%)",
          border: "1px solid rgba(99,102,241,0.2)",
        }}
      >
        <div
          className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-lg font-bold"
          style={{
            background: "linear-gradient(135deg,#6366f1,#8b5cf6)",
            boxShadow: "0 4px 14px rgba(99,102,241,0.35)",
            color: "#fff",
          }}
        >
          {result.prospect_name.charAt(0).toUpperCase()}
        </div>
        <div className="flex-1 min-w-0">
          <h2 className="text-base font-semibold truncate" style={{ color: "var(--text-primary)" }}>
            {result.prospect_name}
          </h2>
          <div className="flex items-center gap-1.5 mt-0.5">
            <Building2 size={12} style={{ color: "var(--text-muted)" }} />
            <span className="text-sm" style={{ color: "var(--text-secondary)" }}>{result.company_name}</span>
          </div>
        </div>
        <div className="flex flex-col items-end gap-1">
          <span
            className="rounded-full px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wide"
            style={{ background: "rgba(16,185,129,0.12)", color: "var(--success)", border: "1px solid rgba(16,185,129,0.25)" }}
          >
            Complete
          </span>
          <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>4 agents · 4 tasks</span>
        </div>
      </div>

      {/* Research */}
      <Section icon={Search} title="Prospect Research" subtitle="Public intelligence gathered via Tavily Search" accent="#06b6d4">
        {result.research_summary
          ? <RawText text={result.research_summary} />
          : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No research data returned.</p>
        }
      </Section>

      {/* Psychology */}
      <Section icon={Brain} title="Psychological Profile" subtitle="Big Five (OCEAN) scores + DISC behavioural type" accent="#8b5cf6">
        {result.profile_raw
          ? <>
              <PsychologyRadar profileRaw={result.profile_raw} />
              <details className="mt-4">
                <summary className="cursor-pointer text-xs" style={{ color: "var(--text-muted)" }}>
                  View raw profiler output
                </summary>
                <div className="mt-2 rounded-lg p-3" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)" }}>
                  <RawText text={result.profile_raw} />
                </div>
              </details>
            </>
          : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No profile data returned.</p>
        }
      </Section>

      {/* Strategy */}
      <Section icon={Target} title="Sales Strategy" subtitle="Top 3 value propositions ranked by psychological fit" accent="#6366f1">
        {result.strategy_brief
          ? <RawText text={result.strategy_brief} />
          : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No strategy data returned.</p>
        }
      </Section>

      {/* Emails */}
      <Section icon={Mail} title="Personalized Email Sequence" subtitle="3-email outreach calibrated to psychology & strategy" accent="#f59e0b">
        {result.emails_raw
          ? <EmailSequence emailsRaw={result.emails_raw} />
          : <p className="text-sm" style={{ color: "var(--text-muted)" }}>No email data returned.</p>
        }
      </Section>
    </div>
  );
}
