# TASK-0008: Implement Magic Link Callback Page

**Epic**: EPIC-5 (Frontend Integration)  
**User Story**: US-007 (Magic Link Callback Page & Sign-in)  
**Priority**: HIGH  
**Effort**: 2 hours

---

## Overview

Build the `/auth/magic-link-callback?token=<token>` page to complete email verification and user sign-in.

---

## Acceptance Criteria

- [ ] New page/route: `/auth/magic-link-callback`
- [ ] Extracts `token` query parameter
- [ ] Calls `supabase.auth.verifyOtp({email, token, type: 'magiclink'})`
- [ ] On success: JWT stored in localStorage, redirect to `/chat?onboarded=true`
- [ ] On failure: display "Link expired or invalid", link to `/pricing`
- [ ] Loading state shown while verifying (spinner)
- [ ] Handles missing email gracefully (error message + link to pricing)

---

## Definition of Done

- [ ] Page component created and deployed
- [ ] Query parameter parsing works
- [ ] OTP verification flow implemented
- [ ] JWT extracted and stored in localStorage
- [ ] Redirect logic works (success → /chat, failure → /pricing)
- [ ] Error messages clear and user-friendly
- [ ] Test with valid and invalid tokens
- [ ] Test localStorage persistence

---

## Implementation

### Step 1: Create React Component

Create `pages/auth/magic-link-callback.tsx`:

```typescript
import { useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL || '',
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || ''
);

interface VerificationState {
  loading: boolean;
  error: string | null;
  success: boolean;
}

export default function MagicLinkCallback() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [state, setState] = useState<VerificationState>({
    loading: true,
    error: null,
    success: false,
  });

  useEffect(() => {
    const verifyLink = async () => {
      try {
        // 1. Get token from URL
        const token = searchParams.get('token');

        if (!token) {
          setState({
            loading: false,
            error: 'No verification token provided. Please request a new magic link.',
            success: false,
          });
          return;
        }

        // 2. Get current session to extract email
        const { data: { session }, error: sessionErr } = await supabase.auth.getSession();

        if (sessionErr || !session?.user?.email) {
          setState({
            loading: false,
            error: 'Unable to retrieve email. Please request a new magic link.',
            success: false,
          });
          return;
        }

        const email = session.user.email;

        // 3. Verify OTP (magic link)
        const { data, error: verifyErr } = await supabase.auth.verifyOtp({
          email,
          token,
          type: 'magiclink',
        });

        if (verifyErr || !data.session) {
          setState({
            loading: false,
            error: 'Link expired or invalid. Please request a new magic link.',
            success: false,
          });
          return;
        }

        // 4. Extract JWT and store in localStorage
        const jwt = data.session.access_token;

        if (!jwt) {
          setState({
            loading: false,
            error: 'Failed to establish session. Please try again.',
            success: false,
          });
          return;
        }

        // Store JWT in localStorage
        localStorage.setItem('jwt', jwt);

        setState({
          loading: false,
          error: null,
          success: true,
        });

        // 5. Redirect to chat after brief delay
        setTimeout(() => {
          router.push('/chat?onboarded=true');
        }, 500);
      } catch (err) {
        console.error('Verification failed:', err);
        setState({
          loading: false,
          error: 'An unexpected error occurred. Please try again.',
          success: false,
        });
      }
    };

    // Only run verification on mount
    if (searchParams) {
      verifyLink();
    }
  }, [searchParams, router]);

  if (state.loading) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.spinner}></div>
          <p style={styles.text}>Verifying your email...</p>
        </div>
      </div>
    );
  }

  if (state.error) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <h2 style={styles.errorTitle}>Verification Failed</h2>
          <p style={styles.errorText}>{state.error}</p>
          <div style={styles.buttonGroup}>
            <a href="/pricing" style={styles.button}>
              Return to Pricing
            </a>
          </div>
        </div>
      </div>
    );
  }

  if (state.success) {
    return (
      <div style={styles.container}>
        <div style={styles.card}>
          <div style={styles.successIcon}>✓</div>
          <h2 style={styles.successTitle}>Welcome!</h2>
          <p style={styles.text}>Redirecting you to the chat...</p>
          <div style={styles.spinner}></div>
        </div>
      </div>
    );
  }

  return null;
}

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  card: {
    background: 'white',
    borderRadius: '8px',
    padding: '40px',
    boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
    textAlign: 'center',
    maxWidth: '500px',
    minHeight: '300px',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
  },
  spinner: {
    width: '40px',
    height: '40px',
    border: '3px solid #f3f3f3',
    borderTop: '3px solid #667eea',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite',
    margin: '20px 0',
  },
  text: {
    color: '#666',
    fontSize: '16px',
    margin: '0',
  },
  errorTitle: {
    color: '#d32f2f',
    marginTop: '0',
    marginBottom: '20px',
  },
  errorText: {
    color: '#666',
    fontSize: '16px',
    lineHeight: '1.6',
    marginBottom: '30px',
  },
  successIcon: {
    fontSize: '48px',
    color: '#4caf50',
    marginBottom: '20px',
  },
  successTitle: {
    color: '#333',
    marginTop: '0',
    marginBottom: '10px',
  },
  buttonGroup: {
    display: 'flex',
    gap: '10px',
    justifyContent: 'center',
  },
  button: {
    display: 'inline-block',
    padding: '12px 24px',
    background: '#667eea',
    color: 'white',
    textDecoration: 'none',
    borderRadius: '4px',
    fontSize: '16px',
    fontWeight: '500',
    cursor: 'pointer',
    border: 'none',
    transition: 'background 0.3s',
  },
};

// CSS animation (add to global styles or CSS module)
const styleSheet = document.createElement('style');
styleSheet.textContent = `
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
`;
document.head.appendChild(styleSheet);
```

