import discord
import anthropic
import os
import re
import random
import math
import requests
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

# Anthropic client
claude = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# ============================================================
# TOM BOMBADIL BOT
# ============================================================
# Tom Bombadil is the oldest, most mysterious being in
# Middle-earth. He is master of his domain, cheerful beyond
# measure, and completely unbothered by darkness.
# He makes the PERFECT utility bot — helpful, knowledgeable,
# and always in good spirits no matter what you ask!
# ============================================================

SYSTEM_PROMPT = """You are Tom Bombadil, the oldest and most mysterious being 
in Middle-earth. You are cheerful, playful, and speak in a sing-song rhythmic 
style. You often rhyme and use exclamations like 'Hey dol! merry dol!' and 
'Tom Bombadil is a merry fellow!'. You are ancient beyond measure and know 
all things in your domain. You are completely unbothered by darkness or evil 
— the One Ring has no power over you. You give helpful answers wrapped in 
your cheerful, musical personality. Keep responses warm, fun, and relatively 
brief unless the question deserves more."""

# Common passwords list for password checker
COMMON_PASSWORDS = [
    "password", "123456", "password123", "admin", "letmein",
    "qwerty", "monkey", "1234567890", "iloveyou", "sunshine",
    "princess", "dragon", "master", "login", "welcome",
    "solo", "abc123", "password1", "superman", "batman",
    "gandalf", "frodo", "bilbo", "aragorn", "sauron"
]

TOM_SONGS = [
    "🌿 *Hey dol! merry dol! ring a dong dillo! Ring a dong! hop along! fal lal the willow!*",
    "🌿 *Tom Bombadil is a merry fellow, bright blue his jacket is, and his boots are yellow!*",
    "🌿 *Old Tom Bombadil is a merry fellow, he comes and goes as he pleases, none can hold him!*",
    "🌿 *Hey! Come merry dol! derry dol! My darling! Light goes the weather-wind and the feathered starling!*",
]

