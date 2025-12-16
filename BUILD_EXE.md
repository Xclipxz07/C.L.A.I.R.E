# Building Claire as a Standalone .exe

## 🎯 Quick Build

**Just double-click:** `build_exe.bat`

This will create a standalone `Claire.exe` that works without Python!

---

## 📦 What Gets Created

After building, you'll have:
```
dist/
  Claire/
    Claire.exe          <- Your standalone app!
    config.example.yaml
    logs/
    data/
    README.md
    (and other required files)
```

**Total size:** ~50-100 MB (includes everything needed)

---

## 🚀 How to Build

### Step 1: Build the .exe
```cmd
double-click: build_exe.bat
```
Wait 2-5 minutes for the build to complete.

### Step 2: Find Your .exe
Look in: `dist\Claire\Claire.exe`

### Step 3: Test It
Double-click `Claire.exe` - it should work!

---

## 📤 How to Share/Distribute

**To give Claire to others:**

1. **Copy the entire folder:** `dist\Claire\`
2. **Share it** (zip it if needed)
3. **Users just run:** `Claire.exe`

✅ **No Python needed**  
✅ **No pip install**  
✅ **Just click and run!**

---

## 💡 What Users Need

Your friends/family only need:
- ✅ Windows PC
- ✅ Ollama installed (for AI features)

That's it! Everything else is included in the .exe.

---

## 🎨 Optional: Add an Icon

1. Get a `.ico` file (Claire icon)
2. Save it as `claire.ico` in the project folder
3. Edit `claire.spec`, change:
   ```python
   icon=None,
   ```
   to:
   ```python
   icon='claire.ico',
   ```
4. Run `build_exe.bat` again

---

## 🔧 Build Options

### One-File Build (Single .exe, no folder)

Edit `claire.spec` and change:
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,        # Add these three lines
    a.zipfiles,        # to bundle everything
    a.datas,           # into one file
    [],
    name='Claire',
    ...
    onefile=True,      # Add this line
)
```

Then remove the `COLLECT` section and rebuild.

**Result:** Single 100MB `Claire.exe` file (slower startup)

---

## 🐛 Troubleshooting

### "PyInstaller not found"
The script auto-installs it. If it fails, run manually:
```cmd
venv\Scripts\pip install pyinstaller
```

### Build fails
1. Make sure venv exists: `python -m venv venv`
2. Install dependencies: `pip install -r requirements-minimal.txt`
3. Try again: `build_exe.bat`

### .exe won't start
- Run from command prompt to see errors
- Check if config.yaml exists in same folder
- Make sure Ollama is installed

---

## 📊 .exe vs .bat Comparison

| Feature | .bat Launcher | .exe Standalone |
|---------|--------------|-----------------|
| Python required | ✅ Yes | ❌ No |
| Size | Small (~1KB) | Large (~100MB) |
| Speed | Fast | Slightly slower |
| Distribution | Need Python | Just copy folder |
| Updates | Edit .py files | Rebuild .exe |

**Use .exe for:** Sharing with non-technical users  
**Use .bat for:** Personal use, development

---

## 🎯 Next Steps

1. Run `build_exe.bat`
2. Wait for build to complete
3. Test `dist\Claire\Claire.exe`
4. Share the `dist\Claire` folder with others!

Your AI assistant is now a standalone app! 🎉
