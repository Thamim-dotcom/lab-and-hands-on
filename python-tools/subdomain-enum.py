#!/usr/bin/env python3
"""
subdomain-enum.py — Subdomain Enumerator with DNS Resolution & HTTPS Validation
Author: Thamim Ansari | CEH v13 | github.com/Thamim-dotcom

DISCLAIMER: Only use on domains you own or have explicit written permission to test.
"""

import dns.resolver
import requests
import argparse
import sys
import threading
from queue import Queue
from datetime import datetime

found_subdomains = []
lock = threading.Lock()


def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║      Subdomain Enumerator — Thamim Ansari            ║
║      CEH v13 | github.com/Thamim-dotcom             ║
╚══════════════════════════════════════════════════════╝
""")


def check_subdomain(domain: str, sub: str, check_http: bool) -> None:
    """Resolve and optionally HTTP-probe a subdomain."""
    fqdn = f"{sub}.{domain}"
    try:
        answers = dns.resolver.resolve(fqdn, "A")
        ips = [r.address for r in answers]

        status = ""
        if check_http:
            for scheme in ["https", "http"]:
                try:
                    r = requests.get(f"{scheme}://{fqdn}", timeout=3, allow_redirects=True,
                                     headers={"User-Agent": "Mozilla/5.0"})
                    status = f"[{r.status_code}]"
                    break
                except Exception:
                    continue

        with lock:
            found_subdomains.append(fqdn)
            ip_str = ", ".join(ips)
            print(f"  [FOUND] {fqdn:<40} → {ip_str:<15} {status}")

    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
        pass
    except Exception:
        pass


def worker(domain: str, queue: Queue, check_http: bool) -> None:
    while not queue.empty():
        sub = queue.get()
        check_subdomain(domain, sub, check_http)
        queue.task_done()


def load_wordlist(path: str) -> list:
    with open(path, "r", errors="ignore") as f:
        return [line.strip() for line in f if line.strip()]


def main():
    banner()

    parser = argparse.ArgumentParser(description="Subdomain Enumerator")
    parser.add_argument("-d", "--domain", required=True, help="Target domain (e.g., example.com)")
    parser.add_argument("-w", "--wordlist", help="Wordlist path (default: built-in common list)")
    parser.add_argument("-T", "--threads", type=int, default=50, help="Thread count (default: 50)")
    parser.add_argument("--no-http", action="store_true", help="Skip HTTP probing")
    args = parser.parse_args()

    # Built-in common subdomain wordlist
    DEFAULT_SUBS = [
        "www", "mail", "ftp", "remote", "blog", "webmail", "server", "ns1", "ns2",
        "smtp", "secure", "vpn", "api", "dev", "staging", "test", "admin", "portal",
        "app", "cloud", "cdn", "static", "media", "images", "video", "m", "mobile",
        "shop", "store", "help", "support", "docs", "wiki", "git", "gitlab", "jenkins",
        "ci", "monitoring", "metrics", "grafana", "kibana", "elastic", "db", "database",
        "mysql", "postgres", "redis", "internal", "intranet", "corp", "office",
    ]

    subdomains = load_wordlist(args.wordlist) if args.wordlist else DEFAULT_SUBS

    print(f"[*] Domain    : {args.domain}")
    print(f"[*] Subdomains: {len(subdomains)}")
    print(f"[*] Threads   : {args.threads}")
    print(f"[*] HTTP Check: {'No' if args.no_http else 'Yes'}")
    print(f"[*] Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 65)

    queue = Queue()
    for sub in subdomains:
        queue.put(sub)

    threads = []
    for _ in range(min(args.threads, len(subdomains))):
        t = threading.Thread(target=worker, args=(args.domain, queue, not args.no_http))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

    print("-" * 65)
    print(f"\n[✓] Found {len(found_subdomains)} subdomain(s)")
    if found_subdomains:
        print("\n[*] Summary:")
        for s in sorted(found_subdomains):
            print(f"    {s}")


if __name__ == "__main__":
    main()
