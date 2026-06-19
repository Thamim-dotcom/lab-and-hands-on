#!/usr/bin/env python3
"""
port-scanner.py — Multi-threaded TCP/UDP Port Scanner with Banner Grabbing
Author: Thamim Ansari | CEH v13 | github.com/Thamim-dotcom
Usage: python3 port-scanner.py -t <target> [-p <ports>] [-T <threads>]

DISCLAIMER: For authorized use only. Only scan systems you own or have permission to scan.
"""

import socket
import threading
import argparse
import sys
from queue import Queue
from datetime import datetime

# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────
DEFAULT_THREADS = 100
DEFAULT_TIMEOUT = 1
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143,
                443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080, 8443]

open_ports = []
lock = threading.Lock()


def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║        Port Scanner v1.0 — Thamim Ansari             ║
║        CEH v13 | github.com/Thamim-dotcom            ║
║  ⚠  Use only on systems you own or have permission   ║
╚══════════════════════════════════════════════════════╝
""")


def grab_banner(host: str, port: int) -> str:
    """Attempt to grab service banner from open port."""
    try:
        s = socket.socket()
        s.settimeout(DEFAULT_TIMEOUT)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        return banner[:80] if banner else ""
    except Exception:
        return ""


def scan_port(host: str, port: int) -> None:
    """Scan a single TCP port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(DEFAULT_TIMEOUT)
        result = s.connect_ex((host, port))
        s.close()

        if result == 0:
            service = ""
            try:
                service = socket.getservbyport(port, "tcp")
            except Exception:
                service = "unknown"

            banner_text = grab_banner(host, port)

            with lock:
                open_ports.append(port)
                print(f"  [OPEN]  {port:>5}/tcp  {service:<15}  {banner_text}")
    except Exception:
        pass


def worker(host: str, queue: Queue) -> None:
    """Thread worker function."""
    while not queue.empty():
        port = queue.get()
        scan_port(host, port)
        queue.task_done()


def parse_ports(port_str: str) -> list:
    """Parse port string into list (e.g., '80,443', '1-1024', 'common')."""
    if port_str == "common":
        return COMMON_PORTS
    if "-" in port_str:
        start, end = port_str.split("-")
        return list(range(int(start), int(end) + 1))
    return [int(p.strip()) for p in port_str.split(",")]


def main():
    banner()

    parser = argparse.ArgumentParser(description="Multi-threaded Port Scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP or hostname")
    parser.add_argument("-p", "--ports", default="common",
                        help="Ports: 'common', '80,443', '1-1024' (default: common)")
    parser.add_argument("-T", "--threads", type=int, default=DEFAULT_THREADS,
                        help=f"Thread count (default: {DEFAULT_THREADS})")
    args = parser.parse_args()

    # Resolve hostname
    try:
        target_ip = socket.gethostbyname(args.target)
    except socket.gaierror:
        print(f"[!] Cannot resolve hostname: {args.target}")
        sys.exit(1)

    ports = parse_ports(args.ports)

    print(f"[*] Target    : {args.target} ({target_ip})")
    print(f"[*] Ports     : {len(ports)} ports")
    print(f"[*] Threads   : {args.threads}")
    print(f"[*] Started   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    print(f"  {'PORT':>5}  {'PROTO':<6}  {'SERVICE':<15}  BANNER")
    print("-" * 60)

    # Populate queue
    queue = Queue()
    for port in ports:
        queue.put(port)

    # Start threads
    threads = []
    for _ in range(min(args.threads, len(ports))):
        t = threading.Thread(target=worker, args=(target_ip, queue))
        t.daemon = True
        t.start()
        threads.append(t)

    queue.join()

    print("-" * 60)
    print(f"\n[✓] Scan complete. {len(open_ports)} open port(s) found.")
    print(f"[*] Finished  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
