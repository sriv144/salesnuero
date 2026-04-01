"use client";

import { User, Building2, Clock } from "lucide-react";
import type { RunResult } from "@/lib/types";
import { truncate } from "@/lib/utils";

interface Props {
  history: RunResult[];
  activeKey: string | null;
  onSelect: (r: RunResult) => void;
}

export default function Sidebar({ history, activeKey, onSelect }: Props) {
  return (
    <aside
      className="hidden w-64 shrink-0 flex-col gap-1 overflow-y-auto lg:flex"
      style={{ borderRight: "1px solid var(--border-subtle)", padding: "20px 12px" }}
    >
      <p
        className="mb-3 px-2 text-[10px] font-semibold uppercase tracking-widest"
        style={{ color: "var(--text-muted)" }}
      >
        Prospect History
      </p>

      {history.length === 0 && (
        <div className="flex flex-col items-center gap-2 py-10 text-center">
          <div
            className="flex h-10 w-10 items-center justify-center rounded-xl"
            style={{ background: "var(--bg-card)", border: "1px solid var(--border)" }}
          >
            <User size={18} style={{ color: "var(--text-muted)" }} />
          </div>
          <p className="text-xs" style={{ color: "var(--text-muted)" }}>
            No prospects yet. <br /> Run your first analysis.
          </p>
        </div>
      )}

      {history.map((r) => {
        const key    = `${r.prospect_name}::${r.company_name}`;
        const active = key === activeKey;
        return (
          <button
            key={key}
            onClick={() => onSelect(r)}
            className="sidebar-item text-left w-full"
            style={active ? {
              background: "var(--accent-glow)",
              border: "1px solid rgba(99,102,241,0.3)",
              borderRadius: "8px",
            } : {}}
          >
            <div className="flex items-start gap-3">
              <div
                className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-lg"
                style={{
                  background: active ? "rgba(99,102,241,0.2)" : "var(--bg-card)",
                  border: `1px solid ${active ? "rgba(99,102,241,0.3)" : "var(--border)"}`,
                }}
              >
                <User size={12} style={{ color: active ? "var(--accent-light)" : "var(--text-muted)" }} />
              </div>
              <div className="min-w-0 flex-1">
                <p
                  className="truncate text-xs font-medium"
                  style={{ color: active ? "var(--accent-light)" : "var(--text-primary)" }}
                >
                  {truncate(r.prospect_name, 22)}
                </p>
                <div className="mt-0.5 flex items-center gap-1">
                  <Building2 size={10} style={{ color: "var(--text-muted)" }} />
                  <p className="truncate text-[11px]" style={{ color: "var(--text-muted)" }}>
                    {truncate(r.company_name, 18)}
                  </p>
                </div>
              </div>
            </div>

            {/* Status pill */}
            <div className="mt-2 flex items-center gap-1.5">
              <span
                className="h-1.5 w-1.5 rounded-full"
                style={{ background: "var(--success)" }}
              />
              <span className="text-[10px]" style={{ color: "var(--text-muted)" }}>
                Profile complete
              </span>
            </div>
          </button>
        );
      })}
    </aside>
  );
}
