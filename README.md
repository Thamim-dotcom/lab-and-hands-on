<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=32&duration=2800&pause=2000&color=00FF41&center=true&vCenter=true&width=700&lines=🛡️+Lab+%26+Hands-On+Security;Thamim+Ansari+|+CEH+v13;Ethical+Hacking+%7C+Python+%7C+CTF" alt="Typing SVG" />

<br/>

[![CEH v13](https://img.shields.io/badge/CEH%20v13-ECC0385921476-green?style=for-the-badge&logo=ec-council&logoColor=white)](https://www.eccouncil.org/)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-THM--L6596XPHA4-red?style=for-the-badge&logo=tryhackme&logoColor=white)](https://tryhackme.com/p/thamim-ansari)
[![Python](https://img.shields.io/badge/Python-Security%20Tools-blue?style=for-the-badge&logo=python&logoColor=white)](https://github.com/thamim-ansari)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

> **"Security is not a product, but a process. It is about understanding how things break so we can build them better."**  
> — Thamim Ansari

</div>

---

# 🧪 Lab & Hands-On — Thamim Ansari's Security Practicum

Welcome to my **cybersecurity lab and hands-on practice repository**. This is a living, growing collection of my real-world security experiments, CTF writeups, Python security tools, OWASP challenge walkthroughs, and ethical hacking labs — all sanitized and documented for learning purposes.

> ⚠️ **Responsible Use:** All content here is for **educational purposes only**. No live IPs, production credentials, active exploits, or private keys are published. See [`RESPONSIBLE_DISCLOSURE.md`](RESPONSIBLE_DISCLOSURE.md).

---

## 📋 Table of Contents

| # | Section | Description |
|---|---------|-------------|
| 1 | [🏁 CTF Writeups](#-ctf-writeups) | TryHackMe, HackTheBox, PicoCTF challenge solutions |
| 2 | [🌐 OWASP Top 10 Labs](#-owasp-top-10-labs) | Hands-on OWASP:2025 walkthroughs |
| 3 | [🐍 Python Security Tools](#-python-security-tools) | Custom-built recon, payload, and audit tools |
| 4 | [🔐 Privilege Escalation Labs](#-privilege-escalation-labs) | Linux & Windows privesc walkthroughs |
| 5 | [🌐 Web Exploitation Labs](#-web-exploitation-labs) | XSS, SQLi, IDOR, SSRF, and more |
| 6 | [🔍 Digital Forensics Labs](#-digital-forensics-labs) | Memory dumps, PCAP analysis, steganography |
| 7 | [🤖 Automation & Scripting](#-automation--scripting) | Security automation scripts and frameworks |
| 8 | [📚 Study Notes](#-study-notes) | CEH v13 and certification prep notes |
| 9 | [🛠️ Walkthroughs](#️-walkthroughs) | Step-by-step platform walkthroughs |

---

## 🏁 CTF Writeups

> Sanitized solutions from real CTF competitions. Each challenge folder contains the methodology, tools used, and key takeaways.

| Challenge | Platform | Category | Difficulty | Status |
|-----------|----------|----------|------------|--------|
| [EH101v13](ctf-writeups/EH101v13/) | TryHackMe | Web Upload → RCE → PATH Hijack | 🔴 Hard | ✅ Solved |
| [Diffanc](ctf-writeups/Diffanc/) | HackTheBox | Forensics → FTP → Sudo Misconfig | 🟠 Medium | ✅ Solved |
| [CyBox](ctf-writeups/CyBox/) | HackTheBox | SQLi → Container Escape → Root | 🔴 Hard | ✅ Solved |
| [WebShell101](ctf-writeups/WebShell101/) | PicoCTF | Web Exploitation | 🟢 Easy | ✅ Solved |
| [CryptoVault](ctf-writeups/CryptoVault/) | OverTheWire | Cryptography | 🟠 Medium | ✅ Solved |
| [AoC2025-Day1](ctf-writeups/AoC2025/) | TryHackMe | Advent of Cyber 2025 | 🟢 Easy | ✅ Solved |

---

## 🌐 OWASP Top 10 Labs

> Hands-on labs for each of the OWASP Top 10:2025 vulnerabilities using DVWA, WebGoat, and custom environments.

| # | Vulnerability | Lab | Writeup |
|---|--------------|-----|---------|
| A01 | Broken Access Control | [Lab →](owasp-labs/A01-broken-access-control/) | [Notes →](owasp-labs/A01-broken-access-control/README.md) |
| A02 | Cryptographic Failures | [Lab →](owasp-labs/A02-cryptographic-failures/) | [Notes →](owasp-labs/A02-cryptographic-failures/README.md) |
| A03 | Injection (SQLi, XSS, CMDi) | [Lab →](owasp-labs/A03-injection/) | [Notes →](owasp-labs/A03-injection/README.md) |
| A04 | Insecure Design | [Lab →](owasp-labs/A04-insecure-design/) | [Notes →](owasp-labs/A04-insecure-design/README.md) |
| A05 | Security Misconfiguration | [Lab →](owasp-labs/A05-security-misconfiguration/) | [Notes →](owasp-labs/A05-security-misconfiguration/README.md) |
| A06 | Vulnerable Components | [Lab →](owasp-labs/A06-vulnerable-components/) | [Notes →](owasp-labs/A06-vulnerable-components/README.md) |
| A07 | Auth Failures | [Lab →](owasp-labs/A07-auth-failures/) | [Notes →](owasp-labs/A07-auth-failures/README.md) |
| A08 | Software & Data Integrity | [Lab →](owasp-labs/A08-software-integrity/) | [Notes →](owasp-labs/A08-software-integrity/README.md) |
| A09 | Logging & Monitoring Failures | [Lab →](owasp-labs/A09-logging-failures/) | [Notes →](owasp-labs/A09-logging-failures/README.md) |
| A10 | SSRF | [Lab →](owasp-labs/A10-ssrf/) | [Notes →](owasp-labs/A10-ssrf/README.md) |

---

## 🐍 Python Security Tools

> Custom-built Python tools for ethical hacking and security automation.

| Tool | Description | Category |
|------|-------------|----------|
| [port-scanner.py](python-tools/port-scanner.py) | Multi-threaded TCP/UDP port scanner with banner grabbing | Recon |
| [subdomain-enum.py](python-tools/subdomain-enum.py) | Subdomain enumerator with DNS resolution and HTTPS validation | Recon |
| [hash-cracker.py](python-tools/hash-cracker.py) | Dictionary-based hash cracker (MD5, SHA1, SHA256, bcrypt) | Password |
| [payload-gen.py](python-tools/payload-gen.py) | XSS/SQLi payload generator with WAF bypass templates | Exploitation |
| [log-analyzer.py](python-tools/log-analyzer.py) | Web server log analyzer for anomaly detection | Defensive |
| [ssl-checker.py](python-tools/ssl-checker.py) | SSL/TLS certificate auditor and weak cipher detector | Audit |

---

## 🔐 Privilege Escalation Labs

> Documented privesc chains using common misconfigurations found in CTFs and real engagements.

| Lab | OS | Vector | Writeup |
|-----|----|--------|---------|
| [SUID Binaries](privesc-labs/linux/suid-binaries/) | Linux | SUID find/bash/cp abuse | [README](privesc-labs/linux/suid-binaries/README.md) |
| [Cron Jobs](privesc-labs/linux/cron-jobs/) | Linux | Writable cron script injection | [README](privesc-labs/linux/cron-jobs/README.md) |
| [Sudo Misconfig](privesc-labs/linux/sudo-misconfig/) | Linux | Sudo -l exploit vectors | [README](privesc-labs/linux/sudo-misconfig/README.md) |
| [PATH Hijacking](privesc-labs/linux/path-hijacking/) | Linux | Relative PATH in scripts | [README](privesc-labs/linux/path-hijacking/README.md) |
| [NFS No Root Squash](privesc-labs/linux/nfs-no-root-squash/) | Linux | NFS SUID mount | [README](privesc-labs/linux/nfs-no-root-squash/README.md) |

---

## 🌐 Web Exploitation Labs

> Hands-on web attack scenarios with step-by-step exploitation walkthroughs.

| Lab | Vulnerability | Target | Writeup |
|-----|--------------|--------|---------|
| [SQLi Lab](web-exploitation/sqli-lab/) | SQL Injection (Union, Blind, Time-based) | DVWA | [README](web-exploitation/sqli-lab/README.md) |
| [XSS Lab](web-exploitation/xss-lab/) | Reflected, Stored, DOM XSS | WebGoat | [README](web-exploitation/xss-lab/README.md) |
| [IDOR Lab](web-exploitation/idor-lab/) | Insecure Direct Object Reference | Custom App | [README](web-exploitation/idor-lab/README.md) |
| [SSRF Lab](web-exploitation/ssrf-lab/) | Server-Side Request Forgery | Custom App | [README](web-exploitation/ssrf-lab/README.md) |
| [File Upload RCE](web-exploitation/file-upload-rce/) | Unrestricted File Upload → RCE | DVWA | [README](web-exploitation/file-upload-rce/README.md) |
| [JWT Attacks](web-exploitation/jwt-attacks/) | JWT None Algorithm & Secret Brute | Custom App | [README](web-exploitation/jwt-attacks/README.md) |

---

## 🔍 Digital Forensics Labs

> Memory analysis, PCAP investigation, and steganography exercises.

| Lab | Type | Tools Used | Writeup |
|-----|------|-----------|---------|
| [Memory Dump Analysis](forensics-labs/memory-dump/) | Volatile Memory | Volatility3, strings, grep | [README](forensics-labs/memory-dump/README.md) |
| [PCAP Investigation](forensics-labs/pcap-analysis/) | Network Forensics | Wireshark, tshark, tcpdump | [README](forensics-labs/pcap-analysis/README.md) |
| [Steganography](forensics-labs/steganography/) | Image/Audio Stego | steghide, exiftool, binwalk | [README](forensics-labs/steganography/README.md) |
| [Log Analysis](forensics-labs/log-analysis/) | DFIR | grep, awk, python | [README](forensics-labs/log-analysis/README.md) |

---

## 🤖 Automation & Scripting

> Scripts that automate security tasks and improve efficiency.

| Script | Purpose | Language |
|--------|---------|---------|
| [recon-auto.sh](automation/recon-auto.sh) | Automated recon pipeline (nmap → gobuster → nikto) | Bash |
| [vuln-scanner.py](automation/vuln-scanner.py) | CVE-based vulnerability scanner using NVD API | Python |
| [report-gen.py](automation/report-gen.py) | Auto-generate pentest reports from scan outputs | Python |
| [ssh-brute.py](automation/ssh-brute.py) | Controlled SSH brute-force for lab environments | Python |

---

## 📚 Study Notes

> Organized notes from CEH v13, TryHackMe learning paths, and self-study.

| Topic | Notes | Status |
|-------|-------|--------|
| [CEH v13 Module Summary](study-notes/ceh-v13/) | All 20 modules condensed | ✅ Complete |
| [Networking Fundamentals](study-notes/networking/) | TCP/IP, OSI, Subnetting | ✅ Complete |
| [Web Security Basics](study-notes/web-security/) | HTTP, Cookies, Sessions, Auth | ✅ Complete |
| [Cryptography Basics](study-notes/cryptography/) | Symmetric, Asymmetric, Hashing | ✅ Complete |
| [Linux Fundamentals](study-notes/linux/) | Commands, Permissions, Scripting | ✅ Complete |

---

## 🛠️ Walkthroughs

> Detailed step-by-step walkthroughs of platforms, challenges, and tools.

| Walkthrough | Platform | Description |
|-------------|----------|-------------|
| [TryHackMe Advent of Cyber 2025](walkthroughs/THM-AoC-2025/) | TryHackMe | Full 25-day challenge walkthrough |
| [CEH v13 Exam Journey](walkthroughs/CEH-v13-journey/) | EC-Council | My path from zero to CEH certified |
| [VulnForge Elite — Build Log](walkthroughs/vulnforge-elite-build/) | Personal | End-to-end VAPT tool development |
| [NEXUS Platform — Build Log](walkthroughs/nexus-platform-build/) | Personal | Industrial diagnostic app build journey |
| [DVWA Setup & Full Exploit](walkthroughs/dvwa-full-walkthrough/) | DVWA | Complete DVWA exploitation guide |
| [Metasploit Framework Basics](walkthroughs/metasploit-basics/) | Lab | MSF from setup to shell |
| [Burp Suite Pro Workflow](walkthroughs/burp-suite-workflow/) | BurpSuite | Complete web testing workflow |

---

## 🗂️ Repository Structure

```
lab-and-hands-on/
├── 📁 ctf-writeups/
│   ├── EH101v13/           # THM: Web Upload → RCE → PATH Hijack
│   ├── Diffanc/            # HTB: Forensics → FTP → Sudo Misconfig
│   ├── CyBox/              # HTB: SQLi → Container Escape → Root
│   ├── WebShell101/        # PicoCTF: Web Exploitation
│   ├── CryptoVault/        # OTW: Cryptography
│   └── AoC2025/            # THM: Advent of Cyber 2025
├── 📁 owasp-labs/
│   ├── A01-broken-access-control/
│   ├── A02-cryptographic-failures/
│   ├── A03-injection/
│   └── ... (all 10 categories)
├── 📁 python-tools/
│   ├── port-scanner.py
│   ├── subdomain-enum.py
│   └── ...
├── 📁 privesc-labs/
│   └── linux/
│       ├── suid-binaries/
│       ├── cron-jobs/
│       └── ...
├── 📁 web-exploitation/
│   ├── sqli-lab/
│   ├── xss-lab/
│   └── ...
├── 📁 forensics-labs/
│   ├── memory-dump/
│   ├── pcap-analysis/
│   └── ...
├── 📁 automation/
│   ├── recon-auto.sh
│   └── ...
├── 📁 study-notes/
│   ├── ceh-v13/
│   └── ...
├── 📁 walkthroughs/
│   ├── THM-AoC-2025/
│   ├── CEH-v13-journey/
│   └── ...
├── RESPONSIBLE_DISCLOSURE.md
├── CONTRIBUTING.md
└── README.md
```

---

## 🏅 Achievements & Certifications

<div align="center">

| Certification | Issuer | ID | Year |
|--------------|--------|----|------|
| **Certified Ethical Hacker (CEH v13)** | EC-Council (ANAB) | ECC0385921476 | 2025 |
| **Advent of Cyber 2025** | TryHackMe | THM-L6596XPHA4 | 2025 |

</div>

---

## 📊 Stats & Progress

<div align="center">

![CTF Challenges](https://img.shields.io/badge/CTF%20Challenges%20Solved-50%2B-brightgreen?style=flat-square)
![TryHackMe](https://img.shields.io/badge/TryHackMe-Top%205%25-red?style=flat-square&logo=tryhackme)
![Python Tools](https://img.shields.io/badge/Python%20Security%20Tools-6%2B-blue?style=flat-square&logo=python)
![OWASP Labs](https://img.shields.io/badge/OWASP%20Labs%20Completed-10%2F10-orange?style=flat-square)

</div>

---

## 🤝 Connect

<div align="center">

[![Portfolio](https://img.shields.io/badge/Portfolio-thamim--ansari-00ff41?style=for-the-badge&logo=github&logoColor=white)](https://github.com/thamim-ansari)
[![GitHub](https://img.shields.io/badge/GitHub-Thamim--dotcom-black?style=for-the-badge&logo=github)](https://github.com/Thamim-dotcom)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-thamim--ansari-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/thamim-ansari)
[![TryHackMe](https://img.shields.io/badge/TryHackMe-Profile-red?style=for-the-badge&logo=tryhackme)](https://tryhackme.com/p/thamim-ansari)

</div>

---

<div align="center">
<sub>⭐ If this helped you learn something, give it a star! | Made with ❤️ and ☕ by Thamim Ansari</sub>
</div>
