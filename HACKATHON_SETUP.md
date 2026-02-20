# 🏆 AWS x Datadog GenAI Hackathon - Oratio Setup Guide

## 🎯 Quick Start (5 Minutes)

### Prerequisites
- Python 3.11+
- Node.js 20+
- AWS Account with Bedrock access
- Datadog Account (free trial available)
- MiniMax API Key (apply at https://forms.gle/Fazk8r87QmudNLNd6)
- Google API Key for Gemini

### 1. Clone and Setup

```bash
# Clone repository
git clone <your-repo>
cd oratio

# Backend setup
cd backend
cp .env.example .env
# Edit .env with your API keys (see below)

# Install dependencies
pip install -e .

# Frontend setup (optional for demo)
cd ../frontend
npm install
```

### 2. Configure Environment Variables

Edit `backend/.env`:

```bash
# ========================================
# REQUIRED FOR HACKATHON
# ========================================

# Datadog (REQUIRED)
DD_API_KEY=your_datadog_api_key_here
DD_APP_KEY=your_datadog_app_key_here
DD_SERVICE=oratio-backend
DD_ENV=hackathon
DD_TRACE_ENABLED=true
DD_LLM_OBS_ENABLED=true

# MiniMax Voice (PRIMARY - REQUIRED)
MINIMAX_API_KEY=your_minimax_api_key_here
MINIMAX_GROUP_ID=your_minimax_group_id_here

# Google Gemini (BACKUP - REQUIRED)
GOOGLE_API_KEY=your_google_api_key_here

# AWS Bedrock (REQUIRED)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
BEDROCK_REGION=us-east-1
```

### 3. Run with Datadog Tracing

```bash
cd backend

# Option 1: Run with ddtrace (recommended)
ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000

# Option 2: Run normally (Datadog still works via imports)
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Verify Setup

```bash
# Check health endpoint
curl http://localhost:8000/health

# Expected response:
{
  "status": "healthy",
  "service": "oratio-backend",
  "environment": "hackathon",
  "voice_providers": {
    "current": "minimax",
    "minimax": {
      "available": true,
      "configured": true
    },
    "gemini": {
      "available": true,
      "configured": true
    }
  }
}
```

---

## 📊 Datadog Setup

### 1. Get API Keys

1. Sign up at https://www.datadoghq.com/ (free trial)
2. Go to Organization Settings → API Keys
3. Create new API Key → Copy to `DD_API_KEY`
4. Go to Organization Settings → Application Keys
5. Create new Application Key → Copy to `DD_APP_KEY`

### 2. Install Datadog Agent (Optional but Recommended)

```bash
# macOS
brew install datadog-agent

# Start agent
datadog-agent run

# Verify
datadog-agent status
```

### 3. View Traces

1. Go to https://app.datadoghq.com/apm/traces
2. Filter by service: `oratio-backend`
3. Filter by env: `hackathon`

### 4. View LLM Observability

1. Go to https://app.datadoghq.com/llm/
2. See token usage, latency, costs
3. View model performance metrics

---

## 🎤 MiniMax Voice Setup

### 1. Apply for Credits

1. Fill out form: https://forms.gle/Fazk8r87QmudNLNd6
2. Wait for approval (usually quick during hackathon)
3. Receive API key and Group ID via email

### 2. Test MiniMax

```bash
# Test endpoint
curl -X POST http://localhost:8000/api/v1/voice/test-minimax \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test"}'
```

### 3. WebSocket Connection

```javascript
// JavaScript client example
const ws = new WebSocket('ws://localhost:8000/api/v1/voice/ws/agent_id/session_id');

ws.onopen = () => {
  console.log('Connected to voice service');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

// Send audio
ws.send(JSON.stringify({
  type: 'audio',
  data: base64AudioData
}));
```

---

## 🤖 Google Gemini Setup

### 1. Get API Key

1. Go to https://makersuite.google.com/app/apikey
2. Create API Key
3. Copy to `GOOGLE_API_KEY`

### 2. Test Gemini

```bash
# Test endpoint
curl -X POST http://localhost:8000/api/v1/voice/test-gemini \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test"}'
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Oratio Platform                          │
│                  (Hackathon Version)                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI Backend                            │
│                 (with Datadog APM)                           │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   MiniMax    │   │    Gemini    │   │ AWS Bedrock  │
│   (Primary)  │   │   (Backup)   │   │  (Agents)    │
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │   Datadog    │
                    │ Observability│
                    └──────────────┘
```

---

## 🎯 Demo Flow

### 1. Create Agent

```bash
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "name": "Customer Service Agent",
    "description": "Handles customer inquiries",
    "sop": "Always be polite and helpful. Answer questions about products."
  }'
```

**Datadog Shows:**
- API request latency
- Agent creation time
- Bedrock invocation metrics

### 2. Voice Interaction

```bash
# Connect via WebSocket
wscat -c ws://localhost:8000/api/v1/voice/ws/<agent_id>/<session_id>

# Send audio (base64 encoded)
{"type": "audio", "data": "<base64_audio>"}
```

**Datadog Shows:**
- Voice session duration
- MiniMax API latency
- Transcription accuracy
- Agent response time

### 3. Failover Demo

```bash
# Simulate MiniMax failure (set invalid API key)
export MINIMAX_API_KEY=invalid

# Restart server
ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000

# Try voice interaction - should automatically use Gemini
```

**Datadog Shows:**
- Failover event
- Provider switch (minimax → gemini)
- Error recovery time

---

## 📈 Key Metrics to Show Judges

### 1. API Performance
- Request latency (p50, p95, p99)
- Throughput (requests/sec)
- Error rate

### 2. LLM Operations
- Token usage per request
- Model latency
- Cost per interaction
- Success rate

### 3. Voice Operations
- Audio processing time
- Transcription accuracy
- End-to-end latency
- Provider usage ratio (MiniMax vs Gemini)

### 4. Agent Operations
- Agent creation time
- Code generation success rate
- Memory access latency

---

## 🐛 Troubleshooting

### Datadog Not Showing Traces

```bash
# Check if ddtrace is installed
pip list | grep ddtrace

# Verify environment variables
echo $DD_API_KEY
echo $DD_SERVICE

# Check Datadog agent status (if installed)
datadog-agent status

# Run with debug logging
DD_TRACE_DEBUG=true ddtrace-run uvicorn main:app
```

### MiniMax Connection Issues

```bash
# Verify API key
curl -H "Authorization: Bearer $MINIMAX_API_KEY" \
  https://api.minimax.chat/v1/voice/health

# Check logs
tail -f logs/oratio.log | grep minimax
```

### Gemini Not Working

```bash
# Test API key
curl -H "x-goog-api-key: $GOOGLE_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models

# Check Python package
python -c "import google.generativeai as genai; print(genai.__version__)"
```

---

## 📝 Presentation Tips

### 1. Start with Problem
"Traditional AI agent deployment takes weeks and requires separate infrastructure for each agent"

### 2. Show Innovation
"Oratio's Chameleon architecture: one runtime for unlimited agents"

### 3. Demo Live
- Create agent in real-time
- Show Datadog dashboard
- Voice interaction with metrics
- Failover demonstration

### 4. Highlight AWS + Datadog
- "Built entirely on AWS Bedrock"
- "Full observability with Datadog"
- "Production-ready monitoring"

### 5. Show Business Value
- "Sub-second agent creation"
- "Cost-effective scaling"
- "Enterprise-grade observability"

---

## 🏆 Prize Eligibility Checklist

- [x] Uses AWS infrastructure (Bedrock) ✅
- [x] Integrates Datadog observability ✅
- [x] Delivers live, working demo ✅
- [x] Production-ready system ✅
- [x] Clear value proposition ✅

---

## 📞 Support

- **Discord**: Join hackathon Discord for real-time help
- **Documentation**: See `/docs` folder for detailed guides
- **Issues**: Check `HACKATHON_PLAN.md` for known issues

---

## 🚀 Quick Commands Reference

```bash
# Start backend with Datadog
cd backend && ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000

# Start frontend
cd frontend && npm run dev

# Check health
curl http://localhost:8000/health

# View Datadog traces
open https://app.datadoghq.com/apm/traces?query=service:oratio-backend

# Test voice WebSocket
wscat -c ws://localhost:8000/api/v1/voice/ws/test_agent/test_session
```

---

**Good luck at the hackathon! 🎉**
