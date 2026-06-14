import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import hashlib
import os
from datetime import datetime

# ----------------------------
# CONFIG
# ----------------------------

SUSPICIOUS_STRINGS = {
    "discord.com/api/webhooks": 20,
    "HttpClient": 10,
    "WebClient": 10,
    "WebRequest": 10,
    "Process.Start": 20,
    "powershell": 25,
    "cmd.exe": 25,
    "DownloadFile": 15,
    "Registry": 10,
    "token": 5,
    "stealer": 50,
    "keylogger": 50,
    "inject": 10,
    "VirtualAlloc": 15,
    "WriteProcessMemory": 20,
    "CreateRemoteThread": 20
}

SAFE_INDICATORS = [
    "BepInEx",
    "HarmonyLib",
    "UnityEngine",
    "Photon.Pun",
    "TMPro",
    "GorillaNetworking",
    "GorillaLocomotion"
]

# ----------------------------
# HELPERS
# ----------------------------

def md5_file(path):
    h = hashlib.md5()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    return h.hexdigest()


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            h.update(chunk)

    return h.hexdigest()


def extract_text(path):
    with open(path, "rb") as f:
        data = f.read()

    return data.decode("utf-8", errors="ignore")


def analyze_file(path):
    findings = []
    safe_hits = []

    text = extract_text(path)

    score = 0

    for keyword, value in SUSPICIOUS_STRINGS.items():
        if keyword.lower() in text.lower():
            findings.append((keyword, value))
            score += value

    for item in SAFE_INDICATORS:
        if item.lower() in text.lower():
            safe_hits.append(item)

    score = max(0, min(score, 100))

    if score == 0:
        verdict = "LOW RISK"
    elif score < 30:
        verdict = "SUSPICIOUS"
    elif score < 60:
        verdict = "MEDIUM RISK"
    else:
        verdict = "HIGH RISK"

    return findings, safe_hits, score, verdict


# ----------------------------
# GUI
# ----------------------------

class AnalyzerGUI:

    def __init__(self, root):

        self.root = root
        self.current_file = None

        root.title("DLL Analyzer")
        root.geometry("900x700")
        root.configure(bg="#1e1e1e")

        title = tk.Label(
            root,
            text="DLL Analyzer",
            font=("Segoe UI", 20, "bold"),
            fg="white",
            bg="#1e1e1e"
        )

        title.pack(pady=10)

        self.file_label = tk.Label(
            root,
            text="No file selected",
            fg="lightgray",
            bg="#1e1e1e"
        )

        self.file_label.pack()

        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Open DLL",
            command=self.select_file
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Save Report",
            command=self.save_report
        ).pack(side="left", padx=5)

        self.score_label = tk.Label(
            root,
            text="Risk Score: N/A",
            font=("Segoe UI", 14),
            fg="white",
            bg="#1e1e1e"
        )

        self.score_label.pack()

        self.hash_label = tk.Label(
            root,
            text="",
            fg="lightgray",
            bg="#1e1e1e",
            justify="left"
        )

        self.hash_label.pack(pady=10)

        self.output = ScrolledText(
            root,
            bg="#121212",
            fg="white",
            insertbackground="white"
        )

        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.last_report = ""

    def select_file(self):

        path = filedialog.askopenfilename(
            filetypes=[
                ("DLL Files", "*.dll"),
                ("Executable Files", "*.exe"),
                ("All Files", "*.*")
            ]
        )

        if not path:
            return

        self.current_file = path

        self.file_label.config(
            text=os.path.basename(path)
        )

        self.run_analysis(path)

    def run_analysis(self, path):

        self.output.delete("1.0", tk.END)

        md5 = md5_file(path)
        sha256 = sha256_file(path)

        findings, safe_hits, score, verdict = analyze_file(path)

        self.hash_label.config(
            text=
            f"MD5: {md5}\n"
            f"SHA256: {sha256}"
        )

        if score < 30:
            color = "lime"
        elif score < 60:
            color = "orange"
        else:
            color = "red"

        self.score_label.config(
            text=f"Risk Score: {score}/100 | {verdict}",
            fg=color
        )

        report = []

        report.append("=" * 60)
        report.append("DLL ANALYZER REPORT")
        report.append("=" * 60)
        report.append("")
        report.append(f"File: {path}")
        report.append(f"Time: {datetime.now()}")
        report.append("")
        report.append(f"MD5: {md5}")
        report.append(f"SHA256: {sha256}")
        report.append("")
        report.append(f"Risk Score: {score}/100")
        report.append(f"Verdict: {verdict}")
        report.append("")

        report.append("SAFE INDICATORS")
        report.append("-" * 30)

        if safe_hits:
            for item in safe_hits:
                report.append(f"[+] {item}")
        else:
            report.append("None found")

        report.append("")
        report.append("SUSPICIOUS FINDINGS")
        report.append("-" * 30)

        if findings:
            for item, value in findings:
                report.append(
                    f"[!] {item} (+{value})"
                )
        else:
            report.append(
                "No suspicious strings found."
            )

        report_text = "\n".join(report)

        self.last_report = report_text

        self.output.insert(
            tk.END,
            report_text
        )

    def save_report(self):

        if not self.last_report:
            messagebox.showinfo(
                "DLL Analyzer",
                "Analyze a file first."
            )
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text File", "*.txt")
            ]
        )

        if not path:
            return

        with open(path, "w", encoding="utf-8") as f:
            f.write(self.last_report)

        messagebox.showinfo(
            "DLL Analyzer",
            "Report saved."
        )


# ----------------------------
# START
# ----------------------------

if __name__ == "__main__":

    root = tk.Tk()

    app = AnalyzerGUI(root)

    root.mainloop()