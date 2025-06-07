import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import re, math, random, string
from datetime import datetime
from reportlab.pdfgen import canvas

def password_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32
    return len(password) * math.log2(charset) if charset else 0

def analyze_password():
    pwd = password_entry.get()
    entropy = password_entropy(pwd)
    if entropy < 28:
        strength = "❌ Weak password"
        password_result.config(foreground="#ff4d4d")
    elif entropy < 50:
        strength = "⚠️ Moderate password"
        password_result.config(foreground="#ffa500")
    else:
        strength = "✅ Strong password"
        password_result.config(foreground="#00cc66")
    result = f"Entropy: {entropy:.2f} bits\n{strength}"
    password_result.config(text=result)
    log_analysis(pwd, result)

def export_pdf():
    file = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    if file:
        c = canvas.Canvas(file)
        c.drawString(100, 750, "Password Analysis Report")
        c.drawString(100, 730, f"Password: {password_entry.get()}")
        y = 710
        for line in password_result.cget("text").split("\n"):
            c.drawString(100, y, line)
            y -= 20
        c.save()
        messagebox.showinfo("Export", "PDF Report Saved!")

def log_analysis(pwd, result):
    with open("password_logs.txt", "a") as f:
        f.write(f"[{datetime.now()}] Password: {pwd} | {result}\n")


def suggest_password():
    try:
        length = int(length_entry.get())
        if length < 8:
            raise ValueError
    except:
        length = 12
        length_entry.delete(0, tk.END)
        length_entry.insert(0, "12")

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    symbol = random.choice(string.punctuation)
    remaining = length - 4
    rest = [random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(remaining)]
    password_list = [upper, lower, digit, symbol] + rest
    random.shuffle(password_list)
    suggestion = ''.join(password_list)

    suggestion_label.config(text=f"🔑 Suggested Password:\n{suggestion}")
    copy_btn.config(state=tk.NORMAL)
    copy_btn.suggestion = suggestion

def copy_suggestion():
    root.clipboard_clear()
    root.clipboard_append(copy_btn.suggestion)
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def toggle_password():
    password_entry.config(show="" if show_var.get() else "*")


root = tk.Tk()
root.title("🛡️ Password Analyzer & Generator")
root.geometry("450x600")
root.configure(bg="#1c1c1c")

style = ttk.Style()
style.theme_use("default")
style.configure(".", background="#1c1c1c", foreground="#ffffff", font=("Bodoni Mt", 12))
style.configure("TLabel", background="#1c1c1c", foreground="#ffffff")
style.configure("TButton", background="#333333", foreground="#ffffff", padding=6, relief="flat")
style.configure("TEntry", fieldbackground="#2d2d2d", foreground="#ffffff", insertcolor="white")


ttk.Label(root, text="🔐 Password Analyzer Tool", font=("Copperplate Gothic Light", 16, "bold")).pack(pady=15)


password_frame = ttk.LabelFrame(root, text="Enter Password", padding=15)
password_frame.pack(fill="x", padx=20, pady=10)

password_entry = ttk.Entry(password_frame, show="*", width=40)
password_entry.pack(pady=5)

show_var = tk.BooleanVar()
ttk.Checkbutton(password_frame, text="Show Password", variable=show_var, command=toggle_password).pack(anchor="w")

ttk.Button(password_frame, text="Analyze Password", command=analyze_password).pack(pady=5)
ttk.Button(password_frame, text="Export Report (PDF)", command=export_pdf).pack()

password_result = ttk.Label(password_frame, text="", wraplength=500, justify="left")
password_result.pack(pady=10)


gen_frame = ttk.LabelFrame(root, text="🔧 Generate Strong Password", padding=15)
gen_frame.pack(fill="x", padx=20, pady=10)

ttk.Label(gen_frame, text="Length:").pack(anchor="w")
length_entry = ttk.Entry(gen_frame, width=5)
length_entry.insert(0, "12")
length_entry.pack(pady=5, anchor="w")

ttk.Button(gen_frame, text="Suggest Password", command=suggest_password).pack(pady=5)

suggestion_label = ttk.Label(gen_frame, text="", wraplength=500, justify="left", foreground="#66ccff")
suggestion_label.pack(pady=10)

copy_btn = ttk.Button(gen_frame, text="Copy Suggested Password", command=copy_suggestion, state="disabled")
copy_btn.pack()

root.mainloop()
