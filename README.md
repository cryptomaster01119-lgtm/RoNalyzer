# 🎮 RoNalyzer — Roblox Game Analyzer (Detailed)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![License](https://img.shields.io/badge/license-MIT-green)

RoNalyzer is a fast, terminal-based Roblox game analyzer that fetches public stats from Roblox APIs and prints a polished, detailed report. Designed for Termux / Linux / Replit / Colab — perfect for power users who want deep insight in a simple CLI.

---

## 🚀 Features

* Fetch Universe ID from a PlaceID or a game link
* Pull detailed stats from `games.roblox.com` (visits, playing/CCU, maxPlayers)
* Retrieve favorites, likes (upVotes), downVotes and thumbnail when available
* Compute engagement metrics (favorites/visits and likes/visits)
* Interactive CLI with options to show full description and export JSON report
* Lightweight, dependency only `requests`

---

## 📁 Project layout

```
RoNalyzer/
├─ src/
│  └─ roblox_analyzer/
│     └─ roblox_analyzer_detalhado.py   # main detailed analyzer script
├─ scripts/
│  └─ run_local.sh
├─ tests/
├─ requirements.txt
└─ README.md
```

Primary script: `src/roblox_analyzer/roblox_analyzer_detalhado.py`
(You can also copy it to project root as `roblox_analyzer_detalhado.py` for quick testing.)

---

## ⚙️ Requirements

* Python 3.9 or newer
* `requests` library

Install dependencies:

```bash
pip install -r requirements.txt
# or
pip install requests
```

`requirements.txt` should contain:

```
requests
```

---

## ▶️ Quick start

Run the analyzer:

```bash
python src/roblox_analyzer/roblox_analyzer_detalhado.py
```

If you placed the script in the repo root:

```bash
python roblox_analyzer_detalhado.py
```

Interactive flow:

1. Paste a Roblox game link or the PlaceID when prompted.
2. The script resolves the UniverseId and fetches game data.
3. It prints a formatted detailed report:

   * Name, description, Universe ID, root Place ID
   * Visits, playing (CCU), maxPlayers
   * Favorites, likes (upVotes), downVotes
   * Engagement metrics, thumbnail URL (if available)
4. Choose whether to display the full description.
5. Optionally save a JSON report (`roblox_report_<universeId>.json`).

---

## 📊 Example output

```
=== Roblox Game Analyzer (DETAILED) ===
Paste Roblox game link (or PlaceID): https://www.roblox.com/games/79297358668243/PLS-DONATE-N-1
Show full description? (y/N): n

ROBLOX GAME ANALYZER — DETAILED REPORT
============================================================
Input PlaceID/URL: https://www.roblox.com/...
Name: 💸 PLS DONATE N 1
Description: PLS DONATE N 1 💸 is a game where you can claim stands...
Universe ID: 8115728073
...
Favorites: 33,852
Likes (upVotes): 278  Downvotes: 42
Engagement (favorites/visits): 10.63%
Engagement (likes/visits): 0.0873%
...
```

---

## 🛠 Troubleshooting

* `NameResolutionError` or DNS errors:

  * Your environment may block `apis.roblox.com`. Try switching to Wi-Fi, using a DNS resolver (1.1.1.1), or a VPN.
  * Replit/Colab usually have open network access if your device is blocked.
* Missing fields:

  * Roblox API responses vary — the script prints `N/A` when a field is absent.
* Rate limiting:

  * Avoid making requests too frequently. Use reasonable intervals if you add monitoring.

---

## 🔭 Next improvements (ideas)

* Add live visits monitor integrated into the CLI (separate mode)
* Export CSV for spreadsheet analysis alongside JSON
* Add chart generation (small PNG) or a web dashboard
* Discord webhook integration for alerts
* Batch mode to analyze many games automatically

---

## 📝 License

This project is licensed under the MIT License.

---

## 🤝 Contributing

PRs welcome. Add tests in `tests/` and update `requirements.txt` if you add dependencies. Include a clear description and usage examples for big features.

---

## 💡 Pro tips

* Run on Replit or Colab for uninterrupted network access if your mobile network blocks Roblox APIs.
* Use `scripts/run_local.sh` to standardize running the CLI (`bash scripts/run_local.sh`).
* Add a GitHub Action to run unit tests on push for CI (example `.github/workflows/ci.yml` can run `pytest`).

Enjoy building — and if you want, I can add the Live Monitor mode or prepare a GitHub Actions CI file for this repo next.
