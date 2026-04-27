# US-007: Magic Link Callback Page & Sign-in

**EPIC**: EPIC-5 (Frontend Integration)  
**User Story**: As a user, I need the magic link callback to complete sign-in so that I can access the chat after receiving my verification email.

---

## Acceptance Criteria

- [ ] New page/route: `/auth/magic-link-callback?token=<token>`
- [ ] Extracts `token` query parameter
- [ ] Extracts `email` from query params or Supabase session
- [ ] Calls `supabase.auth.verifyOtp({email, token, type: 'magiclink'})`
- [ ] On success: JWT stored in localStorage, redirect to `/chat?onboarded=true`
- [ ] On failure: display error "Link expired or invalid", provide link to `/pricing`
- [ ] Magic link TTL verified (24h default, Supabase enforced)
- [ ] Page handles loading state (show spinner while verifying)

## Definition of Done

1. Page component created (`pages/auth/magic-link-callback.tsx` or similar)
2. Query parameter parsing works
3. Supabase OTP verification implemented
4. JWT extracted from session and stored in localStorage
5. Redirect logic works (success → `/chat?onboarded=true`, failure → `/pricing`)
6. Error handling displays appropriate messages
7. Loading state managed (spinner while verifying)
8. Test with valid and expired tokens

## Technical Details

**Component Structure** (React/Next.js example):
```typescript
// pages/auth/magic-link-callback.tsx
import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
);

export default function MagicLinkCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const verifyLink = async () => {
      const token = searchParams.get('token');
      
      if (!token) {
        setError('No token provided');
        setLoading(false);
        return;
      }

      // Extract email from session or use as fallback
      const { data: { session } } = await supabase.auth.getSession();
      const email = session?.user?.email;

      if (!email) {
        setError('Email not found. Please try the magic link again.');
        setLoading(false);
        return;
      }

      try {
        // Verify OTP (magic link)
        const { data, error: verifyErr } = await supabase.auth.verifyOtp({
          email,
          token,
          type: 'magiclink'
        });

        if (verifyErr) {
          setError('Link expired or invalid. Please request a new magic link.');
          setLoading(false);
          return;
        }

        // Get JWT from session
        const { data: { session: newSession } } = await supabase.auth.getSession();
        const jwt = newSession?.access_token;

        if (jwt) {
          // Store JWT in localStorage
          localStorage.setItem('jwt', jwt);
          
          // Redirect to chat
          router.push('/chat?onboarded=true');
        } else {
          setError('Failed to establish session. Please try again.');
          setLoading(false);
        }
      } catch (err) {
        console.error('Verification failed:', err);
        setError('An error occurred. Please try again.');
        setLoading(false);
      }
    };

    verifyLink();
  }, [searchParams, router]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
      {loading && <p>Verifying your link...</p>}
      {error && (
        <div>
          <p style={{ color: 'red' }}>{error}</p>
          <a href="/pricing">Back to pricing</a>
        </div>
      )}
    </div>
  );
}
```

**Alternative (Plain HTML/JavaScript)**:
```html
<!DOCTYPE html>
<html>
<head><title>Verifying Email...</title></head>
<body>
  <p id="status">Verifying your link...</p>
  
  <script type="module">
    import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@latest/+esm';
    
    const supabase = createClient(
      'https://your-project.supabase.co',
      'your-anon-key'
    );

    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');

    if (!token) {
      document.getElementById('status').textContent = 'No token provided.';
      return;
    }

    // Get session to extract email
    const { data: { session } } = await supabase.auth.getSession();
    const email = session?.user?.email;

    if (!email) {
      document.getElementById('status').innerHTML = 'Email not found. <a href="/pricing">Back to pricing</a>';
      return;
    }

    try {
      const { error } = await supabase.auth.verifyOtp({
        email,
        token,
        type: 'magiclink'
      });

      if (error) {
        document.getElementById('status').innerHTML = 'Link expired or invalid. <a href="/pricing">Back to pricing</a>';
        return;
      }

      // Get JWT
      const { data: { session: newSession } } = await supabase.auth.getSession();
      const jwt = newSession?.access_token;

      if (jwt) {
        localStorage.setItem('jwt', jwt);
        window.location.href = '/chat?onboarded=true';
      }
    } catch (err) {
      document.getElementById('status').textContent = 'An error occurred. ' + err.message;
    }
  </script>
</body>
</html>
```

**Environment Variables Required**:
- `NEXT_PUBLIC_SUPABASE_URL`: Supabase project URL (public)
- `NEXT_PUBLIC_SUPABASE_ANON_KEY`: Supabase anon key (public)

## Dependencies

Requires:
- US-004 (stripe-webhook creates users and sends magic links)
- `/chat` page exists for redirect

## Related Specs

- Scope: **Section 5** (Frontend — Integrate JWT, Magic Link Callback)
- Brief: **Key Decisions** (Q-003: inviteUserByEmail automatically sends magic link)
