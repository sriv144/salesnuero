"use client";

import { useState } from "react";
import { Mail, Copy, Check, ChevronRight } from "lucide-react";
import { parseEmails } from "@/lib/utils";
import type { ParsedEmail } from "@/lib/types";

const TAB_COLORS = [
  { accent: "#6366f1", bg: "rgba(99,102,241,0.1)", border: "rgba(99,102,241,0.3)" },
  { accent: "#8b5cf6", bg: "rgba(139,92,246,0.1)", border: "rgba(139,92,246,0.3)" },
  { accent: "#06b6d4", bg: "rgba(6,182,212,0.1)",  border: "rgba(6,182,212,0.3)" },
];

const INTENT_ICONS = ["🎯", "💎", "🚀"];

interface Props { emailsRaw: string }

function CopyButton({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);
  const copy = () => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  return (
    <button
      onClick={copy}
      className="flex items-center gap-1.5 rounded-md px-2.5 py-1 text-xs transition-all"
      style={{
        background: copied ? "rgba(16,185,129,0.12)" : "var(--bg-surface)",
        border: copied ? "1px solid rgba(16,185,129,0.3)" : "1px solid var(--border)",
        color: copied ? "var(--success)" : "var(--text-muted)",
      }}
    >
      {copied ? <Check size={11} /> : <Copy size={11} />}
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}

function EmailCard({ email, color }: { email: ParsedEmail; color: typeof TAB_COLORS[0] }) {
  const fullText = `Subject: ${email.subject}\n\n${email.body}${email.ps ? `\n\nP.S. ${email.ps}` : ""}`;

  return (
    <div className="fade-in space-y-4">
      {/* Intent badge */}
      <div className="flex items-center justify-between">
        <div
          className="flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium"
          style={{ background: color.bg, border: `1px solid ${color.border}`, color: color.accent }}
        >
          <span>{INTENT_ICONS[email.number - 1]}</span>
          {email.intent}
        </div>
        <CopyButton text={fullText} />
      </div>

      {/* Subject line */}
      <div
        className="rounded-lg px-4 py-3"
        style={{ background: color.bg, border: `1px solid ${color.border}` }}
      >
        <p className="mb-1 text-[10px] font-semibold uppercase tracking-widest" style={{ color: color.accent }}>
          Subject Line
        </p>
        <p className="text-sm font-medium" style={{ color: "var(--text-primary)" }}>
          {email.subject}
        </p>
      </div>

      {/* Body */}
      <div
        className="rounded-lg px-4 py-3"
        style={{ background: "var(--bg-surface)", border: "1px solid var(--border)" }}
      >
        <p className="mb-2 text-[10px] font-semibold uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
          Body
        </p>
        <p className="whitespace-pre-wrap text-sm leading-relaxed" style={{ color: "var(--text-secondary)" }}>
          {email.body}
        </p>
      </div>

      {/* P.S. */}
      {email.ps && (
        <div
          className="flex gap-2 rounded-lg px-4 py-3"
          style={{ background: "rgba(99,102,241,0.04)", border: "1px solid var(--border-subtle)" }}
        >
          <ChevronRight size={14} className="mt-0.5 shrink-0" style={{ color: color.accent }} />
          <div>
            <p className="mb-0.5 text-[10px] font-semibold uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
              P.S.
            </p>
            <p className="text-sm italic" style={{ color: "var(--text-secondary)" }}>{email.ps}</p>
          </div>
        </div>
      )}
    </div>
  );
}

export default function EmailSequence({ emailsRaw }: Props) {
  const [activeTab, setActiveTab] = useState(0);
  const emails = parseEmails(emailsRaw);
  const color  = TAB_COLORS[activeTab];

  return (
    <div className="space-y-4">
      {/* Tabs */}
      <div className="flex gap-1 rounded-lg p-1" style={{ background: "var(--bg-surface)", border: "1px solid var(--border)" }}>
        {emails.map((email, i) => {
          const c = TAB_COLORS[i];
          const active = i === activeTab;
          return (
            <button
              key={i}
              onClick={() => setActiveTab(i)}
              className="flex flex-1 items-center justify-center gap-2 rounded-md px-3 py-2 text-xs font-medium transition-all"
              style={{
                background: active ? c.bg : "transparent",
                border: active ? `1px solid ${c.border}` : "1px solid transparent",
                color: active ? c.accent : "var(--text-muted)",
              }}
            >
              <Mail size={12} />
              {email.label}
            </button>
          );
        })}
      </div>

      {/* Active email */}
      <EmailCard email={emails[activeTab]} color={color} />

      {/* Usage tips */}
      <div
        className="rounded-lg px-4 py-3"
        style={{ background: "var(--bg-surface)", border: "1px solid var(--border-subtle)" }}
      >
        <p className="mb-2 text-[10px] font-semibold uppercase tracking-widest" style={{ color: "var(--text-muted)" }}>
          Sequence Strategy
        </p>
        <div className="flex flex-col gap-1.5">
          {emails.map((e, i) => (
            <div key={i} className="flex items-start gap-2 text-xs">
              <span style={{ color: TAB_COLORS[i].accent }}>{INTENT_ICONS[i]}</span>
              <span style={{ color: "var(--text-secondary)" }}>
                <span className="font-medium" style={{ color: TAB_COLORS[i].accent }}>Email {i + 1}:</span>{" "}
                {e.intent}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
