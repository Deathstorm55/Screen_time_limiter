import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import time
import threading
import psutil
import os
import json
import pystray
from PIL import Image, ImageDraw

CONFIG_FILE = "tracked_apps.json"
PASSWORD = "admin123"  # Change this for better security

class AppTracker:
    def __init__(self):
        self.apps = {}
        self.load_apps()

    def add_app(self, path, limit_minutes):
        self.apps[path] = {
            "limit": limit_minutes * 60,
            "start_time": None,
            "running": False
        }
        self.save_apps()

    def save_apps(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.apps, f)

    def load_apps(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, "r") as f:
                self.apps = json.load(f)

    def track_apps(self, update_gui_callback):
        while True:
            for path, info in self.apps.items():
                for proc in psutil.process_iter(['pid', 'exe']):
                    try:
                        if proc.info['exe'] and os.path.normpath(proc.info['exe']) == os.path.normpath(path):
                            if not info["start_time"]:
                                info["start_time"] = time.time()
                                info["running"] = True
                            elif time.time() - info["start_time"] >= info["limit"]:
                                psutil.Process(proc.info['pid']).terminate()
                                info["start_time"] = None
                                info["running"] = False
                    except (psutil.AccessDenied, psutil.NoSuchProcess):
                        continue
            update_gui_callback()
            time.sleep(5)

class App:
    def __init__(self, root):
        self.tracker = AppTracker()
        self.root = root
        self.root.title("Screen Time Limiter")
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.path_var = tk.StringVar()
        self.time_var = tk.StringVar()

        tk.Label(root, text="App Path:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.path_var, width=40).grid(row=0, column=1)
        tk.Button(root, text="Browse", command=self.browse_app).grid(row=0, column=2)

        tk.Label(root, text="Limit (minutes):").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.time_var).grid(row=1, column=1)
        tk.Button(root, text="Add App", command=self.add_app).grid(row=2, column=1)

        self.status_text = tk.Text(root, height=10, width=60, state="disabled")
        self.status_text.grid(row=3, column=0, columnspan=3)

        self.show_password_prompt()
        self.create_tray_icon()

        threading.Thread(target=self.tracker.track_apps, args=(self.update_gui,), daemon=True).start()

    def show_password_prompt(self):
        pwd = simpledialog.askstring("Authentication", "Enter admin password:", show="*")
        if pwd != PASSWORD:
            messagebox.showerror("Error", "Incorrect password. Exiting.")
            self.root.destroy()

    def browse_app(self):
        path = filedialog.askopenfilename()
        self.path_var.set(path)

    def add_app(self):
        path = self.path_var.get()
        try:
            minutes = int(self.time_var.get())
            if os.path.exists(path):
                self.tracker.add_app(path, minutes)
                messagebox.showinfo("Success", f"Tracking {os.path.basename(path)} for {minutes} minutes.")
            else:
                messagebox.showerror("Error", "Invalid path.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def update_gui(self):
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        for path, info in self.tracker.apps.items():
            name = os.path.basename(path)
            remaining = max(0, int(info["limit"] - (time.time() - info["start_time"])) if info["start_time"] else info["limit"])
            self.status_text.insert(tk.END, f"{name}: {remaining // 60}m {remaining % 60}s remaining\n")
        self.status_text.config(state="disabled")

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.deiconify()

    def create_tray_icon(self):
        icon_image = Image.new("RGB", (64, 64), "white")
        draw = ImageDraw.Draw(icon_image)
        draw.rectangle((16, 16, 48, 48), fill="black")
        self.icon = pystray.Icon("ScreenTimeLimiter", icon_image, "Time Limiter", menu=pystray.Menu(
            pystray.MenuItem("Show", lambda: self.show_window()),
            pystray.MenuItem("Exit", self.quit_app)
        ))
        threading.Thread(target=self.icon.run, daemon=True).start()

    def quit_app(self):
        self.icon.stop()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