### Step 2: Alternative — Plain HTML/JavaScript

Create `public/auth/magic-link-callback.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Verifying Email...</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .container {
      background: white;
      border-radius: 8px;
      padding: 40px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.1);
      text-align: center;
      max-width: 500px;
    }
    .spinner {
      display: inline-block;
      width: 40px;
      height: 40px;
      border: 3px solid #f3f3f3;
      border-top: 3px solid #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin: 20px 0;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    h2 {
      color: #333;
      margin: 20px 0 10px 0;
    }
    p {
      color: #666;
      font-size: 16px;
      line-height: 1.6;
      margin: 0 0 20px 0;
    }
    .error-text {
      color: #d32f2f;
    }
    .success-icon {
      font-size: 48px;
      color: #4caf50;
      margin-bottom: 20px;
    }
    a {
      display: inline-block;
      padding: 12px 24px;
      background: #667eea;
      color: white;
      text-decoration: none;
      border-radius: 4px;
      margin-top: 20px;
      transition: background 0.3s;
    }
    a:hover {
      background: #5568d3;
    }
  </style>
</head>
<body>
  <div class="container" id="container">
    <div class="spinner"></div>
    <p>Verifying your email...</p>
  </div>

  <script type="module">
    import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@latest/+esm';

    const supabase = createClient(
      'YOUR_SUPABASE_URL',
      'YOUR_SUPABASE_ANON_KEY'
    );

    async function verifyLink() {
      try {
        // 1. Get token from URL
        const params = new URLSearchParams(window.location.search);
        const token = params.get('token');

        if (!token) {
          showError('No verification token provided. Please request a new magic link.');
          return;
        }

        // 2. Get session to extract email
        const { data: { session }, error: sessionErr } = await supabase.auth.getSession();

        if (sessionErr || !session?.user?.email) {
          showError('Unable to retrieve email. Please request a new magic link.');
          return;
        }

        const email = session.user.email;

        // 3. Verify OTP
        const { data, error: verifyErr } = await supabase.auth.verifyOtp({
          email,
          token,
          type: 'magiclink'
        });

        if (verifyErr || !data.session) {
          showError('Link expired or invalid. Please request a new magic link.');
          return;
        }

        // 4. Store JWT and redirect
        const jwt = data.session.access_token;
        localStorage.setItem('jwt', jwt);

        showSuccess('Redirecting to chat...');
        setTimeout(() => {
          window.location.href = '/chat?onboarded=true';
        }, 500);
      } catch (err) {
        showError('An unexpected error occurred. Please try again.');
      }
    }

    function showError(message) {
      const container = document.getElementById('container');
      container.innerHTML = `
        <h2>Verification Failed</h2>
        <p class="error-text">${message}</p>
        <a href="/pricing">Return to Pricing</a>
      `;
    }

    function showSuccess(message) {
      const container = document.getElementById('container');
      container.innerHTML = `
        <div class="success-icon">✓</div>
        <h2>Welcome!</h2>
        <p>${message}</p>
        <div class="spinner"></div>
      `;
    }

    // Run verification on page load
    verifyLink();
  </script>
</body>
</html>
```

### Step 3: Deploy

```bash
# For Next.js: already deployed when app deployed
# For plain HTML: ensure file accessible at /auth/magic-link-callback.html
```

---

## Testing

### Test 1: Valid Magic Link

```bash
# 1. User receives email from webhook with magic link
# 2. User clicks link with valid token
# 3. Verify: JWT in localStorage, user redirected to /chat?onboarded=true
```

### Test 2: Invalid Token

```bash
# Navigate to: /auth/magic-link-callback?token=invalid
# Verify: Error message shown, link to /pricing
```

### Test 3: Expired Token

```bash
# Generate token, wait for expiry (24h), click link
# Verify: "Link expired or invalid" message
```

### Test 4: Missing Email

```bash
# Call endpoint without prior auth.getSession()
# Verify: "Unable to retrieve email" error
```

### Test 5: localStorage Persistence

```typescript
// 1. Complete verification
// 2. Check localStorage: localStorage.getItem('jwt') should return token
// 3. Refresh page
// 4. Verify: JWT still in localStorage
```

---

## Integration with Webhook

The magic link URL is sent by `stripe-webhook` via:
```typescript
await supabaseAdmin.auth.admin.inviteUserByEmail(email, {
  redirectTo: 'https://app.com/auth/magic-link-callback'
});
```

Supabase automatically appends `?token=XXX` to the redirect URL.

---

## Related Specs

- Scope: **Section 5** (Frontend — Magic Link Callback, Q-003)
- Brief: **Key Decisions** (Q-003: inviteUserByEmail automatically sends magic link)
