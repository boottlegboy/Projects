// Simple, deterministic stub so you see the full pipeline working.
// We will replace this with Bedrock/OpenAI once the flow is solid.

export function buildPrompt(resumeText, jd) {
  return `Review resume vs JD and return structured JSON. (Stub for now)\n\nRESUME:\n${resumeText}\n\nJD:\n${jd || "(none)"}\n`;
}

export async function callLLM(prompt) {
  const hasMetrics = /\b\d+%|\b\d{4}\b|\b\d+\b/.test(prompt);
  const mentions = ["react","node","python","aws","docker","sql","kubernetes","java","golang"];
  const matched = mentions.filter(k => new RegExp(`\\b${k}\\b`, "i").test(prompt));
  const missing = mentions.filter(k => !matched.includes(k));

  return {
    score: Math.min(100, 60 + matched.length * 4 + (hasMetrics ? 8 : 0)),
    summary: "Stubbed review: replace with a real LLM call later.",
    topStrengths: matched.slice(0, 3).map(k => `Mentions ${k}`),
    gaps: missing.slice(0, 3).map(k => `Missing ${k}`),
    keywordsMatched: matched,
    keywordsMissing: missing.slice(0, 7),
    actionItems: [
      "Quantify achievements with metrics.",
      "Mirror keywords from the job description.",
      "Tighten bullets with outcome-focused language."
    ]
  };
}
