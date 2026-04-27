# US-009: Success Page — Payment Confirmation

**EPIC**: EPIC-5 (Frontend Integration)  
**User Story**: As a user, I need a success page after payment so that I know what to expect next (magic link sent).

---

## Acceptance Criteria

- [ ] New page/route: `/success.html?session_id=<cs_xyz>`
- [ ] Displays message: "Magic link sent to your email. Check your inbox (and spam folder)."
- [ ] Shows session ID for reference (optional, for debugging)
- [ ] Auto-redirects after 5 seconds to `/auth/magic-link-callback` (or manual button)
- [ ] Or optionally: "Waiting for verification..." with manual "Check email" button
- [ ] No email field required (automatic via Stripe `customer_email`)
- [ ] Manual link to check email or resend link (future feature)
- [ ] Matches brand and styling of rest of app

## Definition of Done

1. Page created at `/success.html` or `/pages/success.tsx`
2. Session ID extracted from query params
3. User-friendly message displayed
4. Auto-redirect or manual button works
5. Page accessible after Stripe checkout
6. Matches app styling

## Technical Details

**Simple HTML Version**:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Payment Successful</title>
  <style>
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
    h1 {
      color: #333;
      margin: 0 0 20px 0;
    }
    p {
      color: #666;
      font-size: 16px;
      line-height: 1.6;
      margin: 0 0 30px 0;
    }
    .code {
      background: #f5f5f5;
      padding: 10px;
      border-radius: 4px;
      font-family: monospace;
      color: #333;
      margin: 20px 0;
    }
    .spinner {
      display: inline-block;
      width: 30px;
      height: 30px;
      border: 3px solid #f3f3f3;
      border-top: 3px solid #667eea;
      border-radius: 50%;
      animation: spin 1s linear infinite;
      margin-right: 10px;
    }
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    .countdown {
      color: #999;
      font-size: 14px;
      margin-top: 20px;
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>✓ Payment Successful</h1>
    <p>Thank you for your purchase! We've sent a magic link to your email address.</p>
    <p><strong>Check your inbox (and spam folder) for the verification link.</strong></p>
    
    <div class="code" id="sessionId" style="display:none;"></div>
    
    <div style="margin-top: 30px;">
      <span class="spinner"></span>
      <span>Redirecting to verification in <span id="countdown">5</span> seconds...</span>
    </div>
    
    <div class="countdown" style="margin-top: 30px;">
      <a href="javascript:void(0)" onclick="redirectNow()">Click here if not redirected</a>
    </div>
  </div>

  <script>
    // Extract session ID from URL
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get('session_id');
    
    if (sessionId) {
      const elem = document.getElementById('sessionId');
      elem.textContent = 'Session ID: ' + sessionId;
      elem.style.display = 'block';
    }

    // Auto-redirect countdown
    let countdown = 5;
    const timer = setInterval(() => {
      countdown--;
      document.getElementById('countdown').textContent = countdown;
      if (countdown <= 0) {
        clearInterval(timer);
        redirectNow();
      }
    }, 1000);

    function redirectNow() {
      // Redirect to magic link callback (user clicks link in email)
      window.location.href = '/auth/magic-link-callback';
    }
  </script>
</body>
</html>
```

**React Component Version**:
```typescript
// pages/success.tsx
import { useEffect, useState } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';

export default function SuccessPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const [countdown, setCountdown] = useState(5);

  const sessionId = searchParams.get('session_id');

  useEffect(() => {
    const timer = setInterval(() => {
      setCountdown((prev) => {
        if (prev <= 1) {
          router.push('/auth/magic-link-callback');
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [router]);

  const redirectNow = () => {
    router.push('/auth/magic-link-callback');
  };

  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center', 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    }}>
      <div style={{
        background: 'white',
        borderRadius: '8px',
        padding: '40px',
        boxShadow: '0 10px 40px rgba(0,0,0,0.1)',
        textAlign: 'center',
        maxWidth: '500px'
      }}>
        <h1>✓ Payment Successful</h1>
        <p>Thank you for your purchase! We've sent a magic link to your email address.</p>
        <p><strong>Check your inbox (and spam folder) for the verification link.</strong></p>
        
        {sessionId && (
          <div style={{ background: '#f5f5f5', padding: '10px', borderRadius: '4px', margin: '20px 0' }}>
            Session ID: {sessionId}
          </div>
        )}
        
        <div style={{ marginTop: '30px' }}>
          <p>Redirecting to verification in <strong>{countdown}</strong> seconds...</p>
        </div>
        
        <button 
          onClick={redirectNow}
          style={{
            marginTop: '20px',
            padding: '10px 20px',
            background: '#667eea',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Click here if not redirected
        </button>
      </div>
    </div>
  );
}
```

## Dependencies

Requires:
- US-005 (create-checkout returns success URL pointing to `/success.html`)

## Related Specs

- Scope: **Section 5** (Frontend — Success Page, Q-006, Q-010)
- Brief: **Objectives** (User flow confirmation after payment)
