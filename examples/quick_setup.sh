#!/bin/bash
# Quick setup script for Concordia with .env file

echo "🚀 Setting up Concordia with .env file..."

# Check if .env.example exists
if [ ! -f "../.env.example" ]; then
    echo "❌ .env.example not found. Make sure you're in the examples directory."
    exit 1
fi

# Copy .env.example to .env
if [ ! -f "../.env" ]; then
    cp ../.env.example ../.env
    echo "📁 Created .env file from template"
else
    echo "📁 .env file already exists"
fi

# Install python-dotenv if not installed
echo "📦 Checking python-dotenv installation..."
python -c "import dotenv" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing python-dotenv..."
    pip install python-dotenv
else
    echo "✅ python-dotenv already installed"
fi

echo ""
echo "🔧 Setup complete! Next steps:"
echo "1. Edit the .env file and add your API keys:"
echo "   code ../.env"
echo ""
echo "2. Add your Gemini API key:"
echo "   GOOGLE_API_KEY=your_actual_api_key_here"
echo ""
echo "3. Run the test:"
echo "   python test_gemini_simple.py"
echo ""
echo "📖 For detailed instructions, see: setup_instructions.md"