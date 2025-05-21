import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import shlex

def send_request():
    url = url_entry.get().strip()
    method = method_var.get()
    http_version = http_version_var.get()
    headers = headers_text.get("1.0", tk.END).strip().splitlines()
    body = body_text.get("1.0", tk.END).strip()

    if not url:
        messagebox.showerror("Error", "URL cannot be empty.")
        return

    if not url.startswith(("http://", "https://")):
        messagebox.showerror("Error", "URL must start with http:// or https://")
        return

    try:
        cmd = f"curl -s -X {method}"

        if http_version == "HTTP/1.0":
            cmd += " --http1.0"
        elif http_version == "HTTP/1.1":
            cmd += " --http1.1"
        elif http_version == "HTTP/2":
            cmd += " --http2"
        elif http_version == "HTTP/3":
            cmd += " --http3"

        for header in headers:
            if ':' in header:
                cmd += f" -H {shlex.quote(header.strip())}"

        if method in ["POST", "PUT", "PATCH"] and body:
            cmd += f" -d {shlex.quote(body)}"

        cmd += f" {shlex.quote(url)}"

        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, result.stdout)

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Curl")

# Dark mode colors
bg_color = "#1e1e1e"
fg_color = "#e0e0e0"
entry_bg = "#2e2e2e"

root.configure(bg=bg_color)
root.geometry("730x630")  # Window Size

title_label = tk.Label(root, text="Curl GUI Client", font=("Segoe UI", 14, "bold"), fg=fg_color, bg=bg_color)
title_label.pack(pady=(15, 10))


form_frame = tk.Frame(root, bg=bg_color)
form_frame.pack(anchor="w", padx=20)

def create_label(parent, text, row):
    label = tk.Label(parent, text=text, fg=fg_color, bg=bg_color)
    label.grid(row=row, column=0, sticky="w", padx=(0, 2), pady=3)
    return label

# URL
create_label(form_frame, "URL:", 0)
url_entry = tk.Entry(form_frame, width=55, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
url_entry.grid(row=0, column=1, pady=3, sticky="w")

# Method
create_label(form_frame, "Method:", 1)
method_var = tk.StringVar(value="GET")
method_menu = ttk.Combobox(form_frame, textvariable=method_var, values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD"], width=20)
method_menu.grid(row=1, column=1, pady=3, sticky="w")

# HTTP Version
create_label(form_frame, "HTTP Version:", 2)
http_version_var = tk.StringVar(value="Default")
http_version_menu = ttk.Combobox(form_frame, textvariable=http_version_var, values=["Default", "HTTP/1.0", "HTTP/1.1", "HTTP/2", "HTTP/3"], width=20)
http_version_menu.grid(row=2, column=1, pady=3, sticky="w")

# Headers
create_label(form_frame, "Headers:", 3)
headers_text = scrolledtext.ScrolledText(form_frame, width=58, height=4, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
headers_text.grid(row=3, column=1, pady=3, sticky="w")

# Body
create_label(form_frame, "Body:", 4)
body_text = scrolledtext.ScrolledText(form_frame, width=58, height=4, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
body_text.grid(row=4, column=1, pady=3, sticky="w")

# Send button
send_button = tk.Button(form_frame, text="Send Request", command=send_request, bg="#3a3a3a", fg=fg_color)
send_button.grid(row=5, column=1, sticky="e", padx=(0, 10), pady=10)

# Response
create_label(form_frame, "Response:", 6)
result_text = scrolledtext.ScrolledText(form_frame, width=70, height=15, bg=entry_bg, fg=fg_color, insertbackground=fg_color)
result_text.grid(row=6, column=1, pady=(3, 10), sticky="w")

root.mainloop()
