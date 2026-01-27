# 📋 Clipic2URL v0.1.0-beta

<p align='center'>
  <img src='assets/logo.png' width='180' alt='Logo'>
</p>

**Clipic2URL** is a lightweight Windows productivity tool. It automatically detects images in your clipboard and lets you choose between saving them locally or generating a public URL instantly.

## ✨ Key Features
- **Auto-detection**: Monitors the system clipboard for new image data.
- **Native Experience**: Integrated with Windows 11 notifications and System Tray.
- **Smart Metadata**: Displays image resolution, file size, and format.
- **Dual Action**: Quick Save to Downloads or Cloud Upload to ImgBB.

## 🛠️ Tech Stack
- Python 3.10+, win11toast, Pillow, ImgBB API, pystray.

## 🚀 Installation & Setup

1. **Clone the repository**:
```bash
git clone https://github.com/davidgianonatti/Clipic2URL.git
cd Clipic2URL
```

2. **Set up the environment**:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure your API Key**:
Create a file named .env and paste this:
```text
IMGBB_API_KEY=your_api_key_here
```

## 📜 License
MIT License. Created by David Gianonatti.