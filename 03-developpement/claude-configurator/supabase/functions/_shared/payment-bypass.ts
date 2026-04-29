/**
 * Optional bypass for payment checks (staging / internal QA only).
 * Production: do NOT set SKIP_PAYMENT_CHECK; prefer CONFIGURATOR_DEV_KEY + header on curl only.
 */

export function isPaymentCheckSkipped(req: Request): boolean {
  const skipEnv = Deno.env.get("SKIP_PAYMENT_CHECK");
  if (skipEnv === "true" || skipEnv === "1") {
    console.warn(
      "[payment-bypass] SKIP_PAYMENT_CHECK active — paiement non vérifié",
    );
    return true;
  }

  const devKey = Deno.env.get("CONFIGURATOR_DEV_KEY");
  const header = req.headers.get("x-configurator-dev-key");
  if (devKey && header && secureCompare(header, devKey)) {
    console.warn("[payment-bypass] Dev key header match — paiement non vérifié");
    return true;
  }

  return false;
}

/** Constant-time-ish compare to reduce timing leaks on short secrets */
function secureCompare(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let out = 0;
  for (let i = 0; i < a.length; i++) {
    out |= a.charCodeAt(i) ^ b.charCodeAt(i);
  }
  return out === 0;
}
