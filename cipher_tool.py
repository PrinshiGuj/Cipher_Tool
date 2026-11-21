#!/usr/bin/env python3
"""
Caesar and Vigenere Cipher Tool
--------------------------------
Features:
  1. Caesar encrypt / decrypt
  2. Caesar brute force (all 25 shifts)
  3. Caesar automatic cracking (frequency analysis, chi-squared)
  4. Vigenere encrypt / decrypt
  5. Vigenere automatic cracking (Index of Coincidence + frequency analysis)
  6. Letter frequency report

Run without arguments for the interactive menu, or use the sub-commands:
  python3 cipher_tool.py caesar-enc  -t "HELLO" -k 3
  python3 cipher_tool.py vig-crack   -f ciphertext.txt
"""
import argparse
import string
import sys
from collections import Counter

ALPHA = string.ascii_uppercase

# Standard English letter frequencies (percent), A..Z
ENGLISH_FREQ = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966,
                0.153, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987,
                6.327, 9.056, 2.758, 0.978, 2.360, 0.150, 1.974, 0.074]


# ---------------------------------------------------------------- Caesar ----
def caesar_shift(text, shift):
    """Shift every letter by `shift` positions; keep case, digits and symbols."""
    out = []
    for ch in text:
        if ch.isalpha() and ch.isascii():
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            out.append(ch)
    return "".join(out)


def caesar_encrypt(text, key):
    return caesar_shift(text, key)


def caesar_decrypt(text, key):
    return caesar_shift(text, -key)


def caesar_bruteforce(text):
    """Return a list of (shift, decrypted_text) for all 25 possible keys."""
    return [(k, caesar_decrypt(text, k)) for k in range(1, 26)]


# ------------------------------------------------------------- Frequency ----
def clean(text):
    """Keep only A-Z letters, upper-cased."""
    return "".join(c for c in text.upper() if c in ALPHA)


def letter_frequency(text):
    """Return {letter: percent} for A..Z."""
    letters = clean(text)
    total = len(letters) or 1
    counts = Counter(letters)
    return {c: counts.get(c, 0) * 100.0 / total for c in ALPHA}


def chi_squared(text):
    """Chi-squared distance between text and English. Lower = more English-like."""
    letters = clean(text)
    n = len(letters)
    if n == 0:
        return float("inf")
    counts = Counter(letters)
    score = 0.0
    for i, c in enumerate(ALPHA):
        expected = ENGLISH_FREQ[i] * n / 100.0
        score += (counts.get(c, 0) - expected) ** 2 / expected
    return score


def caesar_crack(text):
    """Pick the shift whose plaintext looks most like English."""
    best = min(range(26), key=lambda k: chi_squared(caesar_decrypt(text, k)))
    return best, caesar_decrypt(text, best)


# --------------------------------------------------------------- Vigenere ---
def _key_shifts(key):
    key = clean(key)
    if not key:
        raise ValueError("Key must contain at least one letter (A-Z).")
    return [ord(c) - 65 for c in key]


def vigenere_process(text, key, decrypt=False):
    shifts = _key_shifts(key)
    out, i = [], 0
    for ch in text:
        if ch.isalpha() and ch.isascii():
            s = shifts[i % len(shifts)]
            if decrypt:
                s = -s
            base = ord('A') if ch.isupper() else ord('a')
            out.append(chr((ord(ch) - base + s) % 26 + base))
            i += 1          # key advances only on letters
        else:
            out.append(ch)
    return "".join(out)


def vigenere_encrypt(text, key):
    return vigenere_process(text, key, decrypt=False)


def vigenere_decrypt(text, key):
    return vigenere_process(text, key, decrypt=True)


def index_of_coincidence(text):
    letters = clean(text)
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def guess_key_length(cipher, max_len=12):
    """Average IC of each column; English ~0.066, random ~0.038.
    Pick the smallest length whose IC is close to the best score
    (so multiples of the true length are not preferred)."""
    letters = clean(cipher)
    scores = {}
    for L in range(1, max_len + 1):
        cols = [letters[i::L] for i in range(L)]
        scores[L] = sum(index_of_coincidence(c) for c in cols) / L
    best = max(scores.values())
    for L in range(1, max_len + 1):
        if scores[L] >= best - 0.008:
            return L, scores
    return 1, scores


def vigenere_crack(cipher, max_len=12):
    """Return (key, plaintext, key_length, ic_scores)."""
    letters = clean(cipher)
    L, scores = guess_key_length(cipher, max_len)
    key = ""
    for i in range(L):
        column = letters[i::L]
        shift, _ = caesar_crack(column)
        key += ALPHA[shift]
    return key, vigenere_decrypt(cipher, key), L, scores


