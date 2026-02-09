import os
import sys
import time
import requests
import pyperclip
import threading
import io
import ctypes
import pystray
import webbrowser
import customtkinter as ctk
from datetime import datetime
from PIL import ImageGrab, Image
from pystray import MenuItem as item
from dotenv import load_dotenv
from win11toast import toast

# --- GESTION DES CHEMINS (EXE vs SCRIPT) ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# --- CONFIGURATION ---
VERSION = "0.2.0-beta"
BASE_DIR = os.getcwd() 
ENV_PATH = os.path.join(BASE_DIR, ".env")
load_dotenv(ENV_PATH)

APP_ID = "Clipic2URL"
LOGO_PATH = resource_path(os.path.join("assets", "logo.png"))
# Couleur Bleu Windows Standard
MAIN_BLUE = "#0078D7"

# Dernière capture (partagée entre threads)
last_capture = {"img": None, "api_key": None}

# --- FENÊTRE DE CONFIGURATION (LOOK WINDOWS STANDARD) ---

class ApiKeyWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Setup Thème Clair / Standard
        ctk.set_appearance_mode("light") 
        ctk.set_default_color_theme("blue")

        self.title(f"{APP_ID} - Setup")
        self.geometry("440x380")
        self.resizable(False, False)
        self.configure(fg_color="#F3F3F3") # Gris très clair Windows standard
        self.attributes("-topmost", True)

        # Centrage
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - (440 // 2)
        y = (self.winfo_screenheight() // 2) - (380 // 2)
        self.geometry(f"+{x}+{y}")

        self.result_key = None

        # 1. Logo (plus grand pour l'onboarding)
        try:
            logo_img = Image.open(LOGO_PATH)
            self.logo_ctk = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(90, 90))
            self.logo_label = ctk.CTkLabel(self, image=self.logo_ctk, text="")
            self.logo_label.pack(pady=(25, 10))
        except:
            pass

        # 2. Titre
        self.label_title = ctk.CTkLabel(self, text=APP_ID, font=("Segoe UI", 22, "bold"), text_color="#333333")
        self.label_title.pack(pady=0)

        # 3. Description
        self.label_desc = ctk.CTkLabel(self, text="Please enter your ImgBB API Key to continue", 
                                       font=("Segoe UI", 13), text_color="#555555")
        self.label_desc.pack(pady=(5, 5))

        # 4. Lien vers l'API
        self.label_link = ctk.CTkLabel(self, text="Get your free key at: api.imgbb.com", 
                                       font=("Segoe UI", 11, "underline"), 
                                       text_color=MAIN_BLUE, cursor="hand2")
        self.label_link.pack(pady=(0, 15))
        self.label_link.bind("<Button-1>", lambda e: webbrowser.open("https://api.imgbb.com/"))

        # 5. Champ de saisie
        self.entry_key = ctk.CTkEntry(self, placeholder_text="Paste your API key here...", 
                                      width=320, height=35, 
                                      fg_color="#FFFFFF", border_color="#CCCCCC",
                                      text_color="#000000")
        self.entry_key.pack(pady=10)
        self.entry_key.focus()

        # 6. Boutons
        self.btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.btn_frame.pack(pady=(20, 0))

        self.btn_cancel = ctk.CTkButton(self.btn_frame, text="Cancel", 
                                        width=100, height=32,
                                        fg_color="#E5E5E5", text_color="#333333", 
                                        hover_color="#D5D5D5", command=self.on_cancel)
        self.btn_cancel.pack(side="left", padx=10)

        self.btn_save = ctk.CTkButton(self.btn_frame, text="Connect", 
                                      width=160, height=32,
                                      fg_color=MAIN_BLUE, text_color="#FFFFFF",
                                      hover_color="#005A9E", font=("Segoe UI", 12, "bold"), 
                                      command=self.save_key)
        self.btn_save.pack(side="left", padx=10)

    def save_key(self):
        key = self.entry_key.get().strip()
        if key:
            with open(ENV_PATH, "w") as f:
                f.write(f"IMGBB_API_KEY={key}")
            self.result_key = key
            self.destroy()
        else:
            self.entry_key.configure(border_color="#FF4444")

    def on_cancel(self):
        sys.exit()

# --- LOGIQUE CORE ---

def get_image_metadata(img):
    width, height = img.size
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    size_kb = img_buffer.tell() / 1024
    weight_str = f"{size_kb / 1024:.2f} MB" if size_kb > 1024 else f"{int(size_kb)} KB"
    return f"{width} x {height}px - {weight_str} - PNG"

def on_quick_save(img):
    try:
        ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = os.path.join(os.path.expanduser("~"), "Downloads", f"clip_{ts}.png")
        img.save(path, "PNG")
        toast(APP_ID, "Saved to Downloads! 📁", icon=LOGO_PATH, app_id=APP_ID)
    except: pass

def on_copy_url(img, api_key):
    print(f"[Clipic2URL] on_copy_url called, key={api_key[:8]}...")
    temp_path = os.path.join(os.getenv('TEMP'), f"clipic_up_{int(time.time())}.png")
    try:
        img.save(temp_path, "PNG")
        with open(temp_path, "rb") as f:
            res = requests.post("https://api.imgbb.com/1/upload", params={"key": api_key}, files={"image": f}, timeout=5)
        if res.status_code == 200:
            public_url = res.json()["data"]["url"]
            pyperclip.copy(public_url)
            toast(APP_ID, "Public URL copied to clipboard! ✅", icon=LOGO_PATH, app_id=APP_ID)
        else:
            print(f"[Clipic2URL] Upload error {res.status_code}: {res.text}")
            toast(APP_ID, f"Upload failed ({res.status_code}).", icon=LOGO_PATH, app_id=APP_ID)
    except Exception as e:
        print(f"[Clipic2URL] Upload exception: {e}")
        toast(APP_ID, f"Upload failed: {e}", icon=LOGO_PATH, app_id=APP_ID)
    finally:
        if os.path.exists(temp_path): os.remove(temp_path)

def show_clipic_notification(img, api_key):
    last_capture["img"] = img
    last_capture["api_key"] = api_key
    preview_path = os.path.join(os.getenv('TEMP'), "clipic_preview.png")
    try:
        img.save(preview_path)
        res = toast(APP_ID, get_image_metadata(img), icon=LOGO_PATH, image=preview_path, buttons=['Quick Save', 'Copy URL'], app_id=APP_ID, audio={'silent': True}, duration='short')
        print(f"[Clipic2URL] Toast result: {res}")
        if res and 'arguments' in res:
            if 'Quick Save' in res['arguments']: on_quick_save(img)
            elif 'Copy URL' in res['arguments']: on_copy_url(img, api_key)
    except Exception as e:
        print(f"[Clipic2URL] Notification error: {e}")

def on_show_last(icon, menuitem):
    img = last_capture.get("img")
    api_key = last_capture.get("api_key")
    if img and api_key:
        threading.Thread(target=show_clipic_notification, args=(img, api_key), daemon=True).start()
    else:
        toast(APP_ID, "No capture yet.", icon=LOGO_PATH, app_id=APP_ID)

def setup_tray():
    try: icon_img = Image.open(LOGO_PATH).resize((32, 32), Image.Resampling.LANCZOS)
    except: icon_img = Image.new('RGB', (32, 32), color=(0, 120, 215))
    icon = pystray.Icon(APP_ID, icon_img, f"{APP_ID} v{VERSION}", menu=pystray.Menu(
        item('Show last capture', on_show_last, default=True),
        pystray.Menu.SEPARATOR,
        item(f'Version {VERSION}', lambda: None, enabled=False),
        item('Exit', lambda i, n: os._exit(0))
    ))
    icon.run()

def monitor_clipboard(api_key):
    last_hash = None
    while True:
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):
                h = hash(img.tobytes())
                if h != last_hash:
                    threading.Thread(target=show_clipic_notification, args=(img, api_key), daemon=True).start()
                    last_hash = h
        except: pass
        time.sleep(1)

if __name__ == "__main__":
    # --- Single Instance Check (Windows Mutex) ---
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\Clipic2URL_SingleInstance")
    if ctypes.windll.kernel32.GetLastError() == 183:  # ERROR_ALREADY_EXISTS
        toast(APP_ID, "Clipic2URL is already running.", icon=LOGO_PATH, app_id=APP_ID)
        sys.exit(0)

    # Chargement initial de la clé
    current_key = os.getenv("IMGBB_API_KEY")
    
    # Si la clé est absente ou par défaut
    if not current_key or current_key == "your_api_key_here":
        app = ApiKeyWindow()
        app.mainloop()
        current_key = app.result_key
    
    # Si on a une clé (soit existante, soit saisie)
    if current_key:
        threading.Thread(target=setup_tray, daemon=True).start()
        monitor_clipboard(current_key)