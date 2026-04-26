#!/bin/bash
set -e

echo "🚀 OpenPRIME-Final Codespaces Setup"
echo "===================================="

# Update package manager
echo "📦 Updating system packages..."
apt-get update && apt-get upgrade -y

# Install Ollama
echo "🦙 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh 2>/dev/null || echo "Ollama installation note: Please install manually if needed"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p memory temp

# Install Python dependencies
echo "🐍 Installing Python dependencies..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    pip install requests beautifulsoup4 ollama
fi

echo ""
echo "✅ Setup Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Start Ollama:          ollama serve &"
echo "2. Pull Qwen2.5 model:    ollama pull qwen2.5:7b"
echo "3. Run the agent:         python agentmain.py --llm_no 0 --verbose"
echo ""
echo "📚 For detailed instructions, see CODESPACES_SETUP.md"
echo ""
