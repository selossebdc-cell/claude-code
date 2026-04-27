# US-008: Frontend — JWT Storage & Chat Integration

**EPIC**: EPIC-5 (Frontend Integration)  
**User Story**: As a frontend engineer, I need JWT integration so that authenticated users can call the /chat endpoint with their token.

---

## Acceptance Criteria

- [ ] JWT stored in localStorage after successful sign-in
- [ ] localStorage key: `jwt`
- [ ] JWT persists across browser refresh (localStorage behavior)
- [ ] `/chat` page reads JWT from localStorage: `localStorage.getItem('jwt')`
- [ ] Every `/chat` request includes `Authorization: Bearer <jwt>` header
- [ ] 401 response: clear localStorage, redirect to `/pricing` with message "Session expired"
- [ ] 403 response: show error message "You need to complete your purchase to access this feature"
- [ ] Network error: show "Connection failed. Please retry."
- [ ] JWT never logged to console or sent in query parameters

## Definition of Done

1. JWT storage implemented in localStorage
2. JWT cleared on 401 response
3. Authorization header added to all chat requests
4. Error handling displays appropriate messages
5. Test with valid JWT, expired JWT (simulate 401), unpaid user (simulate 403)
6. Verify JWT not logged to console
7. Test localStorage persistence across page refresh

## Technical Details

**Storing JWT after Sign-in** (in magic-link-callback or login flow):
```typescript
// After successful verifyOtp()
const { data: { session } } = await supabase.auth.getSession();
const jwt = session?.access_token;
localStorage.setItem('jwt', jwt);
```

**Chat Request with Authorization Header**:
```typescript
// pages/chat.tsx or components/ChatComponent.tsx
async function sendMessage(message: string) {
  const token = localStorage.getItem('jwt');

  if (!token) {
    window.location.href = '/pricing';
    return;
  }

  try {
    const response = await fetch('/functions/v1/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    if (response.status === 401) {
      // Session expired
      localStorage.removeItem('jwt');
      alert('Your session has expired. Please log in again.');
      window.location.href = '/pricing';
      return;
    }

    if (response.status === 403) {
      // User not paid
      alert('You need to complete your purchase to access this feature.');
      return;
    }

    if (!response.ok) {
      alert('Connection failed. Please retry.');
      return;
    }

    const data = await response.json();
    console.log('Chat response:', data.response); // JWT never logged
    updateChatUI(data.response);
  } catch (err) {
    alert('Connection failed. Please retry.');
    console.error('Chat error (details not logged):', err);
  }
}
```

**React Hook for JWT-Protected Chat** (reusable pattern):
```typescript
import { useEffect, useState } from 'react';

function useAuthenticatedChat() {
  const [jwt, setJwt] = useState<string | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('jwt');
    if (!token) {
      window.location.href = '/pricing';
      return;
    }
    setJwt(token);
  }, []);

  const sendChat = async (message: string) => {
    if (!jwt) return;

    const response = await fetch('/functions/v1/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    if (response.status === 401) {
      localStorage.removeItem('jwt');
      window.location.href = '/pricing';
      return;
    }

    if (response.status === 403) {
      throw new Error('Purchase required');
    }

    return response.json();
  };

  return { sendChat };
}

export default function ChatPage() {
  const { sendChat } = useAuthenticatedChat();
  const [input, setInput] = useState('');

  const handleSend = async () => {
    try {
      const { response } = await sendChat(input);
      console.log('Diagnostic response:', response);
    } catch (err) {
      alert(err.message || 'Connection failed.');
    }
  };

  return (
    <div>
      <textarea value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={handleSend}>Send</button>
    </div>
  );
}
```

**Security Best Practices**:
- JWT in Authorization header (not query params)
- JWT never console.logged
- localStorage (not sessionStorage) for cross-refresh persistence
- Immediate removal on 401
- HTTPS enforced (browser requirement for Authorization header)

## Dependencies

Requires:
- US-004 (Users created and can sign in)
- US-007 (Magic link callback sets JWT in localStorage)
- US-006 (Chat endpoint accepts JWT and validates)

## Related Specs

- Scope: **Section 5** (Frontend — Integrate JWT, JWT Storage, /chat Authorization Header)
- Brief: **Key Decisions** (Q-004: JWT extraction and validation)
