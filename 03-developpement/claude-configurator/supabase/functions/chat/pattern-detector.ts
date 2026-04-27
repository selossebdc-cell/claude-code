// Pattern Detection Engine for Diagnostic Intelligence
// Analyzes client responses in real-time to detect patterns, pain points, strengths, and risks

import {
  Pattern,
  PainPoint,
  WorkStyleTrait,
  DiagnosticMetadata,
} from "./metadata-manager.ts";

interface Message {
  role: "user" | "assistant" | "system";
  content: string;
}

interface DetectionResult {
  newPatterns: Pattern[];
  updatedMetadata: DiagnosticMetadata;
}

export function detectPatterns(
  currentUserResponse: string,
  conversationHistory: Message[],
  currentMetadata: DiagnosticMetadata
): DetectionResult {
  const detectedPatterns: Pattern[] = [];

  // PATTERN 1: Recurring Keywords/Blocages
  const recurringBlockages = detectRecurringKeywords(conversationHistory, [
    "compliance",
    "documentation",
    "workflow",
    "deadlines",
    "communication",
    "process",
    "team",
    "scaling",
    "management",
    "quality",
    "testing",
  ]);

  recurringBlockages.forEach(({ keyword, occurrences, contexts }) => {
    detectedPatterns.push({
      type: "recurring_blocage",
      pattern: `Recurring challenge: ${keyword}`,
      evidence: contexts.slice(0, 2),
      confidence: Math.min(occurrences / 5, 1), // Normalize 0-1
      consequence: `Mentioned ${occurrences} times — this is a systemic blocker`,
      implication_for_claude: `Claude can help systematize or automate "${keyword}"`,
    });
  });

  // PATTERN 2: Work Style Traits
  const workStyleTraits = detectWorkStyle(conversationHistory);

  workStyleTraits.forEach(({ trait, evidence, implication }) => {
    detectedPatterns.push({
      type: "work_style",
      pattern: trait,
      evidence: [evidence],
      implication_for_claude: implication,
    });
  });

  // PATTERN 3: Strength Signals
  const strengths = detectStrengths(conversationHistory);

  strengths.forEach(({ strength, evidence }) => {
    detectedPatterns.push({
      type: "strength",
      pattern: `Strong at: ${strength}`,
      evidence: [evidence],
      confidence: 0.8,
      implication_for_claude: `Claude can amplify this core competency`,
    });
  });

  // PATTERN 4: Risk Indicators
  const risks = detectRiskIndicators(conversationHistory);

  risks.forEach(({ risk, indicator_phrase }) => {
    detectedPatterns.push({
      type: "risk_indicator",
      pattern: `Risk/Blind spot: ${risk}`,
      evidence: [indicator_phrase],
      confidence: 0.7,
      consequence: `Potential gap or oversight`,
      implication_for_claude: `Claude can systematize this area`,
    });
  });

  const updatedMetadata = mergePatterns(currentMetadata, detectedPatterns);

  return {
    newPatterns: detectedPatterns,
    updatedMetadata,
  };
}

function detectRecurringKeywords(
  history: Message[],
  keywords: string[],
  minOccurrences = 2
): Array<{ keyword: string; occurrences: number; contexts: string[] }> {
  const occurrenceMap: Record<string, number> = {};
  const contexts: Record<string, string[]> = {};

  history.forEach((message) => {
    if (message.role !== "user") return;
    const text = message.content.toLowerCase();

    keywords.forEach((keyword) => {
      if (text.includes(keyword.toLowerCase())) {
        occurrenceMap[keyword] = (occurrenceMap[keyword] || 0) + 1;
        if (!contexts[keyword]) contexts[keyword] = [];

        // Extract snippet around keyword
        const idx = text.indexOf(keyword.toLowerCase());
        const start = Math.max(0, idx - 30);
        const end = Math.min(text.length, idx + keyword.length + 50);
        const snippet = text.substring(start, end).trim();

        contexts[keyword].push(snippet);
      }
    });
  });

  return Object.entries(occurrenceMap)
    .filter(([_, count]) => count >= minOccurrences)
    .map(([keyword, count]) => ({
      keyword,
      occurrences: count,
      contexts: contexts[keyword].slice(0, 2), // Keep first 2 mentions
    }));
}

function detectWorkStyle(
  history: Message[]
): Array<{ trait: string; evidence: string; implication: string }> {
  const styleIndicators: Record<string, string[]> = {
    pragmatic: ["fast", "quick", "practical", "results", "reality"],
    structured: ["process", "system", "step-by-step", "organized", "plan"],
    feeling_based: ["gut", "feeling", "sense", "intuition", "vibe"],
    innovative: ["try", "experiment", "new", "different", "test"],
    risk_aware: ["careful", "check", "verify", "compliance", "rule"],
  };

  const detected: Array<{ trait: string; evidence: string; implication: string }> = [];
  const userResponses = history
    .filter((m) => m.role === "user")
    .map((m) => m.content.toLowerCase());
  const combinedText = userResponses.join(" ");

  Object.entries(styleIndicators).forEach(([style, indicators]) => {
    const matchCount = indicators.filter((ind) =>
      combinedText.includes(ind)
    ).length;

    if (matchCount >= 2) {
      detected.push({
        trait: style.charAt(0).toUpperCase() + style.slice(1),
        evidence: `Shows ${matchCount} indicators of ${style} approach`,
        implication: `Config should support ${style} work style`,
      });
    }
  });

  return detected;
}

