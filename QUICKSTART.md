"""
Quick Start Guide for C.L.A.I.R.E
Step-by-step setup instructions
"""

# C.L.A.I.R.E Quick Start Guide

## Step 1: Install Python
Make sure Python 3.10+ is installed:
```bash
python --version
```

## Step 2: Create Virtual Environment
```bash
cd "C:\Users\wwwdh\Desktop\C.L.A.I.R.E"
python -m venv venv
```

## Step 3: Activate Virtual Environment

### Windows:
```bash
venv\Scripts\activate
```

### Mac/Linux:
```bash
source venv/bin/activate
```

## Step 4: Install Dependencies

### Basic Installation (Text-only mode):
```bash
pip install openai pyyaml requests python-dotenv
```

### Full Installation (with voice):
```bash
pip install -r requirements.txt
```

Note: PyAudio (for voice) may require additional setup on Windows:
```bash
pip install pipwin
pipwin install pyaudio
```

## Step 5: Configure Settings
```bash
# Copy example config
copy config.example.yaml config.yaml

# Edit config.yaml and add your API keys:
# - Get OpenAI API key from: https://platform.openai.com/
# - Get Weather API key from: https://openweathermap.org/api (free)
```

## Step 6: Run Claire
```bash
python main.py
```

## Troubleshooting

### Issue: "OpenAI API key not configured"
**Solution**: Add your API key to config.yaml under `ai.openai_api_key`

### Issue: "PyQt6 not found"
**Solution**: 
- Use terminal mode (option 1) instead
- Or install PyQt6: `pip install PyQt6`

### Issue: "PyAudio failed to install"
**Solution**: 
- Windows: `pip install pipwin` then `pipwin install pyaudio`
- Mac: `brew install portaudio` then `pip install pyaudio`
- Linux: `sudo apt-get install portaudio19-dev` then `pip install pyaudio`

### Issue: "Speech recognition not working"
**Solution**: 
- Start with text-only mode
- Check microphone permissions
- Install: `pip install SpeechRecognition pyaudio`

## What to Try First

1. **Test Basic Mode**:
   ```
   You: hello
   You: what time is it?
   You: what's the date?
   You: help
   ```

2. **Test AI (if configured)**:
   ```
   You: tell me a joke
   You: explain quantum computing in simple terms
   You: help me plan my day
   ```

3. **Test Skills**:
   ```
   You: what's the weather?
   You: open notepad
   You: open chrome
   ```

## Next Steps

1. **Get API Keys**:
   - OpenAI: https://platform.openai.com/api-keys (required for AI)
   - OpenWeatherMap: https://openweathermap.org/api (optional, for weather)

2. **Customize**:
   - Edit assistant name in config.yaml
   - Adjust personality and response style
   - Enable/disable skills

3. **Add Features**:
   - Check README.md for advanced features
   - Explore backend/skills/ to add custom skills
   - Try voice mode once configured

## Getting Help

- Check README.md for full documentation
- Review config.example.yaml for all options
- Check logs in logs/claire.log for errors
- Search for "Python voice assistant" tutorials online

## Cost Considerations

**OpenAI API** (Pay-as-you-go):
- GPT-3.5-Turbo: ~$0.001-0.002 per interaction
- GPT-4: ~$0.03-0.06 per interaction
- Budget: ~$5-10/month for light use

**Free Alternatives**:
- Use Ollama for local LLMs (no API costs)
- Use basic mode without AI (just commands)
- Use free weather APIs

Enjoy your personal AI assistant! 🚀
