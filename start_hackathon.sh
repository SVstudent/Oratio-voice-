#!/bin/bash

# AWS x Datadog GenAI Hackathon - Quick Start Script

echo "🏆 AWS x Datadog GenAI Hackathon - Oratio Platform"
echo "=================================================="
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo ""
    echo "📝 Please edit backend/.env with your API keys:"
    echo "   - DD_API_KEY (Datadog)"
    echo "   - MINIMAX_API_KEY (MiniMax Voice)"
    echo "   - GOOGLE_API_KEY (Gemini Backup)"
    echo "   - AWS credentials"
    echo ""
    echo "Then run this script again."
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
cd backend

if ! python -c "import fastapi" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing..."
    pip install -e .
    echo "✅ Dependencies installed"
else
    echo "✅ Dependencies already installed"
fi

echo ""
echo "🧪 Running setup verification..."
python test_hackathon_setup.py

echo ""
echo "🚀 Starting Oratio Backend with Datadog..."
echo ""
echo "📊 View traces at: https://app.datadoghq.com/apm/traces"
echo "🎤 Voice endpoint: ws://localhost:8000/api/v1/voice/ws/{agent_id}/{session_id}"
echo "💬 Chat endpoint: POST http://localhost:8000/api/v1/chat/{agent_id}/{session_id}"
echo "❤️  Health check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start with Datadog tracing
ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
