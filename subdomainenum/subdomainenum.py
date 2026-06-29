import socket
import requests
import json
import datetime
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# ============================================================
# SUBDOMAIN ENUMERATOR
# ============================================================
# Two techniques running together:
# 1. BRUTE FORCE — try common subdomains from wordlist
#    and check if they resolve to real IP addresses via DNS
# 2. CERTIFICATE TRANSPARENCY — query crt.sh public database
#    for SSL certificates issued to the target domain
# ============================================================

GANDALF_REACTIONS = [
    "🧙 'Like mapping the hidden passages of Moria — the subdomains reveal themselves!'",
    "🧙 'Even the most guarded kingdom has many gates. We have found them all!'",
    "🧙 'The digital realm holds no secrets from a patient wizard!'",
    "🧙 'As the Fellowship mapped Middle-earth, so too have we mapped this domain!'",
]

def resolve_subdomain(subdomain, domain):
    """
    Tries to resolve a subdomain to an IP address using DNS.
    
    socket.gethostbyname() is a DNS lookup — it asks the DNS
    system 'what IP address does this domain name point to?'
    
    If it returns an IP = subdomain EXISTS and is live!
    If it raises socket.gaierror = subdomain doesn't exist
    
    This is called 'DNS resolution' and is the same thing
    your browser does every time you visit a website.
    
    gaierror stands for 'getaddrinfo error' — the technical
    name for a failed DNS lookup.
    """
    full_domain = f"{subdomain}.{domain}"
    try:
        ip = socket.gethostbyname(full_domain)
        return full_domain, ip
    except socket.gaierror:
        return full_domain, None

def brute_force_subdomains(domain, wordlist_path):
    """
    Tries every word in the wordlist as a potential subdomain.
    
    We use ThreadPoolExecutor just like our ping sweeper —
    instead of checking one subdomain at a time (slow!),
    we check 50 simultaneously (fast!).
    
    For each word in the wordlist we build the full domain:
    'admin' + 'google.com' = 'admin.google.com'
    Then we do a DNS lookup to see if it's real.
    """
    print(f"\n⚔️  TECHNIQUE 1: Brute Force Wordlist")
    print("-" * 55)

    try:
        with open(wordlist_path, "r") as f:
            subdomains = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"❌ Wordlist not found: {wordlist_path}")
        return []

    print(f"📋 Loaded {len(subdomains)} subdomains to try")
    print(f"⚡ Running {min(50, len(subdomains))} concurrent DNS lookups...")

    found = []
    checked = 0
    total = len(subdomains)

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = {
            executor.submit(resolve_subdomain, sub, domain): sub
            for sub in subdomains
        }

        for future in as_completed(futures):
            full_domain, ip = future.result()
            checked += 1
            print(f"Checking {checked}/{total}...", end="\r")

            if ip:
                print(f"✅ FOUND: {full_domain:45} → {ip}        ")
                found.append({"subdomain": full_domain, "ip": ip, "source": "brute_force"})

    print(f"\n✅ Brute force complete — {len(found)} subdomains found")
    return found

def query_certificate_transparency(domain):
    """
    Queries crt.sh for SSL certificates issued to the domain.
    
    Certificate Transparency (CT) is a public log of every
    SSL/TLS certificate ever issued. By law, Certificate
    Authorities must log every certificate they issue.
    
    This means if a company has 'admin.company.com' with an
    SSL certificate, that certificate is publicly logged and
    we can find it by querying the CT logs!
    
    crt.sh is a free public interface to these logs.
    We query it as a JSON API — it returns a list of all
    certificates matching our domain, including subdomains.
    
    This is completely legal — it's public information
    that certificate authorities are required to publish!
    """
    print(f"\n🔍 TECHNIQUE 2: Certificate Transparency Logs")
    print("-" * 55)
    print(f"📡 Querying crt.sh for certificates issued to *.{domain}...")

    url = f"https://crt.sh/?q=%.{domain}&output=json"

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        # Extract unique subdomains from certificate data
        subdomains = set()
        for cert in data:
            # name_value can contain multiple domains separated by newlines
            names = cert.get("name_value", "").split("\n")
            for name in names:
                name = name.strip().lower()
                # Filter out wildcards and make sure it's a subdomain
                if name and not name.startswith("*") and name.endswith(domain):
                    subdomains.add(name)

        print(f"📋 Found {len(data)} certificates in CT logs")
        print(f"🔎 Extracted {len(subdomains)} unique subdomains")

        # Now verify which ones are actually live
        print(f"⚡ Verifying which subdomains are live...")
        found = []

        for subdomain in subdomains:
            try:
                ip = socket.gethostbyname(subdomain)
                print(f"✅ LIVE: {subdomain:45} → {ip}")
                found.append({
                    "subdomain": subdomain,
                    "ip": ip,
                    "source": "certificate_transparency"
                })
            except socket.gaierror:
                pass  # Subdomain exists in logs but not live anymore

        print(f"\n✅ CT scan complete — {len(found)} live subdomains found")
        return found

    except requests.exceptions.RequestException as e:
        print(f"❌ Could not query crt.sh: {e}")
        return []
    except json.JSONDecodeError:
        print(f"❌ Could not parse crt.sh response")
        return []