function detectStrengths(
  history: Message[]
): Array<{ strength: string; evidence: string }> {
  const strengthPhrases = [
    /I(?:'m|\ am)\ (?:really\ )?good\ at\ ([^.!?]+)/i,
    /I\ (?:love|enjoy|like)\ ([^.!?]+)/i,
    /I'm\ (?:passionate|enthusiastic)\ about\ ([^.!?]+)/i,
    /successfully\ ([^.!?]+)/i,
  ];

  const strengths: Array<{ strength: string; evidence: string }> = [];
  const userResponses = history.filter((m) => m.role === "user");

  userResponses.forEach((response) => {
    strengthPhrases.forEach((regex) => {
      const match = response.content.match(regex);
      if (match && match[1]) {
        const strength = match[1].trim().slice(0, 50); // Cap length
        strengths.push({
          strength,
          evidence: `Client mentioned competence/passion in: ${strength}`,
        });
      }
    });
  });

  // Deduplicate
  const uniqueStrengths = Array.from(
    new Map(strengths.map((s) => [s.strength, s])).values()
  );
  return uniqueStrengths.slice(0, 5); // Top 5
}

function detectRiskIndicators(
  history: Message[]
): Array<{ risk: string; indicator_phrase: string }> {
  const riskPhrases = [
    /I (?:forget|often forget|always forget)\ ([^.!?]+)/i,
    /I (?:struggle|have trouble)\ (?:with\ )?([^.!?]+)/i,
    /nobody\ (?:tracks|manages|checks)\ ([^.!?]+)/i,
    /I\ don't\ (?:have|keep|track)\ ([^.!?]+)/i,
  ];

  const risks: Array<{ risk: string; indicator_phrase: string }> = [];
  const userResponses = history.filter((m) => m.role === "user");

  userResponses.forEach((response) => {
    riskPhrases.forEach((regex) => {
      const match = response.content.match(regex);
      if (match && match[1]) {
        const risk = match[1].trim().slice(0, 50);
        risks.push({
          risk,
          indicator_phrase: match[0].trim(),
        });
      }
    });
  });

  // Deduplicate
  const uniqueRisks = Array.from(
    new Map(risks.map((r) => [r.risk, r])).values()
  );
  return uniqueRisks.slice(0, 3); // Top 3
}

function mergePatterns(
  currentMetadata: DiagnosticMetadata,
  newPatterns: Pattern[]
): DiagnosticMetadata {
  const updated = { ...currentMetadata };

  newPatterns.forEach((pattern) => {
    if (pattern.type === "recurring_blocage") {
      if (!updated.pain_points) updated.pain_points = [];

      // Avoid duplicates
      if (!updated.pain_points.some((p) => p.area === pattern.pattern)) {
        updated.pain_points.push({
          area: pattern.pattern,
          detail: pattern.consequence,
          severity: pattern.confidence! >= 0.8 ? "high" : "medium",
          context: pattern.evidence?.[0],
        });
      }
    } else if (pattern.type === "work_style") {
      if (!updated.work_style_traits) updated.work_style_traits = [];

      if (!updated.work_style_traits.some((t) => t.trait === pattern.pattern)) {
        updated.work_style_traits.push({
          trait: pattern.pattern,
          manifestation: pattern.evidence?.[0],
          implication: pattern.implication_for_claude,
        });
      }
    } else if (pattern.type === "strength") {
      if (!updated.work_style_traits) updated.work_style_traits = [];

      if (!updated.work_style_traits.some((t) => t.trait === pattern.pattern)) {
        updated.work_style_traits.push({
          trait: pattern.pattern,
          manifestation: pattern.evidence?.[0],
          implication: pattern.implication_for_claude,
          strength: true,
        });
      }
    } else if (pattern.type === "risk_indicator") {
      if (!updated.pain_points) updated.pain_points = [];

      if (!updated.pain_points.some((p) => p.area === pattern.pattern)) {
        updated.pain_points.push({
          area: pattern.pattern,
          detail: pattern.consequence,
          severity: "medium",
          context: pattern.evidence?.[0],
        });
      }
    }
  });

  // Update patterns_detected array
  if (!updated.patterns_detected) updated.patterns_detected = [];
  newPatterns.forEach((newPattern) => {
    if (
      !updated.patterns_detected!.some(
        (p) => p.pattern === newPattern.pattern
      )
    ) {
      updated.patterns_detected!.push(newPattern);
    }
  });

  return updated;
}
