import os
import time
import requests
import pyperclip
import threading
import io
import pystray
import sys
from datetime import datetime
from PIL import ImageGrab, Image, ImageOps
from pystray import MenuItem as item
from dotenv import load_dotenv
from win11toast import toast

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

API_KEY = os.getenv("IMGBB_API_KEY")
TEMP_FOLDER = os.getenv('TEMP')
SAVE_DIR = os.path.join(os.path.expanduser("~"), "Downloads")

APP_ID = "Clipic2URL"
LOGO_PATH = os.path.join(BASE_DIR, "assets", "logo.png")

# --- IMAGE & API LOGIC ---

def get_image_metadata(img):
    width, height = img.size
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    size_kb = img_buffer.tell() / 1024
    weight_str = f"{size_kb / 1024:.2f} MB" if size_kb > 1024 else f"{int(size_kb)} KB"
    return f"{width} x {height}px - {weight_str} - PNG"

def on_quick_save(img):
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(SAVE_DIR, f"clip_{timestamp}.png")
        img.save(file_path, "PNG")
        toast(APP_ID, "Saved to Downloads! 📁", icon=LOGO_PATH, app_id=APP_ID)
        return file_path
    except Exception:
        return None

def on_copy_url(img):
    if not API_KEY:
        toast(APP_ID, "Error: Missing API Key in .env", icon=LOGO_PATH, app_id=APP_ID)
        return

    temp_path = os.path.join(TEMP_FOLDER, f"clipic_upload_{int(time.time())}.png")
    try:
        img.save(temp_path, "PNG")
        response = requests.post(
            "https://api.imgbb.com/1/upload", 
            params={"key": API_KEY}, 
            files={"image": open(temp_path, "rb")},
            timeout=15 
        )
        
        if response.status_code == 200:
            public_url = response.json()["data"]["url"]
            pyperclip.copy(public_url)
            toast(APP_ID, "Public URL copied to clipboard! ✅", icon=LOGO_PATH, app_id=APP_ID)
        
        if os.path.exists(temp_path):
            os.remove(temp_path)
    except Exception:
        if os.path.exists(temp_path): os.remove(temp_path)
        toast(APP_ID, "Upload failed (Connection error).", icon=LOGO_PATH, app_id=APP_ID)

# --- NOTIFICATIONS & UI ---

def show_clipic_notification(img):
    preview_path = os.path.join(TEMP_FOLDER, "clipic_preview.png")
    metadata = get_image_metadata(img)
    
    try:
        img.save(preview_path)
        res = toast(
            APP_ID, 
            metadata,
            icon=LOGO_PATH,
            image=preview_path,
            buttons=['Quick Save', 'Copy URL'],
            app_id=APP_ID,
            audio={'silent': True},
            duration='short'
        )

        if res and 'arguments' in res:
            if 'Quick Save' in res['arguments']:
                on_quick_save(img)
            elif 'Copy URL' in res['arguments']:
                on_copy_url(img)
    except Exception:
        pass

# --- SYSTEM TRAY & MONITOR ---

def setup_tray():
    try:
        # On charge le logo cropped et on le redimensionne proprement pour le tray
        icon_img = Image.open(LOGO_PATH).resize((32, 32), Image.Resampling.LANCZOS)
    except Exception:
        icon_img = Image.new('RGB', (32, 32), color=(0, 120, 215))
    
    def on_exit(icon, item):
        icon.stop()
        os._exit(0)

    icon = pystray.Icon(APP_ID, icon_img, APP_ID, menu=pystray.Menu(
        item('Exit', on_exit)
    ))
    icon.run()

def monitor_clipboard():
    last_hash = None
    while True:
        try:
            img = ImageGrab.grabclipboard()
            if img and isinstance(img, Image.Image):
                current_hash = hash(img.tobytes())
                if current_hash != last_hash:
                    threading.Thread(target=show_clipic_notification, args=(img,), daemon=True).start()
                    last_hash = current_hash
        except Exception:
            pass
        time.sleep(1)

if __name__ == "__main__":
    threading.Thread(target=setup_tray, daemon=True).start()
    monitor_clipboard()