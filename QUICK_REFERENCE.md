# 🚀 Oratio - Quick Reference Card

## 🏃 Quick Start

```bash
# 1. Setup environment
cp backend/.env.example backend/.env
# Edit .env with your API keys

# 2. Install dependencies
cd backend && pip install -e .

# 3. Test setup
python test_hackathon_setup.py

# 4. Start server
./start_hackathon.sh
```

## 🔑 Required API Keys

```bash
# Datadog
DD_API_KEY=your_key_here
DD_APP_KEY=your_key_here

# MiniMax (apply at https://forms.gle/Fazk8r87QmudNLNd6)
MINIMAX_API_KEY=your_key_here
MINIMAX_GROUP_ID=your_group_here

# Gemini
GOOGLE_API_KEY=your_key_here

# AWS
AWS_ACCESS_KEY_ID=your_key_here
AWS_SECRET_ACCESS_KEY=your_secret_here
```

## 📡 Key Endpoints

```bash
# Health check
curl http://localhost:8000/health

# Create agent
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Agent", "sop": "Be helpful"}'

# Chat with agent
curl -X POST http://localhost:8000/api/v1/chat/{agent_id}/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'

# Voice WebSocket
wscat -c ws://localhost:8000/api/v1/voice/ws/{agent_id}/{session_id}
```

## 📊 Datadog Links

```bash
# APM Traces
https://app.datadoghq.com/apm/traces?query=service:oratio-backend

# LLM Observability
https://app.datadoghq.com/llm/

# Metrics Explorer
https://app.datadoghq.com/metric/explorer

# Dashboard
https://app.datadoghq.com/dashboard/lists
```

## 🎯 Demo Flow (5 minutes)

1. **Intro** (30s): "Oratio - AI agents in seconds with full observability"
2. **Architecture** (30s): Show diagram, explain Chameleon
3. **Create Agent** (1m): Live API call, show Datadog traces
4. **Voice Demo** (1m): WebSocket interaction, show metrics
5. **Failover** (30s): Simulate failure, show auto-recovery
6. **Dashboard** (30s): Show Datadog metrics
7. **Close** (30s): Recap value proposition

## 🐛 Quick Troubleshooting

```bash
# Backend won't start
pip install -e . --force-reinstall
lsof -i :8000  # Check port conflicts

# Datadog not working
echo $DD_API_KEY  # Verify set
DD_TRACE_DEBUG=true ddtrace-run uvicorn main:app

# MiniMax not working
curl http://localhost:8000/health | jq .voice_providers
# Should show gemini as backup

# Reset everything
pkill -f uvicorn
rm -rf __pycache__
./start_hackathon.sh
```

## 💡 Key Talking Points

- **AWS**: "Built entirely on Bedrock - AgentCore, Nova, Claude"
- **Datadog**: "Full observability - APM, LLM tracking, custom metrics"
- **Innovation**: "Chameleon architecture - one runtime for unlimited agents"
- **Speed**: "Sub-second deployment vs weeks traditionally"
- **Reliability**: "Multi-provider with automatic failover"
- **Production**: "Multi-tenant, secure, scalable, monitored"

## 📈 Key Metrics to Show

- API latency: p50, p95, p99
- Agent creation time: 8-12 seconds
- Voice latency: 1.5-2.5 seconds
- Token usage per request
- Provider failover events
- Success/error rates

## 🏆 Prize Requirements

- ✅ AWS Infrastructure (Bedrock)
- ✅ Datadog Observability
- ✅ Live Working Demo

## 📞 Emergency Commands

```bash
# Kill everything
pkill -f uvicorn
pkill -f python

# Check what's running
ps aux | grep uvicorn
lsof -i :8000

# View logs
tail -f logs/oratio.log

# Test without Datadog
uvicorn main:app --host 0.0.0.0 --port 8000

# Test with Datadog
ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000
```

## 🎤 Judge Q&A Prep

**Q: How is this different?**
A: "One runtime for all agents vs separate deployments. Sub-second creation vs weeks."

**Q: What if providers fail?**
A: "Automatic failover to backup. Graceful degradation to text-only."

**Q: Production ready?**
A: "Yes - multi-tenant, secure, monitored, error handling, failover."

**Q: Datadog value?**
A: "Complete visibility into AI costs, performance, and reliability."

## 📱 Contacts

- Hackathon Discord: [Link from email]
- AWS Support: At venue
- Datadog Support: At venue

## ⏰ Timeline

- 9:00 AM: Check-in
- 9:30 AM: Talks
- 11:00 AM: Hacking starts
- 12:00 PM: Lunch
- 5:00 PM: Submission deadline
- 5:00 PM: Judging starts
- 7:00 PM: Presentations
- 7:45 PM: Awards

---

**Keep this handy during the hackathon!**
