# TASK-0009: Integrate JWT Storage & Authorization Header

**Epic**: EPIC-5 (Frontend Integration)  
**User Story**: US-008 (Frontend — JWT Storage & Chat Integration)  
**Priority**: HIGH  
**Effort**: 2 hours

---

## Overview

Add JWT management to frontend: store JWT in localStorage after sign-in, and send it in Authorization header for all `/chat` requests.

---

## Acceptance Criteria

- [ ] JWT stored in localStorage after successful magic link verification
- [ ] localStorage key: `jwt`
- [ ] JWT persists across browser refresh
- [ ] `/chat` page reads JWT from localStorage before every request
- [ ] Authorization header added: `Authorization: Bearer <jwt>`
- [ ] 401 response clears localStorage and redirects to `/pricing`
- [ ] 403 response shows error: "Purchase required"
- [ ] JWT never logged to console
- [ ] Test localStorage persistence and error handling

---

## Definition of Done

- [ ] JWT storage implemented
- [ ] Authorization header added to chat requests
- [ ] 401 handling (logout + redirect)
- [ ] 403 handling (error message)
- [ ] Tests: valid JWT, missing JWT, 401, 403
- [ ] localStorage persistence verified

---

## Implementation

### Step 1: Create JWT Utility Hook

Create `hooks/useAuthenticatedChat.ts`:

```typescript
import { useEffect, useState } from 'react';

export interface ChatResult {
  response: string;
  diagnostic_id: string;
}

export interface ChatError {
  status: number;
  message: string;
}

export function useAuthenticatedChat() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(false);

  // Check JWT on mount
  useEffect(() => {
    const jwt = localStorage.getItem('jwt');
    setIsAuthenticated(!!jwt);
  }, []);

  const sendChat = async (message: string): Promise<ChatResult | ChatError> => {
    const jwt = localStorage.getItem('jwt');

    if (!jwt) {
      window.location.href = '/pricing';
      return { status: 401, message: 'No JWT found' };
    }

    setLoading(true);

    try {
      const response = await fetch('/functions/v1/chat', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${jwt}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      // 401: Session expired
      if (response.status === 401) {
        localStorage.removeItem('jwt');
        window.location.href = '/pricing';
        return { status: 401, message: 'Session expired' };
      }

      // 403: Payment required
      if (response.status === 403) {
        return {
          status: 403,
          message: 'You need to complete your purchase to access this feature',
        };
      }

      // Other errors
      if (!response.ok) {
        return {
          status: response.status,
          message: 'Connection failed. Please retry.',
        };
      }

      const data = await response.json() as ChatResult;
      return data;
    } catch (err) {
      return {
        status: 500,
        message: 'Connection failed. Please retry.',
      };
    } finally {
      setLoading(false);
    }
  };

  return {
    isAuthenticated,
    loading,
    sendChat,
  };
}
```

### Step 2: Update Chat Component

Modify chat page to use the hook:

```typescript
// pages/chat.tsx
import { useState } from 'react';
import { useAuthenticatedChat } from '@/hooks/useAuthenticatedChat';

export default function ChatPage() {
  const { isAuthenticated, loading, sendChat } = useAuthenticatedChat();
  const [input, setInput] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  if (!isAuthenticated) {
    return <div>Loading...</div>;
  }

  const handleSend = async () => {
    setError('');
    setResponse('');

    const result = await sendChat(input);

    // Check for error
    if ('status' in result && 'message' in result) {
      setError(result.message);
      return;
    }

    // Success
    setResponse(result.response);
    setInput('');
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Chat Diagnostic</h1>

      <textarea
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Describe your business..."
        rows={4}
        style={{ width: '100%', padding: '10px', marginBottom: '10px' }}
      />

      <button
        onClick={handleSend}
        disabled={loading}
        style={{
          padding: '10px 20px',
          background: loading ? '#ccc' : '#667eea',
          color: 'white',
          border: 'none',
          borderRadius: '4px',
          cursor: loading ? 'not-allowed' : 'pointer',
        }}
      >
        {loading ? 'Sending...' : 'Send'}
      </button>

      {error && <div style={{ color: 'red', marginTop: '20px' }}>{error}</div>}

      {response && (
        <div style={{ marginTop: '20px', padding: '15px', background: '#f5f5f5' }}>
          <h3>Diagnostic Result</h3>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
```

