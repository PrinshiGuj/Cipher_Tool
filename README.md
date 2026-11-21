# 🔐 Caesar & Vigenere Cipher Tool

A command-line tool written in **Python** that can **encrypt, decrypt and automatically break** the Caesar and Vigenere ciphers using frequency analysis.

Built as a cybersecurity (cryptography) project to show *how* classical ciphers work and *why* they are no longer safe.

---

## ✨ Features

| # | Feature | Cipher |
|---|---------|--------|
| 1 | Encrypt / Decrypt with a key | Caesar, Vigenere |
| 2 | Brute force (try all 25 shifts) | Caesar |
| 3 | Automatic cracking (chi-squared frequency analysis) | Caesar |
| 4 | Automatic cracking (Index of Coincidence + frequency analysis) | Vigenere |
| 5 | Letter frequency report (compared with English) | Both |
| 6 | Interactive menu **and** command-line mode | Both |

- Keeps upper/lower case, spaces, numbers and symbols unchanged
- No external libraries — uses only the Python standard library

---

## 📁 Project Structure

```
Project1_Cipher_Tool/
├── cipher_tool.py        # The main tool
├── sample_plaintext.txt  # 593-letter English test text
├── caesar_cipher.txt     # Sample text encrypted with Caesar key 7
├── vig_cipher.txt        # Sample text encrypted with Vigenere key SECURE
└── README.md
```

---

## ⚙️ Requirements

- Python **3.8 or higher**
- Works on Windows, Linux and macOS

Check your version:

```bash
python3 --version
```

---

## 🚀 How to Run

### Option 1 — Interactive menu

```bash
python3 cipher_tool.py
```

Then choose an option (1–8) and follow the prompts.

### Option 2 — Command line

| Task | Command |
|------|---------|
| Caesar encrypt | `python3 cipher_tool.py caesar-enc -t "Hello World" -k 3` |
| Caesar decrypt | `python3 cipher_tool.py caesar-dec -t "Khoor Zruog" -k 3` |
| Caesar brute force | `python3 cipher_tool.py caesar-brute -t "Khoor Zruog"` |
| Caesar auto-crack | `python3 cipher_tool.py caesar-crack -f caesar_cipher.txt` |
| Vigenere encrypt | `python3 cipher_tool.py vig-enc -t "Attack at Dawn!" -k LEMON` |
| Vigenere decrypt | `python3 cipher_tool.py vig-dec -t "Lxfopv ef Rnhr!" -k LEMON` |
| Vigenere auto-crack | `python3 cipher_tool.py vig-crack -f vig_cipher.txt` |
| Frequency report | `python3 cipher_tool.py freq -f caesar_cipher.txt -n 8` |

**Options:** `-t` text, `-f` read text from a file, `-k` key, `-n` number of letters to show (freq), `--max-len` maximum key length to test (vig-crack, default 12).

> On Windows, use `python` instead of `python3` if needed.

---

## 🖥️ Example Output

**Caesar encrypt / decrypt**

```
$ python3 cipher_tool.py caesar-enc -t "Hello World, Attack at Dawn!" -k 3
Khoor Zruog, Dwwdfn dw Gdzq!
```

**Caesar auto-crack**

```
$ python3 cipher_tool.py caesar-crack -f caesar_cipher.txt
[+] Most likely shift : 7
[+] Plaintext         : Cybersecurity is the practice of protecting systems, ...
```

**Vigenere auto-crack**

```
$ python3 cipher_tool.py vig-crack -f vig_cipher.txt
[*] Average Index of Coincidence per key length:
      length  5: 0.0450
      length  6: 0.0682  <-- chosen
      length  7: 0.0452
      ...
[+] Key length : 6
[+] Key found  : SECURE
[+] Plaintext  : Cybersecurity is the practice of protecting systems, ...
```

---

## 🧠 How the Cracking Works

### Caesar cipher
There are only 25 possible keys. The tool decrypts the text with every shift and scores each result against normal English letter frequencies using the **chi-squared test**. The lowest score is the most English-like text, so that shift is the key.

### Vigenere cipher
1. **Find the key length** — split the ciphertext into columns for each possible key length and calculate the **Index of Coincidence (IC)** of each. English text has IC ≈ **0.066**, random text ≈ **0.038**. The key length with a high IC is chosen (the smallest one close to the best score, so multiples of the real length are not picked by mistake).
2. **Find the key letters** — each column was encrypted with a single shift, so it is just a Caesar cipher. Crack each column with frequency analysis. The shifts together spell the key.

---

## ✅ Test Results

Tested on the 593-letter sample text:

| Test | Result |
|------|--------|
| Caesar key 7 | Recovered correctly |
| Vigenere key SECURE | Recovered correctly (key length 6) |
| Vigenere keys KEY, CODE, SECURE, LEMONS, HACKER, CRYPTOGRAPHY | All recovered correctly |
| Standard example ATTACK AT DAWN with key LEMON | Matches the known answer |

---

## ⚠️ Limitations

- Caesar auto-crack needs roughly **30+ letters** (a 15-letter text gave the wrong shift).
- Vigenere auto-crack needs roughly **250+ letters** (200 letters gave one wrong key letter; 120 letters failed).
- Designed for **English text** only.
- Only letters A–Z are encrypted; other characters are left as they are.

---

## 🔮 Future Improvements

- Add the Kasiski examination as a second way to find the Vigenere key length
- Use bigram / quadgram scoring so shorter texts can be cracked
- Support other languages
- Add a simple GUI or a frequency bar chart

---

## 📚 References

- [Caesar cipher — Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Vigenère cipher — Wikipedia](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher)
- [Index of coincidence — Wikipedia](https://en.wikipedia.org/wiki/Index_of_coincidence)
- [Letter frequency — Wikipedia](https://en.wikipedia.org/wiki/Letter_frequency)

---

## 👤 Author

**PRINS GAJERA** — Labmentix Cybersecurity Training Program

## ⚖️ Disclaimer

This project is for **educational purposes only**. Caesar and Vigenere are weak ciphers and must never be used to protect real data.