# ---------------------------------------------------------------- Output ----
def print_frequency(text, top=26):
    freq = letter_frequency(text)
    ranked = sorted(freq.items(), key=lambda kv: -kv[1])[:top]
    print(f"{'Letter':<8}{'Count %':<10}{'English %':<11}Graph")
    for c, pct in ranked:
        eng = ENGLISH_FREQ[ord(c) - 65]
        print(f"{c:<8}{pct:<10.2f}{eng:<11.2f}{'#' * int(round(pct))}")


def read_input(args):
    if getattr(args, "file", None):
        with open(args.file, "r", encoding="utf-8") as f:
            return f.read()
    if getattr(args, "text", None) is not None:
        return args.text
    print("Error: give text with -t or a file with -f", file=sys.stderr)
    sys.exit(1)


# ------------------------------------------------------------------ CLI -----
def build_parser():
    p = argparse.ArgumentParser(description="Caesar and Vigenere Cipher Tool")
    sub = p.add_subparsers(dest="cmd")

    def add(name, help_, key=None):
        sp = sub.add_parser(name, help=help_)
        sp.add_argument("-t", "--text", help="input text")
        sp.add_argument("-f", "--file", help="read input text from file")
        if key == "int":
            sp.add_argument("-k", "--key", type=int, required=True, help="shift 0-25")
        elif key == "str":
            sp.add_argument("-k", "--key", required=True, help="keyword (letters)")
        return sp

    add("caesar-enc", "Caesar encrypt", "int")
    add("caesar-dec", "Caesar decrypt", "int")
    add("caesar-brute", "Caesar brute force (all shifts)")
    add("caesar-crack", "Caesar auto-crack by frequency analysis")
    add("vig-enc", "Vigenere encrypt", "str")
    add("vig-dec", "Vigenere decrypt", "str")
    sp = add("vig-crack", "Vigenere auto-crack")
    sp.add_argument("--max-len", type=int, default=12, help="max key length to test")
    sp = add("freq", "Letter frequency report")
    sp.add_argument("-n", "--top", type=int, default=26, help="show top N letters")
    return p


def run_command(args):
    text = read_input(args)
    c = args.cmd
    if c == "caesar-enc":
        print(caesar_encrypt(text, args.key))
    elif c == "caesar-dec":
        print(caesar_decrypt(text, args.key))
    elif c == "caesar-brute":
        for k, pt in caesar_bruteforce(text):
            print(f"Shift {k:>2}: {pt}")
    elif c == "caesar-crack":
        k, pt = caesar_crack(text)
        print(f"[+] Most likely shift : {k}")
        print(f"[+] Plaintext         : {pt}")
    elif c == "vig-enc":
        print(vigenere_encrypt(text, args.key))
    elif c == "vig-dec":
        print(vigenere_decrypt(text, args.key))
    elif c == "vig-crack":
        key, pt, L, scores = vigenere_crack(text, args.max_len)
        print("[*] Average Index of Coincidence per key length:")
        for l, s in scores.items():
            print(f"      length {l:>2}: {s:.4f}{'  <-- chosen' if l == L else ''}")
        print(f"[+] Key length : {L}")
        print(f"[+] Key found  : {key}")
        print(f"[+] Plaintext  : {pt}")
    elif c == "freq":
        print_frequency(text, args.top)


def menu():
    options = """
==============================================
   CAESAR & VIGENERE CIPHER TOOL
==============================================
 1. Caesar  - Encrypt
 2. Caesar  - Decrypt
 3. Caesar  - Brute force
 4. Caesar  - Auto crack (frequency analysis)
 5. Vigenere - Encrypt
 6. Vigenere - Decrypt
 7. Vigenere - Auto crack
 8. Letter frequency report
 0. Exit
"""
    while True:
        print(options)
        choice = input("Choose option: ").strip()
        if choice == "0":
            print("Bye!")
            return
        if choice not in list("12345678"):
            print("Invalid option.")
            continue
        text = input("Enter text: ")
        try:
            if choice == "1":
                print("Result:", caesar_encrypt(text, int(input("Shift (0-25): "))))
            elif choice == "2":
                print("Result:", caesar_decrypt(text, int(input("Shift (0-25): "))))
            elif choice == "3":
                for k, pt in caesar_bruteforce(text):
                    print(f"Shift {k:>2}: {pt}")
            elif choice == "4":
                k, pt = caesar_crack(text)
                print(f"Most likely shift: {k}\nPlaintext: {pt}")
            elif choice == "5":
                print("Result:", vigenere_encrypt(text, input("Keyword: ")))
            elif choice == "6":
                print("Result:", vigenere_decrypt(text, input("Keyword: ")))
            elif choice == "7":
                key, pt, L, _ = vigenere_crack(text)
                print(f"Key length: {L}\nKey: {key}\nPlaintext: {pt}")
            elif choice == "8":
                print_frequency(text)
        except ValueError as e:
            print("Error:", e)


if __name__ == "__main__":
    parser = build_parser()
    args = parser.parse_args()
    if args.cmd is None:
        menu()
    else:
        run_command(args)
