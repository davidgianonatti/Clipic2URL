<table>
  <tr>
    <td width='200' align='center'>
      <img src='assets/logo.png' width='180' alt='Clipic2URL Logo'>
    </td>
    <td>
      <h1>Clipic2URL v0.1.0-beta</h1>
      <p><b>Clipic2URL</b> is a lightweight Windows productivity tool designed to eliminate friction in image sharing workflows. It automatically detects images in your clipboard and lets you choose between saving them locally or generating a public URL instantly.</p>
    </td>
  </tr>
</table>

## ✨ Key Features
- **Auto-detection**: Monitors the system clipboard for new image data.
- **Native Experience**: Integrated with Windows 11 notifications and System Tray.
- **Smart Metadata**: Displays image resolution, file size, and format.
- **Dual Action**: Quick Save to Downloads or Cloud Upload to ImgBB.
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
Create a file named .env in the root folder and paste this:
```text
IMGBB_API_KEY=your_api_key_here
```

## 🗺️ Product Roadmap (PM Perspective)
- [ ] **AI-Powered OCR**: Automatically extract text from captured images.
- [ ] **Smart Tagging**: Use AI to categorize captures based on visual content.
- [ ] **Image Compression**: Optimize payloads before cloud upload.

## 📜 License
MIT License. Created by David Gianonatti.