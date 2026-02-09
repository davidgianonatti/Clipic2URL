<table>
  <tr>
    <td width='200' align='center'>
      <img src='assets/logo.png' width='180' alt='Clipic2URL Logo'>
    </td>
    <td>
      <h1>Clipic2URL v0.2.0-beta</h1>
      <p><b>Clipic2URL</b> is a lightweight Windows productivity tool designed to eliminate friction in image sharing workflows. It automatically detects images in your clipboard and lets you choose between saving them locally or generating a public URL instantly.</p>
    </td>
  </tr>
</table>

## ✨ Key Features

- **Auto-detection**: Monitors the system clipboard for new image data.
- **Native Experience**: Integrated with Windows 11 notifications and System Tray.
- **Smart Metadata**: Displays image resolution, file size, and format.
- **Dual Action**: Quick Save to Downloads or Cloud Upload to ImgBB.
- **Tray Recall**: Double-click the tray icon to recall the last capture notification.
- **Privacy Conscious**: Uses Windows TEMP directory for processing.

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
   On first launch, a setup window will prompt you to enter your [ImgBB API key](https://api.imgbb.com/).
   The key is saved locally in a `.env` file.

## 💡 Tip

Clipic2URL works with the built-in **Snipping Tool**. Press <kbd>⊞ Win</kbd> + <kbd>⇧ Shift</kbd> + <kbd>S</kbd> to capture any area of your screen — Clipic2URL will instantly detect it and show you the notification.

## 🗺️ Product Roadmap (PM Perspective)

- [ ] **AI-Powered OCR**: Automatically extract text from captured images.
- [ ] **Smart Tagging**: Use AI to categorize captures based on visual content.
- [ ] **Image Compression**: Optimize payloads before cloud upload.

## 📜 License

This project is open source under the [MIT License](https://opensource.org/licenses/MIT) — free to use, modify, and distribute. Created by David Gianonatti.
