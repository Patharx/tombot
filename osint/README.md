# 🧙 Gandalf's OSINT Web Scraper

A Python Open Source Intelligence (OSINT) tool that automatically gathers 
publicly available information from target websites — extracting metadata, 
emails, links, technology fingerprints, and robots.txt data.
Built as part of a cybersecurity learning journey.

---

## 🔍 What is OSINT?

**Open Source Intelligence** is the practice of gathering information from 
publicly available sources. It's the first step real penetration testers 
take before touching a target system.

> "Know your enemy before you engage." — every penetration tester ever

Real OSINT tools used by professionals:
- **Maltego** — professional OSINT platform
- **theHarvester** — email and domain harvester
- **Shodan** — search engine for internet-connected devices
- **Recon-ng** — full featured recon framework

This tool is a simplified version of **theHarvester** — built from scratch in Python.

---

## ⚡ Features

| Feature | Description |
|---|---|
| **Page Fetching** | Retrieves target website with browser-like headers |
| **Metadata Extraction** | Title, description, keywords, author, OG tags |
| **Technology Fingerprinting** | Detects server software, frameworks, and services |
| **Email Harvesting** | Regex-based email extraction from page content |
| **Link Mapping** | Separates internal and external links |
| **robots.txt Analysis** | Reveals disallowed paths and hidden site structure |
| **Report Generation** | Saves timestamped reports to text files
🎯 Target: https://books.toscrape.com

✅ Connected! Status: 200

📦 Page size: 51,294 bytes📋 Metadata:

title: All products | Books to Scrape - Sandbox🔧 Technologies:

✅ Framework/Service: jQuery🔗 Links:

Internal links: 73

   External links: 0📊 SCAN SUMMARY

✅ Technologies:     1 detected

✅ Emails found:     0

✅ Internal links:   73

✅ External links:   0

💾 Report saved to: osint_books_toscrape_com_20260613_011715.txt
---

## 🔑 Key Concepts Learned

- **HTTP requests** — fetching web pages programmatically with `requests`
- **HTML parsing** — extracting structured data from HTML with BeautifulSoup
- **HTTP status codes** — 200=OK, 404=Not Found, 403=Forbidden, 500=Server Error
- **HTTP headers** — invisible metadata revealing server software and technologies
- **User Agent** — how tools identify themselves to websites
- **robots.txt** — publicly available file revealing what sites want to hide from crawlers
- **Technology fingerprinting** — identifying software via HTML and header signatures
- **Regex email extraction** — pattern matching to find email addresses in text
- **URL parsing** — breaking URLs into components with `urlparse` and `urljoin`
- **Timestamped reporting** — saving scan results with date/time in filename

---

## 📋 Sample Report Output

Every scan saves a timestamped `.txt` report:
osint_example_com_20260613_011313.txt

osint_toscrape_com_20260613_011703.txt

osint_books_toscrape_com_20260613_011715.txt

Reports include all metadata, technologies, emails, links, and robots.txt findings.

---

## ⚠️ Legal Disclaimer

This tool is intended for **educational purposes only**. Only scan websites 
you own or have explicit permission to scan. Respect robots.txt directives 
and website terms of service. Unauthorized scraping may violate laws in 
your jurisdiction.

---

## 🔗 Related Projects

A growing Python cybersecurity toolkit:

| Tool | Purpose |
|---|---|
| [OSINT Scanner](https://github.com/Patharx/osint) | Gather public intelligence from websites |
| [File Integrity Monitor](https://github.com/Patharx/fileintegrity) | Detect unauthorized file changes |
| [Hash Cracker](https://github.com/Patharx/hashcracker) | Crack MD5/SHA hashes via dictionary attack |
| [Port Scanner](https://github.com/Patharx/portscanner) | Find open ports on a specific host |
| [Ping Sweeper](https://github.com/Patharx/pingsweeper) | Discover live hosts on a network |
| [Password Checker](https://github.com/Patharx/passwordchecker) | Analyze password strength |
| [Caesar Cipher](https://github.com/Patharx/caesarcipher) | Encrypt and decrypt messages |

---

## 👤 Author

**Ryan** — [github.com/Patharx](https://github.com/Patharx)

---

*"Every website leaves traces for those who know where to look."* 🧙

