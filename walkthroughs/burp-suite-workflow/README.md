# 🛠️ Walkthrough: Burp Suite Pro — Complete Web Testing Workflow

**Tool:** Burp Suite Professional  
**Version:** 2025.x  
**Category:** Web Application Security Testing  
**Status:** ✅ Complete

---

## 📝 Overview

This walkthrough covers my complete Burp Suite workflow for web application penetration testing — from initial setup and configuration through to comprehensive vulnerability discovery.

---

## 🏗️ Phase 1: Setup & Configuration

### Browser Proxy Setup

```
Burp Settings:
- Listen on: 127.0.0.1:8080
- Certificate: Export and install Burp's CA cert in browser

Firefox FoxyProxy Setup:
- Pattern: *
- Proxy: 127.0.0.1:8080
- Toggle: On when testing, Off otherwise
```

### Target Scope Configuration

```
Target → Scope → Add:
- Protocol: http/https
- Host: target.example.com
- Exclude: logout, assets/*, cdn.*
```

---

## 🔍 Phase 2: Reconnaissance with Spider/Crawl

### Passive Crawl

```
Target → Site map → Right-click target → Passively scan this host

Results:
- Full site map with all discovered URLs
- Parameter inventory
- Cookie analysis
- Hidden directories
```

### Active Crawl (Burp Scanner)

```
Dashboard → New Scan → Crawl → Set scope
Burp will:
1. Follow all links
2. Submit forms with fuzzing payloads
3. Identify JavaScript endpoints
4. Map API endpoints
```

---

## 💥 Phase 3: Manual Testing with Repeater

### Intercepting Requests

```
Proxy → Intercept → Turn on
Browse to target → Request captured
Right-click → Send to Repeater
```

### SQL Injection Testing in Repeater

```
Modify parameter value:
- id=1         → Normal response
- id=1'        → SQL error? → SQLi candidate!
- id=1 OR 1=1  → More results? → Confirmed
- id=1 UNION SELECT NULL,NULL -- -  → Column count
```

### XSS Testing in Repeater

```
Inject into each parameter:
<script>alert(1)</script>
"><script>alert(1)</script>
'><img src=x onerror=alert(1)>
javascript:alert(1)
```

---

## 🎯 Phase 4: Automated Scanning

### Running Active Scan

```
Right-click any request → Scan
OR
Dashboard → New Scan → Active Scan
Set scope, start scan

Key findings to look for:
✅ SQL injection
✅ XSS (reflected, stored, DOM)
✅ SSRF
✅ Path traversal
✅ Command injection
✅ Open redirect
```

---

## 🔐 Phase 5: Authentication Testing

### Brute Force with Intruder

```
Capture login request
Send to Intruder

Positions tab:
- Clear all positions
- Select password value → Add §
- §wrong_password§

Payloads tab:
- Type: Simple list
- Load: /usr/share/wordlists/common-passwords.txt

Attack!
Look for different status code or response length
```

### Session Token Analysis

```
Proxy → HTTP history → Find login responses
Look for Set-Cookie header
Send cookie to Sequencer → Live capture
Burp analyses randomness of token
Weak tokens (predictable) = Session fixation risk
```

---

## 🔧 Phase 6: Advanced Techniques

### CSRF Testing

```
Find state-changing action (password change, profile update)
Check for:
1. Anti-CSRF token in form? 
2. Same-site cookie attribute?
3. Referer header checked?

If none → CSRF vulnerability!

Burp → Right-click request → Engagement tools → Generate CSRF PoC
Burp auto-generates the malicious HTML page
```

### JWT Testing

```
Install Burp Extension: JWT Editor

Intercept request with JWT
Send to JWT Editor tab

Tests:
1. "none" algorithm: Remove signature
2. Weak secret: Send to brute-force
3. Key confusion: Use RS256 public key as HS256 secret
```

### SSRF Testing

```
Find any URL parameter the server fetches:
- ?url=http://...
- ?image=http://...
- ?redirect=http://...
- Webhook URLs
- XML with external entities

Test payloads:
http://localhost/
http://169.254.169.254/  (AWS metadata)
http://127.0.0.1:6379/   (Redis)
http://127.0.0.1:27017/  (MongoDB)
file:///etc/passwd
```

---

## 📊 Testing Checklist

```
□ Authentication
  □ Brute force protection
  □ Account lockout
  □ Password reset flow
  □ Multi-factor authentication
  □ Session token entropy

□ Authorization
  □ Horizontal privilege escalation (IDOR)
  □ Vertical privilege escalation
  □ Function-level access control

□ Input Validation
  □ SQL injection
  □ XSS (reflected, stored, DOM)
  □ Command injection
  □ Path traversal
  □ XXE (XML injection)
  □ SSRF
  □ Template injection

□ Business Logic
  □ Price manipulation
  □ Quantity manipulation
  □ Workflow bypass
  □ Race conditions

□ API Security
  □ Exposed endpoints
  □ Mass assignment
  □ Rate limiting
  □ Authentication on all endpoints
```

---

## 🧠 Key Burp Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+I` | Send to Intruder |
| `Ctrl+R` | Send to Repeater |
| `Ctrl+S` | Save (in Repeater) |
| `Ctrl+Space` | Send request |
| `Ctrl+Z` | Undo |
| `F12` | Forward request (Intercept) |

---

## 🛡️ Reporting in Burp

```
Dashboard → Issues (from scanner)
Right-click any issue → Report issue

Include in report:
- Severity (Critical/High/Medium/Low/Info)
- Confidence (Certain/Firm/Tentative)
- Evidence screenshots
- HTTP request/response
- Remediation recommendations
```

---

*This walkthrough reflects techniques learned in authorized lab environments and CEH v13 training.*