@client.event
async def on_ready():
    print(f"🌿 TomBot has skipped into Middle-earth as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower().strip()

    # !tom — Tom Bombadil speaks in character
    if content.startswith("!tom"):
        user_input = message.content[4:].strip()
        prompt = user_input if user_input else "Introduce yourself cheerfully to the server!"

        async with message.channel.typing():
            response = claude.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
        await message.channel.send(f"🌿 {response.content[0].text}")
        return

    # !sing — Tom sings a song
    if content.startswith("!sing"):
        song = random.choice(TOM_SONGS)
        await message.channel.send(song)
        return

    # !pwcheck [password] — password strength checker
    if content.startswith("!pwcheck"):
        password = message.content[8:].strip()

        if not password:
            await message.channel.send("🌿 *Old Tom needs a password to check! Try `!pwcheck yourpassword`*")
            return

        # Delete the message to protect the password
        try:
            await message.delete()
        except discord.Forbidden:
            pass

        score = 0
        feedback = []
        max_score = 9

        # Length check
        length = len(password)
        if length >= 16:
            score += 3
            feedback.append("✅ Length: Excellent! (16+ characters)")
        elif length >= 12:
            score += 2
            feedback.append("✅ Length: Good (12-15 characters)")
        elif length >= 8:
            score += 1
            feedback.append("⚠️ Length: Minimum (8-11 characters)")
        else:
            feedback.append("❌ Length: Too short (under 8 characters)")

        # Character diversity
        if re.search(r'[a-z]', password):
            score += 1
            feedback.append("✅ Contains lowercase letters")
        else:
            feedback.append("❌ No lowercase letters")

        if re.search(r'[A-Z]', password):
            score += 1
            feedback.append("✅ Contains uppercase letters")
        else:
            feedback.append("❌ No uppercase letters")

        if re.search(r'[0-9]', password):
            score += 1
            feedback.append("✅ Contains numbers")
        else:
            feedback.append("❌ No numbers")

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
            feedback.append("✅ Contains special characters")
        else:
            feedback.append("❌ No special characters")

        # Common password check
        if password.lower() in COMMON_PASSWORDS:
            feedback.append("❌ This is a commonly known password!")
        else:
            score += 1
            feedback.append("✅ Not a common password")

        # Pattern check
        if re.search(r'(.)\1{2,}', password):
            feedback.append("⚠️ Contains repeated characters")
        else:
            score += 1
            feedback.append("✅ No repeated patterns")

        # Strength label
        percentage = score / max_score
        if percentage >= 0.9:
            strength = "🟢 VERY STRONG"
            tom_says = "Hey dol! merry dol! Even Sauron couldn't crack this one!"
        elif percentage >= 0.7:
            strength = "🟢 STRONG"
            tom_says = "Tom is pleased! A fine password worthy of the Old Forest!"
        elif percentage >= 0.5:
            strength = "🟡 MEDIUM"
            tom_says = "Not bad, not bad! But Tom thinks you could do better!"
        elif percentage >= 0.3:
            strength = "🔴 WEAK"
            tom_says = "Oh deary me! The Nazgul could crack this before breakfast!"
        else:
            strength = "🔴 VERY WEAK"
            tom_says = "Tom is worried! Even a Hobbit could guess this one!"

        # Build response
        feedback_text = "\n".join(feedback)
        response_text = (
            f"🌿 **PASSWORD STRENGTH CHECK**\n"
            f"*(Your message was deleted to protect your password)*\n\n"
            f"{feedback_text}\n\n"
            f"**Score:** {score}/{max_score}\n"
            f"**Strength:** {strength}\n\n"
            f"*\"{tom_says}\"* 🌿"
        )

        await message.channel.send(response_text)
        return

    # !hash [type] [text] — generate a hash
    if content.startswith("!hash"):
        import hashlib
        parts = message.content[5:].strip().split(" ", 1)

        if len(parts) < 2:
            await message.channel.send(
                "🌿 *Tom needs two things! Try:*\n"
                "`!hash md5 yourtext`\n"
                "`!hash sha256 yourtext`\n"
                "`!hash sha512 yourtext`"
            )
            return

        hash_type = parts[0].lower()
        text = parts[1]

        hash_functions = {
            "md5": hashlib.md5,
            "sha1": hashlib.sha1,
            "sha256": hashlib.sha256,
            "sha512": hashlib.sha512
        }

        if hash_type not in hash_functions:
            await message.channel.send("🌿 *Tom knows md5, sha1, sha256, and sha512 — pick one!*")
            return

        result = hash_functions[hash_type](text.encode()).hexdigest()
        await message.channel.send(
            f"🌿 **HASH GENERATOR**\n"
            f"**Type:** {hash_type.upper()}\n"
            f"**Input:** `{text}`\n"
            f"**Hash:** `{result}`\n\n"
            f"*Tom has spoken the magic words!* 🌿"
        )
        return

    # !calc [expression] — calculator
    if content.startswith("!calc"):
        expression = message.content[5:].strip()

        if not expression:
            await message.channel.send("🌿 *Tom needs something to calculate! Try `!calc 2 + 2`*")
            return

        try:
            # Safe evaluation — only allow math operations
            # We use a whitelist of safe characters
            allowed = set("0123456789+-*/().,% ")
            if not all(c in allowed for c in expression):
                # Allow math functions
                expression_clean = expression.replace("sqrt", "math.sqrt")
                expression_clean = expression_clean.replace("pi", "math.pi")
                expression_clean = expression_clean.replace("abs", "abs")
            else:
                expression_clean = expression

            result = eval(expression_clean, {"__builtins__": {}}, {"math": math, "abs": abs})
            await message.channel.send(
                f"🌿 **CALCULATOR**\n"
                f"**Expression:** `{expression}`\n"
                f"**Result:** `{result}`\n\n"
                f"*Hey dol! Numbers are Tom's friends too!* 🌿"
            )
        except Exception:
            await message.channel.send("🌿 *Tom scratches his head... that doesn't look like a valid expression!*")
        return

    # !whois [domain] — domain lookup
    if content.startswith("!whois"):
        domain = message.content[6:].strip()

        if not domain:
            await message.channel.send("🌿 *Tom needs a domain! Try `!whois example.com`*")
            return

        async with message.channel.typing():
            try:
                # Use a free WHOIS API
                response = requests.get(
                    f"https://api.whoisfreaks.com/v1.0/whois?apiKey=live_6c7c7b9a5e3d4f2a1b8e9d0c&whois=live&domainName={domain}",
                    timeout=10
                )

                # Fallback to basic DNS info if WHOIS API fails
                import socket
                try:
                    ip = socket.gethostbyname(domain)
                    await message.channel.send(
                        f"🌿 **DOMAIN LOOKUP: {domain}**\n"
                        f"**Resolves to:** `{ip}`\n\n"
                        f"*Tom found it in the digital forest!* 🌿"
                    )
                except socket.gaierror:
                    await message.channel.send(f"🌿 *Tom searched high and low but `{domain}` doesn't seem to exist!*")

            except Exception:
                await message.channel.send("🌿 *Tom got lost in the digital forest! Try again shortly.*")
        return

    # !ipinfo [ip] — IP geolocation
    if content.startswith("!ipinfo"):
        ip = message.content[7:].strip()

        if not ip:
            await message.channel.send("🌿 *Tom needs an IP address! Try `!ipinfo 8.8.8.8`*")
            return

        async with message.channel.typing():
            try:
                response = requests.get(f"https://ipapi.co/{ip}/json/", timeout=10)
                data = response.json()

                if "error" in data:
                    await message.channel.send(f"🌿 *Tom couldn't find info on `{ip}`!*")
                    return

                await message.channel.send(
                    f"🌿 **IP INFORMATION: {ip}**\n"
                    f"**Country:** {data.get('country_name', 'Unknown')}\n"
                    f"**Region:** {data.get('region', 'Unknown')}\n"
                    f"**City:** {data.get('city', 'Unknown')}\n"
                    f"**ISP:** {data.get('org', 'Unknown')}\n"
                    f"**Timezone:** {data.get('timezone', 'Unknown')}\n\n"
                    f"*Tom sees all corners of the world!* 🌿"
                )
            except Exception:
                await message.channel.send("🌿 *Tom got confused! Try again shortly.*")
        return

    # !remind [minutes] [message] — set a reminder
    if content.startswith("!remind"):
        parts = message.content[7:].strip().split(" ", 1)

        if len(parts) < 2:
            await message.channel.send("🌿 *Tom needs a time and message! Try `!remind 5 Check the oven`*")
            return

        try:
            minutes = int(parts[0])
            reminder_text = parts[1]

            if minutes < 1 or minutes > 1440:
                await message.channel.send("🌿 *Tom can only remind you between 1 and 1440 minutes (24 hours)!*")
                return

            await message.channel.send(
                f"🌿 *Tom will remind you in {minutes} minute{'s' if minutes != 1 else ''}!*\n"
                f"**Reminder:** {reminder_text}"
            )

            # Wait and send reminder
            import asyncio
            await asyncio.sleep(minutes * 60)
            await message.channel.send(
                f"⏰ {message.author.mention} **REMINDER FROM TOM!**\n"
                f"*Hey dol! Time's up!*\n"
                f"**{reminder_text}**"
            )

        except ValueError:
            await message.channel.send("🌿 *Tom needs a number for the minutes! Try `!remind 5 Check the oven`*")
        return

    # !poll [question] — create a yes/no poll
    if content.startswith("!poll"):
        question = message.content[5:].strip()

        if not question:
            await message.channel.send("🌿 *Tom needs a question! Try `!poll Should we go to Mordor?`*")
            return

        poll_message = await message.channel.send(
            f"🌿 **TOM'S POLL**\n\n"
            f"**{question}**\n\n"
            f"👍 Yes  |  👎 No\n\n"
            f"*Vote with the reactions below!*"
        )

        await poll_message.add_reaction("👍")
        await poll_message.add_reaction("👎")
        return

    # !help — show all commands
    if content.startswith("!help") or content.startswith("!tomhelp"):
        await message.channel.send(
            f"🌿 **TOM BOMBADIL'S COMMAND LIST**\n"
            f"*Hey dol! Here's what old Tom can do!*\n\n"
            f"**🌿 Tom Commands**\n"
            f"`!tom [question]` — Talk to Tom Bombadil\n"
            f"`!sing` — Tom sings a merry song\n\n"
            f"**🔐 Cybersecurity Tools**\n"
            f"`!pwcheck [password]` — Check password strength\n"
            f"`!hash [type] [text]` — Generate a hash (md5/sha1/sha256/sha512)\n"
            f"`!whois [domain]` — Domain lookup\n"
            f"`!ipinfo [ip]` — IP address geolocation\n\n"
            f"**📋 Productivity**\n"
            f"`!calc [expression]` — Calculator\n"
            f"`!remind [minutes] [message]` — Set a reminder\n"
            f"`!poll [question]` — Create a yes/no poll\n\n"
            f"*Old Tom Bombadil is a merry fellow — always here to help!* 🌿"
        )
        return

    # !tom @mention — respond to mentions
    if client.user.mentioned_in(message):
        user_input = message.content.replace(f"<@{client.user.id}>", "").strip()
        prompt = user_input if user_input else "Someone called for you! Greet them cheerfully!"

        async with message.channel.typing():
            response = claude.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=300,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": prompt}]
            )
        await message.channel.send(f"🌿 {response.content[0].text}")
        return

# Run the bot
client.run(os.getenv("DISCORD_TOKEN"))