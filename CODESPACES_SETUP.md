# GitHub Codespaces Setup Guide for OpenPRIME-Final

## ⚡ Quick Start (5 minutes)

Once your Codespace is created, run these commands in the terminal:

```bash
# 1. Start Ollama in the background
ollama serve &

# 2. Wait a moment for Ollama to initialize
sleep 3

# 3. Pull the Qwen2.5 7B model (takes 5-15 minutes)
ollama pull qwen2.5:7b

# 4. Run the OpenPRIME agent
python agentmain.py --llm_no 0 --verbose
```

---

## 📋 Step-by-Step Setup

### Step 1: Create a Codespace
1. Go to your repository: https://github.com/kevinleestites2-dev/OpenPRIME-Final
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to initialize (2-3 minutes)
4. The setup script will run automatically

### Step 2: Start Ollama
```bash
ollama serve &
```
This starts the Ollama LLM service in the background. Allow 2-3 seconds for initialization.

### Step 3: Pull the Qwen2.5 Model
```bash
ollama pull qwen2.5:7b
```
⏱️ **First time takes 5-15 minutes** (~4.7GB model download)

### Step 4: Verify the Model
```bash
ollama run qwen2.5:7b "What is 2+2?"
```
If this works, Ollama is properly configured.

### Step 5: Configure Your API Keys
Edit `mykey.py` with any required API keys:
```bash
nano mykey.py
```

### Step 6: Run the Agent
```bash
python agentmain.py --llm_no 0 --verbose
```

- `--llm_no 0` → Use the first LLM (Ollama)
- `--verbose` → Show detailed output

---

## 🧪 Testing & Verification

### Check if Ollama is running:
```bash
curl http://localhost:11434/api/tags
```
Expected output: JSON list of installed models

### Check installed models:
```bash
ollama list
```

### Test the model directly:
```bash
ollama run qwen2.5:7b "Hello! Tell me about yourself in one sentence."
```

### View available LLMs in agent:
Run the agent and it will show which LLMs are available on startup.

---

## 🔧 Troubleshooting

### Issue: "ollama: command not found"
**Solution:** The setup script may not have completed. Run manually:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Issue: Model download stuck or timing out
**Solution:** Try pulling with explicit timeout:
```bash
timeout 600 ollama pull qwen2.5:7b
```
Or pull a smaller model first to test:
```bash
ollama pull tinyllama
```

### Issue: Port 11434 already in use
**Solution:** Kill the existing Ollama process and restart:
```bash
pkill ollama
sleep 2
ollama serve &
```

### Issue: Out of memory / Codespace running slow
**Solution:** 
- Close VS Code extensions you don't need
- Free up space: `rm -rf ~/.cache/ollama/*` (saves ~2GB)
- Upgrade Codespace specs if available

### Issue: Agent won't start with "BAD Mixin config"
**Solution:** Check `mykey.py` - ensure it has proper LLM configuration. For Ollama-only, minimal config:
```python
mykeys = {
    'ollama_api': {
        'base_url': 'http://localhost:11434',
        'model': 'qwen2.5:7b'
    }
}
```

---

## 📊 Performance Tips

1. **First model inference is slower** - Model loads into memory (can take 30-60 seconds)
2. **Use smaller models** - If 7B is too slow, try `ollama pull qwen2.5:0.5b`
3. **Free up space** - Codespaces have limited storage (~30GB). After pulling models, check space:
   ```bash
   df -h
   ```

4. **Background processes** - Keep Ollama in background with `&` to free up terminal

---

## 📝 Command Reference

```bash
# Ollama Commands
ollama serve &              # Start Ollama service in background
ollama serve               # Start Ollama in foreground (blocking)
ollama list                # List all downloaded models
ollama run qwen2.5:7b      # Run model interactively
ollama pull qwen2.5:7b     # Download model
ollama rm qwen2.5:7b       # Delete model
pkill ollama               # Stop Ollama service

# OpenPRIME Agent Commands
python agentmain.py --llm_no 0 --verbose        # Start with Ollama
python agentmain.py --task mytask --input "..."  # One-shot task mode
python agentmain.py --help                       # Show all options

# Utility Commands
curl http://localhost:11434/api/tags             # Check Ollama API
ps aux | grep ollama                             # Check if Ollama is running
```

---

## 🚀 Advanced Usage

### Task Mode (Non-interactive)
```bash
python agentmain.py --task mytask --input "Analyze this text and summarize it"
```

### Reflect Mode (Auto-trigger on file changes)
```bash
python agentmain.py --reflect my_script.py
```

### Background Mode
```bash
python agentmain.py --task mytask --bg
```

### Switch LLM during runtime
When agent is running interactively, you can type commands like:
```
/session.model=qwen2.5:7b
```

---

## 🔗 Useful Links

- **Ollama Documentation**: https://github.com/ollama/ollama
- **Qwen2.5 Model Card**: https://huggingface.co/Qwen/Qwen2.5-7B
- **GitHub Codespaces Docs**: https://docs.github.com/en/codespaces
- **OpenPRIME Repository**: https://github.com/kevinleestites2-dev/OpenPRIME-Final

---

## ✨ Tips & Tricks

- **Keep terminal history**: All commands are saved in `.bash_history`
- **Persistent storage**: Files in your repo are always saved
- **Port forwarding**: Ports 11434, 8000, and 3000 are automatically forwarded
- **VS Code Extensions**: Copilot, Python, and Pylance pre-installed

---

Happy coding with OpenPRIME! 🎉
