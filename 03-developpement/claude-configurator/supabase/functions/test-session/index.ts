import { createClient } from "https://esm.sh/@supabase/supabase-js@2.38.0";

const supabaseUrl = Deno.env.get("SUPABASE_URL") || "";
const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";

const supabase = createClient(supabaseUrl, supabaseServiceKey);

Deno.serve(async (req: Request) => {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" },
    });
  }

  try {
    const { email } = await req.json();

    if (!email) {
      return new Response(JSON.stringify({ error: "Email required" }), {
        status: 400,
        headers: { "Content-Type": "application/json" },
      });
    }

    // Créer ou récupérer l'utilisateur
    const { data: user, error: userError } = await supabase.auth.admin.createUser({
      email,
      password: Math.random().toString(36).slice(2),
      email_confirm: true,
    });

    if (userError && !userError.message.includes("already exists")) {
      throw userError;
    }

    // Générer une session
    const { data: session, error: sessionError } = await supabase.auth.admin.generateLink({
      type: "magiclink",
      email,
      options: {
        redirectTo: `${new URL(req.url).origin.replace("/functions/v1", "")}/chat.html?test=true`,
      },
    });

    if (sessionError) throw sessionError;

    return new Response(
      JSON.stringify({
        success: true,
        link: session?.properties?.action_link || `https://setup.csbusiness.fr/chat.html?test=true&email=${encodeURIComponent(email)}`,
        email,
      }),
      {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }
    );
  } catch (error) {
    console.error("Error:", error);
    return new Response(
      JSON.stringify({ error: error.message || "Internal server error" }),
      {
        status: 500,
        headers: { "Content-Type": "application/json" },
      }
    );
  }
});
