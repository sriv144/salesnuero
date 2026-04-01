export interface BigFiveScores {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
}

export interface PersonalityProfile {
  big_five: BigFiveScores;
  disc_type: string;
  buying_motivators: string[];
  communication_style: string;
  objection_patterns: string[];
  raw_output: string;
}

export interface Email {
  subject: string;
  body: string;
  ps_line: string;
}

export interface EmailSequence {
  email_1: Email;
  email_2: Email;
  email_3: Email;
  raw_output: string;
}

export interface RunResult {
  prospect_name: string;
  company_name: string;
  research_summary: string;
  profile_raw: string;
  personality_profile: PersonalityProfile | null;
  strategy_brief: string;
  emails_raw: string;
  email_sequence: EmailSequence | null;
  raw_crew_output: string;
}

export interface RunResponse {
  status: "success" | "error";
  result: RunResult | null;
  error: string | null;
}

export interface RunRequest {
  prospect_name: string;
  company_name: string;
}

/* Radar chart data shape for recharts */
export interface RadarPoint {
  trait: string;
  score: number;
  fullMark: number;
}

/* Parsed email for display */
export interface ParsedEmail {
  number: number;
  label: string;
  subject: string;
  body: string;
  ps: string;
  intent: string;
}