def save_report(domain, all_found):
    """
    Saves the full enumeration report to a file.
    Timestamped so multiple scans don't overwrite each other.
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"subdomains_{domain.replace('.', '_')}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write("🧙 GANDALF'S SUBDOMAIN ENUMERATION REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Target:  {domain}\n")
        f.write(f"Scanned: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total:   {len(all_found)} subdomains found\n")
        f.write("=" * 60 + "\n\n")

        # Group by source
        brute_force = [s for s in all_found if s["source"] == "brute_force"]
        ct_logs = [s for s in all_found if s["source"] == "certificate_transparency"]

        if brute_force:
            f.write("BRUTE FORCE RESULTS:\n")
            f.write("-" * 40 + "\n")
            for s in brute_force:
                f.write(f"  {s['subdomain']:45} → {s['ip']}\n")

        if ct_logs:
            f.write("\nCERTIFICATE TRANSPARENCY RESULTS:\n")
            f.write("-" * 40 + "\n")
            for s in ct_logs:
                f.write(f"  {s['subdomain']:45} → {s['ip']}\n")

    print(f"\n💾 Report saved to: {filename}")
    return filename

def enumerate_subdomains(domain, wordlist_path="subdomains.txt"):
    """
    Main enumeration function — runs both techniques and
    combines the results, removing duplicates.
    """
    print("\n" + "=" * 60)
    print("🧙 GANDALF'S SUBDOMAIN ENUMERATOR")
    print("=" * 60)
    print(f"🎯 Target domain: {domain}")
    print(f"⏰ Started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    all_found = []
    seen_domains = set()

    # Technique 1 — Brute force
    brute_results = brute_force_subdomains(domain, wordlist_path)
    for result in brute_results:
        if result["subdomain"] not in seen_domains:
            all_found.append(result)
            seen_domains.add(result["subdomain"])

    # Small pause between techniques
    time.sleep(1)

    # Technique 2 — Certificate transparency
    ct_results = query_certificate_transparency(domain)
    for result in ct_results:
        if result["subdomain"] not in seen_domains:
            all_found.append(result)
            seen_domains.add(result["subdomain"])

    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)
    print(f"🎯 Target:              {domain}")
    print(f"✅ Brute force found:   {len(brute_results)}")
    print(f"✅ CT logs found:       {len(ct_results)}")
    print(f"✅ Total unique:        {len(all_found)}")
    print("=" * 60)

    if all_found:
        print(f"\n{'Subdomain':<45} {'IP Address':<20} {'Source'}")
        print("-" * 80)
        for s in sorted(all_found, key=lambda x: x["subdomain"]):
            print(f"{s['subdomain']:<45} {s['ip']:<20} {s['source']}")

    print(f"\n{random.choice(GANDALF_REACTIONS)}")

    # Save report
    if all_found:
        save_report(domain, all_found)

    return all_found

def main():
    print("🧙 GANDALF'S SUBDOMAIN ENUMERATOR")
    print("=" * 60)
    print("*unfurls a map of the digital realm*")
    print("Every domain has hidden passages. Let us find them...\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Enumerate subdomains")
        print("2. Quit")

        choice = input("\nEnter choice (1-2): ").strip()

        if choice == "1":
            domain = input("\nEnter target domain (e.g. example.com): ").strip()

            # Clean up input — remove http/https if included
            domain = domain.replace("https://", "").replace("http://", "").strip("/")

            if domain:
                enumerate_subdomains(domain)
            else:
                print("❌ Please enter a domain!")

        elif choice == "2":
            print("\n🧙 'The map is complete. Use this knowledge wisely. Farewell!'")
            break

        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()