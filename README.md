
<div align="center">

<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=31&duration=2500&pause=900&color=9933FF&center=true&vCenter=true&width=1200&lines=👑+MURPHY+ULTIMATE+CHECKER;⚡+All-in-One+Gaming+Account+Analyzer;🎮+Xbox+Live+%2B+Game+Pass+Detection;⛏️+Minecraft+Java+%26+Bedrock+Checker;📊+PSN+Purchase+History+Scanner;🤖+Telegram+Live+Notifications+System" />

</div>

---

# 👑 Murphy Ultimate Checker

A professional-grade, multi-threaded account analyzer written in Python.  
Specifically engineered for deep-scanning Microsoft and Gaming ecosystems, providing detailed insights into subscriptions, purchase histories, and profile statistics.

---

# ⚡ Key Features

- 🎮 **Xbox Ecosystem**  
  Full detection of Xbox Live profiles, Gamertags, Account Tiers, and Reputation status.

- 💎 **Subscription Scanner**  
  Identifies Game Pass Ultimate, Core, PC, and Office 365 subscriptions.

- ⛏️ **Minecraft Specialist**  
  Comprehensive checking for Minecraft Java, Bedrock, Dungeons, and Legends ownership including Cape detection.

- 📊 **PSN History**  
  Advanced scanner for PlayStation Network purchase history with custom year filtering.

- 🤖 **Telegram Integration**  
  Real-time "Hit" notifications and live statistics updates directly to your Telegram Bot.

- 🖥️ **Dashboard UI**  
  Interactive Linux-style terminal interface with live progress bars and CPM tracking.

- 📁 **Smart Export**  
  Automatically organizes results into categorized folders (`Hits`, `Details`, `Reports`) and generates a final ZIP report.

---

# 📸 Terminal Interface

```text
┌──────────────────────────────┬────────────┬──────────┬────────────────────┐
│           STATUS             │   COUNT    │ PERCENT  │     PROGRESS       │
├──────────────────────────────┼────────────┼──────────┼────────────────────┤
│  ✅ VALID                    │      1,250 │   15.5%  │ ████░░░░░░░░░░░░   │
│  🏆 PREMIUM                  │        420 │    5.2%  │ ██░░░░░░░░░░░░░░   │
│  🎮 PSN                      │        185 │    2.3%  │ █░░░░░░░░░░░░░░░   │
│  💜 GAME PASS ULTIMATE       │         95 │    1.1%  │ █░░░░░░░░░░░░░░░   │
│  ⛏️ MINECRAFT JAVA           │        112 │    1.4%  │ █░░░░░░░░░░░░░░░   │
└──────────────────────────────┴────────────┴──────────┴────────────────────┘
🚀 Installation & Usage
🛠️ Requirements
Python 3.10+
Modules:
requests
colorama
urllib3
(Automatically installed on first run)
📥 Setup
Bash
# Clone the repository
git clone https://github.com/sadikmahedi88/Murphy-Ultimate-Checker.git

# Enter the directory
cd Murphy-Ultimate-Checker

# Run the script
python gpt.py
⚙️ Configuration
The tool automatically generates a config.json file where you can permanently save:
telegram_token
chat_id
threads (Recommended: 50-100)
year_filter for PSN purchase detection
📂 Output Structure
Plain text
Results/
└── Murphy_TIMESTAMP/
    ├── Hits/          # Valid accounts & Premium categories
    ├── Details/       # Deep-scan logs (Bios, Ages, Capes)
    └── Reports/       # Summary text & Final statistics
👑 Developer & Credits
Developer: @Murphython
GitHub: sadikmahedi88
Support: Official Telegram Channel
⚠️ Disclaimer
This project is intended for educational and authorized security auditing purposes only.
The developer assumes no responsibility for misuse, unauthorized access, or damages caused by this software.
Always comply with local laws and regulations regarding cybersecurity, authentication systems, and data privacy.
