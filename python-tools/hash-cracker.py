#!/usr/bin/env python3
"""
hash-cracker.py — Dictionary-based Hash Cracker (MD5, SHA1, SHA256, bcrypt)
Author: Thamim Ansari | CEH v13 | github.com/Thamim-dotcom

DISCLAIMER: Only use on hashes you own or have explicit permission to test.
"""

import hashlib
import argparse
import sys
import time
from pathlib import Path

try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False


def banner():
    print("""
╔══════════════════════════════════════════════════════╗
║        Hash Cracker v1.0 — Thamim Ansari             ║
║        CEH v13 | github.com/Thamim-dotcom            ║
║  Supported: MD5, SHA1, SHA256, SHA512, bcrypt        ║
╚══════════════════════════════════════════════════════╝
""")


def detect_hash_type(hash_str: str) -> str:
    """Auto-detect hash type based on length."""
    length_map = {
        32: "md5",
        40: "sha1",
        64: "sha256",
        128: "sha512",
    }
    if hash_str.startswith("$2b$") or hash_str.startswith("$2a$"):
        return "bcrypt"
    return length_map.get(len(hash_str), "unknown")


def compute_hash(word: str, algorithm: str) -> str:
    """Compute hash for a given word and algorithm."""
    encoded = word.encode("utf-8")
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    if algorithm in algorithms:
        return algorithms[algorithm](encoded).hexdigest()
    return ""


def crack_hash(target_hash: str, wordlist_path: str, algorithm: str) -> str | None:
    """Attempt to crack hash using dictionary attack."""
    wordlist = Path(wordlist_path)
    if not wordlist.exists():
        print(f"[!] Wordlist not found: {wordlist_path}")
        sys.exit(1)

    start = time.time()
    attempts = 0

    with open(wordlist_path, "r", errors="ignore") as f:
        for line in f:
            word = line.strip()
            if not word:
                continue

            attempts += 1

            if algorithm == "bcrypt":
                if not BCRYPT_AVAILABLE:
                    print("[!] bcrypt not installed. Run: pip install bcrypt")
                    sys.exit(1)
                try:
                    if bcrypt.checkpw(word.encode(), target_hash.encode()):
                        elapsed = time.time() - start
                        print(f"\n[✓] CRACKED! Hash: {target_hash}")
                        print(f"    Password : {word}")
                        print(f"    Attempts : {attempts:,}")
                        print(f"    Time     : {elapsed:.2f}s")
                        return word
                except Exception:
                    continue
            else:
                computed = compute_hash(word, algorithm)
                if computed == target_hash.lower():
                    elapsed = time.time() - start
                    print(f"\n[✓] CRACKED! Hash: {target_hash}")
                    print(f"    Password : {word}")
                    print(f"    Attempts : {attempts:,}")
                    print(f"    Time     : {elapsed:.2f}s")
                    return word

            if attempts % 100000 == 0:
                elapsed = time.time() - start
                rate = attempts / elapsed if elapsed > 0 else 0
                print(f"[*] Progress: {attempts:,} attempts | {rate:,.0f} h/s", end="\r")

    elapsed = time.time() - start
    print(f"\n[✗] Not found in wordlist after {attempts:,} attempts ({elapsed:.2f}s)")
    return None


def main():
    banner()

    parser = argparse.ArgumentParser(description="Dictionary Hash Cracker")
    parser.add_argument("-H", "--hash", required=True, help="Target hash to crack")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to wordlist file")
    parser.add_argument("-a", "--algorithm", choices=["md5", "sha1", "sha256", "sha512", "bcrypt", "auto"],
                        default="auto", help="Hash algorithm (default: auto-detect)")
    args = parser.parse_args()

    algorithm = args.algorithm
    if algorithm == "auto":
        algorithm = detect_hash_type(args.hash)
        if algorithm == "unknown":
            print(f"[!] Cannot auto-detect algorithm for hash length {len(args.hash)}")
            print("[!] Specify algorithm with -a flag")
            sys.exit(1)
        print(f"[*] Auto-detected: {algorithm.upper()}")

    print(f"[*] Hash      : {args.hash}")
    print(f"[*] Algorithm : {algorithm.upper()}")
    print(f"[*] Wordlist  : {args.wordlist}")
    print("-" * 55)

    crack_hash(args.hash, args.wordlist, algorithm)


if __name__ == "__main__":
    main()
