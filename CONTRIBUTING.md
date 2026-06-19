# 🤝 Contributing to Lab & Hands-On

Thank you for your interest in contributing! This repository contains educational cybersecurity content and follows strict responsible disclosure standards.

## 📋 Contribution Guidelines

### What We Accept

✅ New CTF writeups from public platforms (TryHackMe, HackTheBox, PicoCTF)  
✅ OWASP lab walkthroughs using intentionally vulnerable apps  
✅ Educational Python security tools  
✅ Study notes and cheat sheets  
✅ Bug fixes in existing writeups  

### What We DON'T Accept

❌ Real credentials, API keys, or tokens  
❌ Active exploits against live systems  
❌ Doxxing or PII of third parties  
❌ Malware samples without proper sandboxing notes  
❌ Content encouraging illegal activity  

## 🚀 How to Contribute

1. **Fork** this repository
2. **Create a branch**: `git checkout -b feature/my-ctf-writeup`
3. **Write your content** following the existing format
4. **Sanitize** all IPs, credentials, flags
5. **Submit a PR** with a clear description

## 📝 Writeup Format

Follow the structure in existing writeups:
```
# 🏁 CTF Writeup: [Challenge Name]

**Platform:** ...
**Difficulty:** ...
**Category:** ...
**Status:** ✅ Solved

## 📝 Summary
## 🔍 Phase 1: Reconnaissance
## 💥 Phase 2: Exploitation
## 🔼 Phase 3: Privilege Escalation
## 🚩 Flags (REDACTED)
## 🧠 Key Takeaways
## 🛡️ Mitigations
```

## ✅ Sanitization Checklist

Before submitting, verify:
- [ ] No real IP addresses (use `TARGET_IP` or `10.10.x.x`)
- [ ] No real flags (replace with `[REDACTED]`)
- [ ] No production credentials
- [ ] No private keys or certificates
- [ ] No personally identifiable information

## 📜 License

All contributions are licensed under [MIT License](LICENSE).

---

*Questions? Open an issue or reach out on [LinkedIn](https://linkedin.com/in/thamim-ansari)*
