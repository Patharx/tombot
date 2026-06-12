import hashlib
import os
import time
import json
import datetime
import random

# ============================================================
# FILE INTEGRITY MONITOR
# ============================================================
# How it works:
# 1. BASELINE — scan all files and record their hashes
# 2. MONITOR — continuously re-scan and compare to baseline
# 3. ALERT — if anything changed, added, or deleted — report it!
# ============================================================

# Where to store our baseline snapshot
BASELINE_FILE = "baseline.json"

# How often to check for changes (in seconds)
CHECK_INTERVAL = 10

GANDALF_ALERTS = {
    "new": [
        "🧙 'Something has crept in where it was not before — a new file stirs!'",
        "🧙 'An uninvited guest has arrived. A new file appears where none existed!'",
        "🧙 'Like a Nazgul in the night — something new has entered unseen!'",
    ],
    "modified": [
        "🧙 'Something has changed. I can feel it — like the Ring passing to a new bearer!'",
        "🧙 'A file has been altered! Even the smallest change leaves a trace!'",
        "🧙 'The threads of fate have shifted — this file is not as it was!'",
    ],
    "deleted": [
        "🧙 'A file has vanished! Like Gandalf at the Bridge of Khazad-dûm — gone!'",
        "🧙 'Something has been erased — as Sauron tried to erase the free peoples!'",
        "🧙 'A file is missing! Someone seeks to cover their tracks!'",
    ]
}

def get_file_hash(filepath):
    """
    Generates a SHA256 hash of a file's contents.
    
    We read the file in CHUNKS (8192 bytes at a time) rather than
    all at once. This is important for large files — if we read a
    1GB file all at once it would use 1GB of RAM. Chunked reading
    uses the same tiny amount of RAM regardless of file size.
    
    This is called 'streaming' and is a best practice in real tools.
    """
    sha256 = hashlib.sha256()

    try:
        with open(filepath, "rb") as f:  # "rb" = read binary mode
            # Works for ALL file types — text, images, executables
            while True:
                chunk = f.read(8192)  # Read 8KB at a time
                if not chunk:
                    break  # No more data — stop reading
                sha256.update(chunk)  # Add chunk to hash calculation
        return sha256.hexdigest()

    except (IOError, PermissionError):
        # Some files can't be read — system files, locked files etc
        return None

def get_file_info(filepath):
    """
    Gets metadata about a file — its hash AND its size.
    
    os.path.getsize() returns file size in bytes.
    We store both hash and size in our baseline.
    Hash catches content changes, size is a quick sanity check.
    """
    return {
        "hash": get_file_hash(filepath),
        "size": os.path.getsize(filepath),
        "modified": os.path.getmtime(filepath)  # Last modified timestamp
    }

def scan_directory(directory):
    """
    Walks through every file in a directory and its subdirectories.
    
    os.walk() is a powerful Python tool that recursively explores
    folders. It returns:
    - root: current folder being explored
    - dirs: subfolders in that folder
    - files: files in that folder
    
    This means it finds files nested deep in subfolders too!
    """
    file_data = {}

    if not os.path.exists(directory):
        print(f"❌ Directory not found: {directory}")
        return file_data

    for root, dirs, files in os.walk(directory):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Get relative path — cleaner than full absolute path
            relative_path = os.path.relpath(filepath, directory)

            info = get_file_info(filepath)
            if info["hash"]:  # Only add if we could read the file
                file_data[relative_path] = info

    return file_data

def save_baseline(directory):
    """
    Creates the initial snapshot of all files.
    
    We save it as JSON — a human readable data format.
    JSON (JavaScript Object Notation) is used everywhere in
    programming to store and transfer structured data.
    
    json.dump() converts our Python dictionary to JSON text.
    indent=2 makes it pretty printed and readable.
    """
    print(f"\n📸 Creating baseline snapshot of: {directory}")
    print("Scanning all files...")

    baseline = {
        "directory": directory,
        "created": datetime.datetime.now().isoformat(),
        "files": scan_directory(directory)
    }

    with open(BASELINE_FILE, "w") as f:
        json.dump(baseline, f, indent=2)

    file_count = len(baseline["files"])
    print(f"✅ Baseline created! {file_count} files recorded.")
    print(f"💾 Saved to: {BASELINE_FILE}")

    # Show what was recorded
    print(f"\n{'File':<40} {'Size':<12} {'Hash (first 16 chars)'}")
    print("-" * 75)
    for filepath, info in baseline["files"].items():
        size = f"{info['size']} bytes"
        hash_preview = info['hash'][:16] + "..."
        print(f"{filepath:<40} {size:<12} {hash_preview}")

    return baseline

def load_baseline():
    """
    Loads the previously saved baseline from disk.
    
    json.load() converts JSON text back to a Python dictionary.
    This is the opposite of json.dump().
    """
    if not os.path.exists(BASELINE_FILE):
        print("❌ No baseline found! Create one first with option 1.")
        return None

    with open(BASELINE_FILE, "r") as f:
        return json.load(f)

