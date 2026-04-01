"use client";

import {
  Radar, RadarChart, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, ResponsiveContainer, Tooltip,
} from "recharts";
import { parseBigFive, toRadarData, scoreLabel } from "@/lib/utils";
import type { RadarPoint } from "@/lib/types";

/* Trait metadata */
const TRAIT_META: Record<string, { short: string; color: string; desc: string }> = {
  Openness:          { short: "O", color: "#8b5cf6", desc: "Curiosity, creativity, openness to new ideas" },
  Conscientiousness: { short: "C", color: "#6366f1", desc: "Organisation, goal-driven, detail-oriented" },
  Extraversion:      { short: "E", color: "#06b6d4", desc: "Social energy, assertiveness, visibility" },
  Agreeableness:     { short: "A", color: "#10b981", desc: "Cooperation, empathy, team-first mindset" },
  Neuroticism:       { short: "N", color: "#f59e0b", desc: "Stress sensitivity, risk awareness" },
};

const DISC_META: Record<string, { label: string; color: string; desc: string }> = {
  D: { label: "Dominance",       color: "#ef4444", desc: "Direct, results-oriented, decisive, time-poor" },
  I: { label: "Influence",       color: "#f59e0b", desc: "Enthusiastic, relationship-driven, optimistic" },
  S: { label: "Steadiness",      color: "#10b981", desc: "Patient, loyal, process-oriented, stable" },
  C: { label: "Conscientiousness", color: "#6366f1", desc: "Analytical, quality-driven, detail-focused" },
};

/* Custom tooltip */
function CustomTooltip({ active, payload }: { active?: boolean; payload?: Array<{ payload: RadarPoint }> }) {
  if (!active || !payload?.length) return null;
  const d = payload[0].payload;
  const meta = TRAIT_META[d.trait];
  return (
    <div className="rounded-lg px-3 py-2 text-xs shadow-xl"
      style={{ background: "var(--bg-card-2)", border: "1px solid var(--border)", color: "var(--text-secondary)" }}>
      <p className="font-semibold mb-0.5" style={{ color: meta?.color ?? "var(--accent-light)" }}>
        {d.trait}
      </p>
      <p className="mb-0.5">{d.score} / 10 — <span style={{ color: "var(--text-primary)" }}>{scoreLabel(d.score)}</span></p>
      {meta && <p style={{ color: "var(--text-muted)", maxWidth: 160 }}>{meta.desc}</p>}
    </div>
  );
}

interface Props {
  profileRaw: string;
  discRaw?: string;
}

export default function PsychologyRadar({ profileRaw, discRaw = "" }: Props) {
  const scores   = parseBigFive(profileRaw);
  const data     = toRadarData(scores);
  const rawText  = discRaw || profileRaw;
  const discChar = (() => {
    const m = rawText.match(/\b([DISC])\b.*?(type|profile)/i)
           ?? rawText.match(/DISC[:\s]+([DISC])/i)
           ?? rawText.match(/type[:\s]+([DISC])\b/i);
    if (m) return m[1].toUpperCase();
    if (/dominan/i.test(rawText)) return "D";
    if (/influenc/i.test(rawText)) return "I";
    if (/steadiness|steady/i.test(rawText)) return "S";
    if (/conscientious/i.test(rawText) && !rawText.includes("conscientiousness:")) return "C";
    return "—";
  })();
  const discInfo = DISC_META[discChar];

  return (
    <div className="space-y-4">
      {/* Radar */}
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <RadarChart data={data} margin={{ top: 8, right: 30, bottom: 8, left: 30 }}>
            <PolarGrid stroke="var(--border)" strokeDasharray="3 3" />
            <PolarAngleAxis
              dataKey="trait"
              tick={{ fontSize: 11, fill: "var(--text-secondary)", fontFamily: "var(--font-geist-sans)" }}
            />
            <PolarRadiusAxis
              angle={90}
              domain={[0, 10]}
              tick={{ fontSize: 9, fill: "var(--text-muted)" }}
              tickCount={6}
              stroke="transparent"
            />
            <Radar
              name="Profile"
              dataKey="score"
              stroke="var(--accent)"
              fill="var(--accent)"
              fillOpacity={0.18}
              strokeWidth={2}
              dot={{ fill: "var(--accent)", r: 4, strokeWidth: 0 }}
              activeDot={{ r: 6, fill: "var(--accent-light)", strokeWidth: 0 }}
            />
            <Tooltip content={<CustomTooltip />} />
          </RadarChart>
        </ResponsiveContainer>
      </div>

      {/* Score bars */}
      <div className="space-y-2">
        {data.map((d) => {
          const meta = TRAIT_META[d.trait];
          return (
            <div key={d.trait} className="flex items-center gap-3">
              <div
                className="flex h-5 w-5 shrink-0 items-center justify-center rounded text-[10px] font-bold"
                style={{ background: `${meta.color}20`, color: meta.color }}
              >
                {meta.short}
              </div>
              <div className="flex-1">
                <div className="flex justify-between mb-0.5">
                  <span className="text-xs" style={{ color: "var(--text-secondary)" }}>{d.trait}</span>
                  <span className="text-xs font-medium" style={{ color: meta.color }}>
                    {d.score}/10 · {scoreLabel(d.score)}
                  </span>
                </div>
                <div className="h-1.5 rounded-full overflow-hidden" style={{ background: "var(--bg-surface)" }}>
                  <div
                    className="h-full rounded-full transition-all duration-700"
                    style={{ width: `${d.score * 10}%`, background: meta.color }}
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* DISC badge */}
      {discInfo && (
        <div
          className="mt-2 flex items-center gap-3 rounded-lg px-4 py-3"
          style={{ background: `${discInfo.color}12`, border: `1px solid ${discInfo.color}30` }}
        >
          <div
            className="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-lg font-bold"
            style={{ background: `${discInfo.color}20`, color: discInfo.color }}
          >
            {discChar}
          </div>
          <div>
            <p className="text-sm font-semibold" style={{ color: discInfo.color }}>
              DISC: {discInfo.label}
            </p>
            <p className="text-xs" style={{ color: "var(--text-muted)" }}>{discInfo.desc}</p>
          </div>
        </div>
      )}
    </div>
  );
}