### Step 3: Logout Function

Create utility for clearing JWT:

```typescript
// utils/auth.ts
export function logout() {
  localStorage.removeItem('jwt');
  window.location.href = '/pricing';
}
```

Use in user menu:

```typescript
// components/Header.tsx
import { logout } from '@/utils/auth';

export function Header() {
  return (
    <header>
      <nav>
        <h1>Claude Configurator</h1>
        <button onClick={logout}>Logout</button>
      </nav>
    </header>
  );
}
```

### Step 4: Global Error Handler (Optional)

Add interceptor for all API calls:

```typescript
// utils/api.ts
export async function apiCall(
  endpoint: string,
  options?: RequestInit
): Promise<Response> {
  const jwt = localStorage.getItem('jwt');

  const response = await fetch(endpoint, {
    ...options,
    headers: {
      ...options?.headers,
      ...(jwt && { 'Authorization': `Bearer ${jwt}` }),
    },
  });

  if (response.status === 401) {
    localStorage.removeItem('jwt');
    window.location.href = '/pricing';
  }

  return response;
}
```

---

## Testing

### Test 1: JWT Storage

```typescript
// 1. Complete magic link verification
// 2. Check localStorage
const jwt = localStorage.getItem('jwt');
expect(jwt).toBeTruthy();
expect(jwt).toMatch(/^eyJ/); // JWT format check
```

### Test 2: JWT Persistence

```typescript
// 1. Store JWT in localStorage
// 2. Reload page
// 3. Verify JWT still present
expect(localStorage.getItem('jwt')).toBeTruthy();
```

### Test 3: Authorization Header

```typescript
// Intercept fetch and verify header
const originalFetch = window.fetch;
window.fetch = jest.fn(async (url, opts) => {
  if (url === '/functions/v1/chat') {
    expect(opts.headers.Authorization).toContain('Bearer ');
  }
  return originalFetch(url, opts);
});

// Send chat
await sendChat('test');

expect(window.fetch).toHaveBeenCalled();
```

### Test 4: 401 Handling

```typescript
// Mock fetch to return 401
jest.mock('fetch', () => jest.fn(() =>
  Promise.resolve(new Response('Unauthorized', { status: 401 }))
));

await sendChat('test');

// Verify logout
expect(localStorage.getItem('jwt')).toBeNull();
expect(window.location.href).toBe('/pricing');
```

### Test 5: 403 Handling

```typescript
// Mock fetch to return 403
jest.mock('fetch', () => jest.fn(() =>
  Promise.resolve(new Response('Forbidden', { status: 403 }))
));

const result = await sendChat('test');

// Verify error returned (not logged out)
expect(result.status).toBe(403);
expect(result.message).toContain('purchase');
expect(localStorage.getItem('jwt')).toBeTruthy(); // Still exists
```

### Test 6: No JWT Logging

```typescript
// 1. Send chat
// 2. Inspect browser console logs
// 3. Verify: JWT never appears in logs

const consoleSpy = jest.spyOn(console, 'log');
await sendChat('test');
expect(consoleSpy).not.toHaveBeenCalledWith(
  expect.stringContaining('eyJ')
);
```

---

## Security Checklist

- [ ] JWT stored in localStorage (survives refresh)
- [ ] JWT sent in Authorization header (standard HTTP)
- [ ] JWT never in query params (no URL logging)
- [ ] JWT never logged to console (no debug exposure)
- [ ] 401 immediately clears localStorage (stale token prevention)
- [ ] HTTPS enforced (browser requirement)

---

## Integration Notes

**With Magic Link Callback**:
- Magic link page stores JWT in localStorage
- Chat page reads JWT from localStorage
- Logout clears localStorage

**With Chat Function**:
- Chat function validates JWT signature
- Chat function checks payment status
- Both succeed → 200 response, chat proceeds

---

## Deployment Sequence

1. Create useAuthenticatedChat hook
2. Update chat page to use hook
3. Test JWT storage and persistence
4. Test 401/403 handling
5. Deploy to staging
6. Full E2E test: payment → magic link → chat access
7. Deploy to production

---

## Related Specs

- Scope: **Section 5** (Frontend — JWT Storage & Chat Integration, Q-004, Q-015)
- Brief: **Key Decisions** (Q-004: JWT extraction and validation)
