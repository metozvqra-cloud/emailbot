import smtplib
import time
import random
import sys
from email.message import EmailMessage
from colorama import Fore, Style, init
from tqdm import tqdm

init(autoreset=True)

# ================== STEPUP CONFIG ==================
SMTP_HOST = "mail.upstep-test.com"
SMTP_PORT = 465
SMTP_USER = "bot@upstep-test.com"
SMTP_PASS = "}Fh22cR5K0CM"

FROM_NAME = "👟 StepUP | Your Favourite Plug"
FROM_EMAIL = "bot@upstep-test.com"

EMAIL_FILE = "emails.txt"

BLOCKED_DOMAINS = [
    "@abv.bg",
    "@mail.bg",
    "@dir.bg"
]

SEND_DELAY_MIN = 8
SEND_DELAY_MAX = 15
# ==================================================


def slow_print(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()


def ultra_boot():
    print(Fore.GREEN + Style.BRIGHT + r"""
 ███████╗████████╗███████╗██████╗ ██╗   ██╗██████╗ 
 ██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║   ██║██╔══██╗
 ███████╗   ██║   █████╗  ██████╔╝██║   ██║██████╔╝
 ╚════██║   ██║   ██╔══╝  ██╔═══╝ ██║   ██║██╔═══╝ 
 ███████║   ██║   ███████╗██║     ╚██████╔╝██║     
 ╚══════╝   ╚═╝   ╚══════╝╚═╝      ╚═════╝ ╚═╝     
""")
    slow_print(Fore.GREEN + "INTELLIGENT OUTREACH ENGINE\n")
    slow_print(Fore.CYAN + "SYSTEM STATUS: OPERATIONAL\n")
    print(Fore.GREEN + "=" * 70)
    time.sleep(1)


def smart_fail_screen(reason):
    print(Fore.RED + Style.BRIGHT + f"""
╔════════════════════════════════════════════════╗
║                SYSTEM ALERT                    ║
╠════════════════════════════════════════════════╣
║ STATUS : DELIVERY HALTED                       ║
║ REASON : {reason:<34} ║
║ ACTION : SAFE MODE ENABLED                    ║
╚════════════════════════════════════════════════╝
""")

    print(Fore.CYAN + "Recommended actions:")
    print(Fore.CYAN + "• Verify SMTP username / password")
    print(Fore.CYAN + "• Check hosting SMTP restrictions")
    print(Fore.CYAN + "• Retry after a short cooldown\n")

    slow_print(Fore.YELLOW + "SYSTEM SHUTDOWN SEQUENCE INITIATED...")
    for i in range(5, 0, -1):
        print(Fore.YELLOW + f"Shutdown in {i}...", end="\r")
        time.sleep(1)

    sys.exit(1)


def smart_smtp_login(smtp):
    try:
        slow_print(Fore.CYAN + "AUTH → Establishing secure SMTP channel...")
        smtp.login(SMTP_USER, SMTP_PASS)
        slow_print(Fore.GREEN + Style.BRIGHT + "AUTH SUCCESS ✓\n")
        return True

    except smtplib.SMTPAuthenticationError:
        slow_print(Fore.RED + Style.BRIGHT + "AUTH FAILURE ✖")
        smart_fail_screen("SMTP AUTHENTICATION FAILED")

    except Exception as e:
        slow_print(Fore.RED + Style.BRIGHT + "CRITICAL SMTP ERROR ✖")
        smart_fail_screen(str(e))


def load_emails():
    with open(EMAIL_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def is_blocked(email):
    return any(email.lower().endswith(domain) for domain in BLOCKED_DOMAINS)


def generate_message(to_email):
    subjects = [
        "StepUP ти пише 👋",
        "Малък въпрос от StepUP 🤍",
        "Екипът на StepUP",
        "StepUP | Your Favourite Plug"
    ]

    bodies = [
        """Здравей 👋

Пишем ти от екипа на StepUP.

Получаваш този имейл, защото си наш клиент или си се свързал с нас през сайта ни.
В момента подобряваме системите си и всяка обратна връзка ни помага.

Ако ти е удобно, просто ни отговори с едно „ОК“ 🙂
Това ни помага повече, отколкото изглежда.

Благодарим ти 🤍
Екипът на StepUP
""",

        """Здрасти 🙂

Ние сме StepUP.
Работим всеки ден, за да даваме по-добро изживяване на хора като теб.

Ако този имейл стигне до теб, значи сме на прав път 🙂
Един кратък отговор е напълно достатъчен.

Благодарим ти 🙏
StepUP Team
""",

        """Хей 👋

Това е лично съобщение от StepUP.
Не продаваме нищо – просто настройваме комуникацията си по-добре.

Ако искаш да ни помогнеш, можеш просто да отговориш.
А ако не – няма проблем 🤍

StepUP | Your Favourite Plug
"""
    ]

    msg = EmailMessage()
    msg["From"] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg["To"] = to_email
    msg["Subject"] = random.choice(subjects)
    msg.set_content(random.choice(bodies))
    msg["Reply-To"] = FROM_EMAIL

    return msg


def main():
    ultra_boot()

    emails = load_emails()
    valid_emails = [e for e in emails if not is_blocked(e)]

    print(Fore.CYAN + f"TOTAL LOADED : {len(emails)}")
    print(Fore.RED + f"BLOCKED      : {len(emails) - len(valid_emails)}")
    print(Fore.GREEN + f"READY        : {len(valid_emails)}")
    print(Fore.GREEN + "=" * 70)

    input(Fore.YELLOW + "PRESS ENTER TO DEPLOY STEPUP DELIVERY MODE...")

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        smart_smtp_login(smtp)

        for email in tqdm(valid_emails, desc="DELIVERING", ncols=80):
            try:
                msg = generate_message(email)
                smtp.send_message(msg)
                print(Fore.GREEN + f"✔ SENT → {email}")
            except Exception as e:
                print(Fore.RED + f"✖ FAILED → {email} | {e}")

            time.sleep(random.randint(SEND_DELAY_MIN, SEND_DELAY_MAX))

    print(Fore.GREEN + Style.BRIGHT + "\nMISSION COMPLETE — STEPUP BOT OFFLINE 🚀")


if __name__ == "__main__":
    main()
