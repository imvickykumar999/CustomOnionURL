import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
import math
import re

# Path to your mkp224o binary
MKP224O_PATH = "./mkp224o/mkp224o"
os.makedirs("onions", exist_ok=True)

current_process = None  # Global process ref

VALID_CHARS_PATTERN = re.compile(r'^[a-z2-7]*$')

def estimate_time(prefix):
    try:
        lscpu_out = subprocess.check_output("lscpu", shell=True).decode()
        threads = 1
        for line in lscpu_out.splitlines():
            if "CPU(s):" in line and not line.startswith("NUMA"):
                threads = int(line.split(":")[1].strip())
                break

        prefix_len = len(prefix)
        if prefix_len == 0:
            return "N/A"

        # Hash rate assumption: 1.2M hashes/sec/thread
        hashes_per_sec = threads * 1_200_000
        total_attempts = 32 ** prefix_len
        est_seconds = total_attempts / hashes_per_sec

        if est_seconds < 1:
            return "<1 second"

        # Convert seconds into y:m:d:h:m:s
        seconds = int(est_seconds)
        years, seconds = divmod(seconds, 365*24*3600)
        months, seconds = divmod(seconds, 30*24*3600)
        days, seconds = divmod(seconds, 24*3600)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        parts = []
        if years > 0:
            parts.append(f"{years} years")
        if months > 0 or years > 0:
            parts.append(f"{months} months")
        if days > 0 or months > 0 or years > 0:
            parts.append(f"{days} days")
        if hours > 0 or days > 0 or months > 0 or years > 0:
            parts.append(f"{hours} hours")
        if minutes > 0 or hours > 0 or days > 0 or months > 0 or years > 0:
            parts.append(f"{minutes} minutes")
        parts.append(f"{seconds} seconds")

        return " : ".join(parts)

    except Exception:
        return "Error estimating"

def validate_characters(new_value):
    if VALID_CHARS_PATTERN.fullmatch(new_value):
        return True
    else:
        messagebox.showwarning("Invalid Input", "Only lowercase letters (a–z) and digits 2–7 are allowed.")
        return False

def update_estimate(prefix_entry, time_box):
    prefix = prefix_entry.get().strip()
    if not prefix:
        time_box.config(state=tk.NORMAL)
        time_box.delete(0, tk.END)
        time_box.insert(0, "Estimated time will appear here")
        time_box.config(state="readonly")
        return

    if VALID_CHARS_PATTERN.fullmatch(prefix):
        est = estimate_time(prefix)
        time_box.config(state=tk.NORMAL)
        time_box.delete(0, tk.END)
        time_box.insert(0, f"Estimated time: {est}")
        time_box.config(state="readonly")

def run_mkp224o(prefix, output_box, start_btn, stop_btn):
    global current_process

    if not os.path.isfile(MKP224O_PATH):
        messagebox.showerror("Error", "mkp224o binary not found!")
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)
        return

    output_box.insert(tk.END, f"Starting mkp224o for prefix '{prefix}'...\n")
    output_box.see(tk.END)

    try:
        current_process = subprocess.Popen(
            [MKP224O_PATH, "-d", "onions", prefix],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )

        for line in current_process.stdout:
            if current_process.poll() is not None:
                break
            output_box.insert(tk.END, line)
            output_box.see(tk.END)

        current_process.wait()

    except Exception as e:
        messagebox.showerror("Execution Error", str(e))

    finally:
        current_process = None
        start_btn.config(state=tk.NORMAL)
        stop_btn.config(state=tk.DISABLED)

def start_generation(entry, output_box, time_box, start_btn, stop_btn):
    prefix = entry.get().strip()
    if not prefix or len(prefix) < 5 or len(prefix) > 16:
        messagebox.showerror("Invalid Prefix", "Prefix must be 5–16 characters.")
        return

    est = estimate_time(prefix)
    time_box.config(state=tk.NORMAL)
    time_box.delete(0, tk.END)
    time_box.insert(0, f"Estimated time: {est}")
    time_box.config(state="readonly")

    start_btn.config(state=tk.DISABLED)
    stop_btn.config(state=tk.NORMAL)

    thread = threading.Thread(target=run_mkp224o, args=(prefix, output_box, start_btn, stop_btn))
    thread.daemon = True
    thread.start()

def stop_generation(output_box, stop_btn):
    global current_process
    if current_process and current_process.poll() is None:
        output_box.insert(tk.END, "Stopping process...\n")
        current_process.terminate()
        stop_btn.config(state=tk.DISABLED)
    else:
        output_box.insert(tk.END, "No process is currently running.\n")

def main():
    root = tk.Tk()
    root.title("Tor V3 Onion Vanity Generator")
    root.configure(bg="#2e2e2e")
    root.geometry("800x550")

    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TButton", padding=6, relief="flat", background="#ffffff",
                    foreground="#000000", font=("Segoe UI", 10, "bold"))
    style.map("TButton", background=[('active', '#cccccc')], relief=[('pressed', 'sunken')])
    style.configure("TLabel", background="#2e2e2e", foreground="#ffffff", font=("Segoe UI", 10))

    ttk.Label(root, text="Enter Desired Prefix:").pack(pady=10)

    # Register validation and estimate updater
    def on_entry_change(*args):
        update_estimate(entry, time_box)

    vcmd = (root.register(validate_characters), "%P")
    entry_var = tk.StringVar()
    entry_var.trace_add("write", on_entry_change)

    # ✅ Move input field back to top (below the label)
    entry = ttk.Entry(root, width=30, validate="key", validatecommand=vcmd, textvariable=entry_var)
    entry.pack(pady=5)

    button_frame = tk.Frame(root, bg="#2e2e2e")
    button_frame.pack(pady=10)

    output_box = scrolledtext.ScrolledText(root, height=15, width=90, bg="#1e1e1e",
                                           fg="#00ff00", insertbackground="white")
    output_box.pack(padx=10, pady=10)

    # Estimated time box (kept at bottom)
    time_box = tk.Entry(root, width=40, justify="center", font=("Segoe UI", 10))
    time_box.insert(0, "Estimated time will appear here")
    time_box.config(state="readonly")
    time_box.pack(fill='x', padx=10, pady=(10, 5))

    start_btn = ttk.Button(button_frame, text="Generate .onion")
    stop_btn = ttk.Button(button_frame, text="Stop", state=tk.DISABLED)

    start_btn.config(command=lambda: start_generation(entry, output_box, time_box, start_btn, stop_btn))
    stop_btn.config(command=lambda: stop_generation(output_box, stop_btn))

    start_btn.grid(row=0, column=0, padx=10)
    stop_btn.grid(row=0, column=1, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()
