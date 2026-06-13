# 🧙 Gandalf's File Integrity Monitor

A Python cybersecurity tool that monitors files and directories for unauthorized 
changes — detecting new files, modifications, and deletions in real time with 
SHA256 hashing. Delivered with alerts from Gandalf the Grey.
Built as part of a cybersecurity learning journey.

---

## 🔐 What is a File Integrity Monitor?

When attackers compromise a system they almost always:
- **Drop malware** — new files appear where they shouldn't
- **Modify system files** — alter existing files to hide their presence
- **Delete logs** — remove evidence of their activity

A File Integrity Monitor (FIM) catches all three. It takes a **baseline snapshot** 
of all files using SHA256 hashes, then continuously compares the current state 
against that baseline — alerting on any change, no matter how small.

Real enterprise tools like **Tripwire** and **OSSEC** are sophisticated FIMs 
used by companies worldwide. This is a simplified version of those tools.

---

## ⚡ Features

| Feature | Description |
|---|---|
| **Baseline Snapshot** | Records SHA256 hash, size, and timestamp of every file |
| **Real Time Monitoring** | Continuously scans and compares against baseline |
| **New File Detection** | Alerts when unauthorized files appear |
| **Modification Detection** | Catches file tampering via hash comparison |
| **Deletion Detection** | Flags when files are removed |
| **Security Logging** | Writes all events to `fim_log.txt` with timestamps |
| **Recursive Scanning** | Monitors all files in subfolders too |
| **Chunked File Reading** | Handles large files efficiently without memory issues |
| **Gandalf Mode** | In-character alerts from Gandalf for every security event |

---

## 🛠️ Built With

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

---

## 🚀 Usage

```bash
python fileintegrity.py
```

### Workflow
Choose option 1 — create baseline snapshot of watched folder
Choose option 2 — start monitoring
Any changes trigger instant alerts
Choose option 3 — view full security event log

### Example Output

👁️  MONITORING STARTED

📁 Watching: watched_folder

⏱️  Checking every 10 seconds

📋 Baseline has 2 files
🔍 Check #12 at 17:54:35...

⚠️  NEW FILE DETECTED: suspicious.txt

🧙 'Something has crept in where it was not before — a new file stirs!'
⚡ FILE MODIFIED: secret.txt

Old hash: 9826e31a3e6d2235...

New hash: 1ded2a2f3ec4617f...

🧙 'A file has been altered! Even the smallest change leaves a trace!'
🚨 FILE DELETED: important.txt

🧙 'A file is missing! Someone seeks to cover their tracks!'

---

## 🔑 Key Concepts Learned

- **SHA256 file hashing** — fingerprinting files so any change is detectable
- **Chunked file reading** — reading files in 8KB pieces for memory efficiency
- **JSON** — storing and loading structured baseline data
- **os.walk()** — recursively scanning directories and subdirectories
- **Set operations** — efficiently comparing file lists with Python sets
- **Infinite monitoring loops** — `while True` with `time.sleep()` for continuous watching
- **Security logging** — writing timestamped events to a log file
- **SIEM concept** — Security Information and Event Management fundamentals
- **KeyboardInterrupt** — gracefully handling Ctrl+C to exit cleanly

---

## 📋 Security Log

Every detected event is written to `fim_log.txt` with a timestamp:

[2026-06-08 17:54:35] NEW FILE: suspicious.txt

[2026-06-08 17:55:05] MODIFIED: secret.txt | Old: 9826e31a3e6d2235 | New: 1ded2a2f3ec4617f

[2026-06-08 17:55:45] DELETED: important.txt

Logging is the foundation of all cybersecurity monitoring —
**if it isn't logged, it didn't happen.**

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes only**. Only monitor 
files and directories you own or have explicit permission to monitor.

---

## 🔗 Related Projects

A growing Python cybersecurity toolkit:

| Tool | Purpose |
|---|---|
| [File Integrity Monitor](https://github.com/Patharx/fileintegrity) | Detect unauthorized file changes in real time |
| [Hash Cracker](https://github.com/Patharx/hashcracker) | Crack MD5/SHA hashes via dictionary attack |
| [Port Scanner](https://github.com/Patharx/portscanner) | Find open ports on a specific host |
| [Ping Sweeper](https://github.com/Patharx/pingsweeper) | Discover live hosts on a network |
| [Password Checker](https://github.com/Patharx/passwordchecker) | Analyze password strength |
| [Caesar Cipher](https://github.com/Patharx/caesarcipher) | Encrypt and decrypt messages |

---

## 👤 Author

**Ryan** — [github.com/Patharx](https://github.com/Patharx)

---

*"Nothing shall change without my knowledge."* 🧙