def compare_snapshots(baseline_files, current_files):
    """
    Compares two snapshots and finds what changed.
    
    Three things can happen to a file:
    1. NEW — exists in current but not in baseline
    2. DELETED — exists in baseline but not in current
    3. MODIFIED — exists in both but hash is different
    
    We use Python SET operations for efficient comparison:
    - set(a) - set(b) = items in a but not in b
    - & (intersection) = items in both
    """
    baseline_set = set(baseline_files.keys())
    current_set = set(current_files.keys())

    # New files — in current but not baseline
    new_files = current_set - baseline_set

    # Deleted files — in baseline but not current
    deleted_files = baseline_set - current_set

    # Check for modifications in files that exist in both
    modified_files = []
    common_files = baseline_set & current_set

    for filepath in common_files:
        if baseline_files[filepath]["hash"] != current_files[filepath]["hash"]:
            modified_files.append(filepath)

    return new_files, deleted_files, modified_files

def log_event(message):
    """
    Writes security events to a log file.
    
    Logging is CRITICAL in cybersecurity — you need a record
    of everything that happened and when. Real SIEM (Security
    Information and Event Management) tools are essentially
    sophisticated logging and alerting systems.
    
    We append to the log file rather than overwriting it —
    "a" mode = append, adds to end of file.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}\n"

    with open("fim_log.txt", "a") as f:
        f.write(log_entry)

def monitor(directory, interval):
    """
    The main monitoring loop — runs continuously checking for changes.
    
    This is an INFINITE LOOP — it runs forever until you press Ctrl+C.
    time.sleep(interval) pauses execution for X seconds between checks.
    This is how all monitoring tools work — check, sleep, check, sleep.
    
    KeyboardInterrupt is the exception raised when you press Ctrl+C.
    We catch it gracefully so the program exits cleanly.
    """
    baseline = load_baseline()
    if not baseline:
        return

    baseline_files = baseline["files"]
    watched_dir = baseline["directory"]

    print(f"\n👁️  MONITORING STARTED")
    print(f"📁 Watching: {watched_dir}")
    print(f"⏱️  Checking every {interval} seconds")
    print(f"📋 Baseline has {len(baseline_files)} files")
    print(f"🛑 Press Ctrl+C to stop\n")
    print("-" * 55)

    check_count = 0

    try:
        while True:
            check_count += 1
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"🔍 Check #{check_count} at {timestamp}...", end="\r")

            # Scan current state of directory
            current_files = scan_directory(watched_dir)

            # Compare to baseline
            new_files, deleted_files, modified_files = compare_snapshots(
                baseline_files, current_files
            )

            # Report any changes
            changes_found = False

            for filepath in new_files:
                changes_found = True
                alert = f"⚠️  NEW FILE DETECTED: {filepath}"
                print(f"\n{alert}")
                print(random.choice(GANDALF_ALERTS["new"]))
                log_event(f"NEW FILE: {filepath}")

            for filepath in deleted_files:
                changes_found = True
                alert = f"🚨 FILE DELETED: {filepath}"
                print(f"\n{alert}")
                print(random.choice(GANDALF_ALERTS["deleted"]))
                log_event(f"DELETED: {filepath}")

            for filepath in modified_files:
                changes_found = True
                old_hash = baseline_files[filepath]["hash"][:16]
                new_hash = current_files[filepath]["hash"][:16]
                alert = f"⚡ FILE MODIFIED: {filepath}"
                print(f"\n{alert}")
                print(f"   Old hash: {old_hash}...")
                print(f"   New hash: {new_hash}...")
                print(random.choice(GANDALF_ALERTS["modified"]))
                log_event(f"MODIFIED: {filepath} | Old: {old_hash} | New: {new_hash}")

            if changes_found:
                print("-" * 55)

            # Wait before next check
            time.sleep(interval)

    except KeyboardInterrupt:
        print(f"\n\n🛑 Monitoring stopped after {check_count} checks.")
        print(f"📋 Log saved to: fim_log.txt")
        print("🧙 'Even in vigilance we must rest. Farewell!'")

def view_log():
    """
    Displays the security event log.
    Reading logs is a core cybersecurity skill — 
    most security analysts spend significant time in logs!
    """
    if not os.path.exists("fim_log.txt"):
        print("📋 No log file found yet — start monitoring first!")
        return

    print("\n📋 SECURITY EVENT LOG")
    print("=" * 55)

    with open("fim_log.txt", "r") as f:
        contents = f.read()

    if contents:
        print(contents)
    else:
        print("No events logged yet.")

    print("=" * 55)

def main():
    print("🧙 GANDALF'S FILE INTEGRITY MONITOR")
    print("=" * 55)
    print("*gazes upon the files with all-seeing eyes*")
    print("Nothing shall change without my knowledge...\n")

    while True:
        print("\nWhat would you like to do?")
        print("1. Create baseline snapshot")
        print("2. Start monitoring")
        print("3. View security log")
        print("4. Quit")

        choice = input("\nEnter choice (1-4): ").strip()

        if choice == "1":
            directory = input("\nDirectory to watch (press Enter for watched_folder): ").strip()
            if not directory:
                directory = "watched_folder"
            save_baseline(directory)

        elif choice == "2":
            interval = input(f"\nCheck interval in seconds (press Enter for {CHECK_INTERVAL}): ").strip()
            interval = int(interval) if interval else CHECK_INTERVAL
            directory = "watched_folder"
            monitor(directory, interval)

        elif choice == "3":
            view_log()

        elif choice == "4":
            print("\n🧙 'Vigilance is its own reward. Farewell!'")
            break

        else:
            print("❌ Invalid choice!")

if __name__ == "__main__":
    main()