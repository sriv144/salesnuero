import type { BigFiveScores, ParsedEmail, RadarPoint } from "./types";

/* ─── Big Five parser ─────────────────────────────────────── */
export function parseBigFive(text: string): BigFiveScores {
  const extract = (label: string): number => {
    const re = new RegExp(`${label}[^\\d]*(\\d+)`, "i");
    const m = text.match(re);
    return m ? Math.min(10, Math.max(1, parseInt(m[1]))) : 5;
  };
  return {
    openness:          extract("openness|open"),
    conscientiousness: extract("conscientiousness|conscientious"),
    extraversion:      extract("extraversion|extroversion|extravert"),
    agreeableness:     extract("agreeableness|agreeable"),
    neuroticism:       extract("neuroticism|neurotic"),
  };
}

export function toRadarData(scores: BigFiveScores): RadarPoint[] {
  return [
    { trait: "Openness",          score: scores.openness,          fullMark: 10 },
    { trait: "Conscientiousness", score: scores.conscientiousness,  fullMark: 10 },
    { trait: "Extraversion",      score: scores.extraversion,       fullMark: 10 },
    { trait: "Agreeableness",     score: scores.agreeableness,      fullMark: 10 },
    { trait: "Neuroticism",       score: scores.neuroticism,        fullMark: 10 },
  ];
}

/* ─── DISC parser ────────────────────────────────────────── */
export function parseDISC(text: string): string {
  const m = text.match(/\bDISC\s*[:\-–]?\s*([DISC]{1,2})\b/i)
    ?? text.match(/\btype[:\s]+([DISC]{1,2})\b/i)
    ?? text.match(/\b([DISC])\s*[-–]\s*(Dominance|Influence|Steadiness|Conscientiousness)/i);
  if (m) return m[1].toUpperCase();
  if (/dominan/i.test(text)) return "D";
  if (/influenc/i.test(text)) return "I";
  if (/steadiness|steady/i.test(text)) return "S";
  if (/conscientious/i.test(text)) return "C";
  return "—";
}

/* ─── Email parser ───────────────────────────────────────── */
const EMAIL_INTENTS = ["Pattern Interrupt", "Value + Social Proof", "Low-Friction CTA"];

export function parseEmails(raw: string): ParsedEmail[] {
  const sections = raw.split(/(?=Email\s+[123])/i).filter(Boolean);
  return [0, 1, 2].map((i) => {
    const block = sections[i] ?? "";
    const subjectMatch = block.match(/Subject(?:\s*Line)?[:\s]+(.+)/i);
    const psMatch      = block.match(/P\.?S\.?[:\s]+(.+)/i);
    const subject = subjectMatch ? subjectMatch[1].trim() : "(No subject)";
    const ps      = psMatch      ? psMatch[1].trim()      : "";

    // Body = everything between subject line and P.S. (or end)
    let body = block
      .replace(/Email\s+[123][^\n]*/i, "")
      .replace(/Subject(?:\s*Line)?[:\s]+.+/i, "")
      .replace(/P\.?S\.?[:\s]+.+/i, "")
      .trim();

    if (!body) body = block.replace(/Email\s+[123]/i, "").trim();

    return {
      number: i + 1,
      label: `Email ${i + 1}`,
      subject,
      body: body || "(No body)",
      ps,
      intent: EMAIL_INTENTS[i],
    };
  });
}

/* ─── Score to label ────────────────────────────────────── */
export function scoreLabel(score: number): string {
  if (score >= 8) return "Very High";
  if (score >= 6) return "High";
  if (score >= 4) return "Moderate";
  if (score >= 2) return "Low";
  return "Very Low";
}

/* ─── Truncate text ─────────────────────────────────────── */
export function truncate(text: string, max: number): string {
  return text.length > max ? text.slice(0, max) + "…" : text;
}
