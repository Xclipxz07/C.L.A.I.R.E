# C.L.A.I.R.E - Privacy-First AI Assistant

## 🔒 100% Private & Local Setup

### Quick Setup Guide

## Step 1: Install Ollama (Local AI)

**Download Ollama**: https://ollama.ai

**Windows:**
- Download the installer
- Run and install
- It will start automatically

**Mac:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Step 2: Install AI Model

```bash
# Install Llama 2 (7B - good balance)
ollama pull llama2

# Or try other models:
ollama pull mistral      # Fast and smart
ollama pull phi          # Lightweight (2GB)
ollama pull codellama    # Best for coding
ollama pull gemma        # Google's model
```

## Step 3: Start Ollama Server

```bash
ollama serve
```

Keep this running in a separate terminal.

## Step 4: Install C.L.A.I.R.E

```bash
cd "C:\Users\wwwdh\Desktop\Claire"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Step 5: Configure

```bash
copy config.example.yaml config.yaml
```

The default config is already set for Ollama - no API keys needed!

## Step 6: Run Claire

```bash
python main.py
```

## 🎯 Privacy Features

✅ **All data stays on your computer**
✅ **No internet required** (after model download)
✅ **No API keys or accounts**
✅ **No data sent to third parties**
✅ **Fully open source**

## 📊 Model Comparison

| Model | Size | RAM | Speed | Quality | Best For |
|-------|------|-----|-------|---------|----------|
| phi | 2.7GB | 4GB | ⚡⚡⚡ | ⭐⭐⭐ | Quick tasks |
| llama2 | 7GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐ | General use |
| mistral | 7GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Best balance |
| codellama | 7GB | 8GB | ⚡⚡ | ⭐⭐⭐⭐⭐ | Programming |

## 🔧 Troubleshooting

### "Cannot connect to Ollama"
**Solution**: 
```bash
# Make sure Ollama is running
ollama serve
```

### "Model not found"
**Solution**: 
```bash
# Pull the model first
ollama pull llama2
```

### "Out of memory"
**Solution**: 
- Use a smaller model: `ollama pull phi`
- Or close other applications

## 🚀 Usage Examples

```
You: Hello!
Claire: Hello! I'm Claire, your AI assistant. How can I help you today?

You: explain quantum computing
Claire: [Detailed explanation - all processed locally!]

You: what's the weather?
Claire: [Uses weather skill if configured]
```

## ⚙️ Advanced Configuration

Edit `config.yaml`:

```yaml
ai:
  provider: "ollama"
  ollama:
    url: "http://localhost:11434"
    model: "mistral"  # Change model here
    temperature: 0.7   # Creativity (0-1)
```

## 🎓 Available Commands

```bash
# List installed models
ollama list

# Remove a model
ollama rm llama2

# Update Ollama
# Windows: Re-download installer
# Mac: brew upgrade ollama
# Linux: curl -fsSL https://ollama.ai/install.sh | sh
```

## 💡 Tips

1. **First response is slow** - Model loads into RAM
2. **Subsequent responses are fast** - Model stays loaded
3. **Close Ollama when not in use** - Frees up RAM
4. **Try different models** - Find what works best for you

## 🆚 Why Ollama?

**Before (OpenAI):**
- ❌ Costs ~$0.01-0.10 per query
- ❌ Requires internet
- ❌ Data sent to OpenAI servers
- ❌ Requires API key/account

**Now (Ollama):**
- ✅ Completely free
- ✅ Works offline
- ✅ 100% private
- ✅ No accounts needed

Enjoy your fully private AI assistant! 🎉
