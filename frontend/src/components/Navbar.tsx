"use client";

import { Brain, Zap } from "lucide-react";

export default function Navbar() {
  return (
    <header
      style={{
        background: "rgba(9,11,20,0.85)",
        backdropFilter: "blur(16px)",
        borderBottom: "1px solid var(--border-subtle)",
      }}
      className="sticky top-0 z-50 flex items-center justify-between px-6 py-3"
    >
      {/* Logo */}
      <div className="flex items-center gap-3">
        <div
          className="flex h-8 w-8 items-center justify-center rounded-lg"
          style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)" }}
        >
          <Brain size={16} color="#fff" />
        </div>
        <div className="flex items-baseline gap-1.5">
          <span className="text-base font-semibold tracking-tight" style={{ color: "var(--text-primary)" }}>
            SalesNeuro
          </span>
          <span
            className="rounded px-1.5 py-0.5 text-[10px] font-medium uppercase tracking-wider"
            style={{ background: "var(--accent-glow)", color: "var(--accent-light)", border: "1px solid rgba(99,102,241,0.25)" }}
          >
            Beta
          </span>
        </div>
      </div>

      {/* Tagline */}
      <div className="hidden items-center gap-1.5 md:flex" style={{ color: "var(--text-muted)" }}>
        <Zap size={12} style={{ color: "var(--accent-light)" }} />
        <span className="text-xs">AI Buyer Psychology Intelligence</span>
      </div>

      {/* Status */}
      <div className="flex items-center gap-2">
        <span className="pulse-dot h-1.5 w-1.5 rounded-full" style={{ background: "var(--success)" }} />
        <span className="text-xs" style={{ color: "var(--text-muted)" }}>Pipeline ready</span>
      </div>
    </header>
  );
}
