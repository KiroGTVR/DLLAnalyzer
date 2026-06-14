# DLL Analyzer

🔍 A lightweight Windows utility for educational static analysis of DLL and EXE files.

DLL Analyzer helps inspect files by calculating hashes, detecting common modding libraries, searching for suspicious strings, and generating simple risk reports.

> This tool performs static analysis only. It cannot guarantee that a file is safe or malicious.

---

## Features

- SHA256 hashing
- MD5 hashing
- DLL and EXE support
- Suspicious string detection
- Modding library detection
- Risk scoring system
- Report generation
- Save reports as text files
- Simple and lightweight interface

---

## Screenshots

_Add screenshots here._

---

## How It Works

DLL Analyzer scans files without executing them.

The analyzer:

- Reads file contents
- Calculates hashes
- Searches for known keywords
- Detects common modding frameworks
- Generates a basic risk score
- Produces a human-readable report

Examples of detected libraries:

- BepInEx
- HarmonyLib
- UnityEngine
- Photon.Pun

Examples of monitored strings:

- WebClient
- HttpClient
- Process.Start
- powershell
- discord.com/api/webhooks

---

## Installation

### Option 1: Download Release

Download the latest release from the Releases page.

### Option 2: Run From Source

Requirements:

- Python 3.10+
- Tkinter

Run:

```bash
python app.py
```

---

## Building

Build a standalone executable using PyInstaller:

```bash
pyinstaller --clean --onefile --windowed --icon=icon.ico --name DLLAnalyzer app.py
```

The compiled executable will be located in:

```text
dist/DLLAnalyzer.exe
```

---

## Example Report

```text
============================================================
DLL ANALYZER REPORT
============================================================

File: Example.dll

Risk Score: 10/100
Verdict: LOW RISK

SAFE INDICATORS
------------------------------
[+] BepInEx
[+] HarmonyLib

SUSPICIOUS FINDINGS
------------------------------
[!] HttpClient (+10)
```

---

## Disclaimer

DLL Analyzer is intended for educational and research purposes.

A low risk score does not guarantee that a file is safe.

A high risk score does not guarantee that a file is malicious.

Always use caution when running software from untrusted sources.

---

## Roadmap

### Version 1.1
- Better risk scoring
- Additional keyword detection
- Improved reporting

### Version 1.2
- PE metadata analysis
- File entropy checks
- Improved UI

### Version 2.0
- .NET assembly inspection
- Import analysis
- Enhanced report export

---

## License

MIT License

---

Made with ❤️ using Python and Tkinter.
