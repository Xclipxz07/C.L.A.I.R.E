# C.L.A.I.R.E Installation & Usage Guide

## 🚀 Easy Installation (Windows)

### Method 1: One-Click Install (Recommended)

1. **Double-click:** `install.bat`
2. Wait for installation to complete
3. A desktop shortcut "Claire Assistant" will be created
4. Done! ✅

### Method 2: Manual Install

Run in Command Prompt:
```cmd
cd "C:\Users\wwwdh\Desktop\C.L.A.I.R.E"
install.bat
```

---

## 🎯 How to Run Claire

### Option 1: Desktop Shortcut (After Install)
- Double-click **"Claire Assistant"** on your desktop
- GUI mode opens automatically

### Option 2: Batch Files
- **`run_claire_gui.bat`** - Opens GUI mode
- **`run_claire_terminal.bat`** - Opens terminal mode
- **`run_claire.bat`** - Choose mode on startup

Just double-click any of these!

---

## 📋 First Time Setup

### 1. Install Ollama
Download: https://ollama.ai

### 2. Download AI Model
Open PowerShell:
```powershell
ollama pull llama2
```

### 3. Start Using Claire
Double-click the desktop shortcut!

---

## 🔧 What Each File Does

| File | Purpose |
|------|---------|
| `install.bat` | First-time setup & installation |
| `run_claire.bat` | Run Claire (choose mode) |
| `run_claire_gui.bat` | Run Claire in GUI mode |
| `run_claire_terminal.bat` | Run Claire in terminal mode |

---

## ✅ Automatic Features

The launcher automatically:
- ✅ Creates virtual environment if missing
- ✅ Installs required packages if missing
- ✅ Creates config.yaml if missing
- ✅ Sets up directories

Just double-click and go!

---

## 🎨 Customization

Edit `config.yaml` to customize:
- Assistant name
- AI model (llama2, mistral, etc.)
- Personality
- Skills (weather, system control, etc.)

---

## 🆘 Troubleshooting

### "Python not found"
Install Python from: https://www.python.org/downloads/

### "Ollama connection failed"
1. Make sure Ollama is installed
2. Run: `ollama serve` in a terminal

### Desktop shortcut not working
Right-click shortcut → Properties → Check "Target" path

---

## 🚀 Next Steps

1. Run `install.bat`
2. Double-click desktop shortcut
3. Start chatting with Claire!

Enjoy your AI assistant! 🎉
