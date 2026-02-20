# 🏆 AWS x Datadog GenAI Hackathon - Pre-Event Checklist

## ⏰ Before the Hackathon (Do Now!)

### 1. Get API Keys (CRITICAL - Do This First!)

- [ ] **MiniMax Credits**
  - Apply at: https://forms.gle/Fazk8r87QmudNLNd6
  - Wait for approval email
  - Save API key and Group ID
  - ⏱️ Time: Can take a few hours, apply ASAP!

- [ ] **Datadog Account**
  - Sign up at: https://www.datadoghq.com/
  - Get API Key: Organization Settings → API Keys
  - Get App Key: Organization Settings → Application Keys
  - ⏱️ Time: 5 minutes

- [ ] **Google Gemini**
  - Get key at: https://makersuite.google.com/app/apikey
  - ⏱️ Time: 2 minutes

- [ ] **AWS Credentials**
  - Ensure Bedrock access is enabled
  - Have access key and secret ready
  - ⏱️ Time: Varies

### 2. Setup Development Environment

- [ ] **Install Dependencies**
  ```bash
  # Python 3.11+
  python --version
  
  # Install backend dependencies
  cd backend
  pip install -e .
  
  # Install Datadog CLI (optional)
  pip install ddtrace datadog-api-client
  ```

- [ ] **Configure Environment**
  ```bash
  # Copy template
  cp backend/.env.example backend/.env
  
  # Edit with your keys
  nano backend/.env
  ```

- [ ] **Test Setup**
  ```bash
  cd backend
  python test_hackathon_setup.py
  ```

### 3. Verify Everything Works

- [ ] **Start Backend**
  ```bash
  ./start_hackathon.sh
  ```

- [ ] **Check Health**
  ```bash
  curl http://localhost:8000/health
  ```

- [ ] **Verify Datadog**
  - Go to https://app.datadoghq.com/apm/traces
  - Filter by service: `oratio-backend`
  - Should see traces appearing

- [ ] **Test Voice Providers**
  ```bash
  # Should show both providers available
  curl http://localhost:8000/health | jq .voice_providers
  ```

---

## 📅 Day of Hackathon

### Morning (9:00 AM - 11:00 AM)

- [ ] **Arrive Early**
  - Check-in at 9:00 AM
  - Get breakfast ☕
  - Set up laptop and workspace

- [ ] **Attend Talks (9:30 - 11:00 AM)**
  - AWS Bedrock overview
  - Datadog observability
  - Partner presentations
  - Take notes on useful features

- [ ] **Network**
  - Meet other participants
  - Find potential team members (if needed)
  - Exchange contact info

### Hacking Phase (11:00 AM - 5:00 PM)

#### Hour 1 (11:00 AM - 12:00 PM): Setup & Verification
- [ ] Connect to venue WiFi
- [ ] Test internet connection
- [ ] Verify all services are running
- [ ] Check Datadog is receiving traces
- [ ] Test MiniMax connection
- [ ] Test Gemini backup

#### Hour 2 (12:00 PM - 1:00 PM): Core Demo Prep
- [ ] Create demo agent with sample SOP
- [ ] Test agent creation flow
- [ ] Verify Datadog metrics appear
- [ ] Test voice interaction
- [ ] Document any issues

**🍽️ Lunch Break (12:00 PM - provided by MongoDB)**

#### Hour 3 (1:00 PM - 2:00 PM): Datadog Dashboard
- [ ] Create custom Datadog dashboard
- [ ] Add key metrics widgets
- [ ] Configure alerts
- [ ] Take screenshots for presentation
- [ ] Test dashboard updates in real-time

#### Hour 4 (2:00 PM - 3:00 PM): Demo Polish
- [ ] Prepare demo script
- [ ] Practice demo flow
- [ ] Test failover scenario
- [ ] Record backup demo video (just in case)
- [ ] Prepare talking points

#### Hour 5 (3:00 PM - 4:00 PM): Presentation Prep
- [ ] Create presentation slides (if needed)
- [ ] Prepare architecture diagrams
- [ ] Screenshot Datadog dashboard
- [ ] Write 2-minute pitch
- [ ] Practice presentation

#### Hour 6 (4:00 PM - 5:00 PM): Final Testing
- [ ] Run through complete demo
- [ ] Test all endpoints
- [ ] Verify Datadog is logging everything
- [ ] Check for any errors
- [ ] Prepare for submission

### Judging Phase (5:00 PM - 8:00 PM)

#### Submission (5:00 PM Deadline)
- [ ] Submit project before deadline
- [ ] Ensure all code is committed
- [ ] Verify demo is working
- [ ] Have backup plan ready

#### Science Fair Judging (5:00 PM - 7:00 PM)
- [ ] Set up demo station
- [ ] Have laptop ready with demo running
- [ ] Datadog dashboard open in browser
- [ ] Prepare for judge questions
- [ ] Be ready to show live demo

#### Presentations (7:00 PM - 7:30 PM)
- [ ] If selected, present to full audience
- [ ] Show live demo
- [ ] Highlight Datadog integration
- [ ] Demonstrate failover
- [ ] Answer questions confidently

#### Awards (7:45 PM - 8:00 PM)
- [ ] Attend award ceremony
- [ ] Network with judges and sponsors
- [ ] Celebrate! 🎉

---

## 🎯 Demo Script (Practice This!)

### 1. Introduction (30 seconds)
"Hi, I'm [name] and this is Oratio - an AI agent platform that automatically generates and deploys conversational agents with full observability. Traditional agent deployment takes weeks; we do it in seconds."

### 2. Architecture Overview (30 seconds)
"We're built entirely on AWS Bedrock with Datadog observability. Our innovation is the Chameleon architecture - one runtime for unlimited agents, with automatic code generation from SOPs."

### 3. Live Demo - Agent Creation (1 minute)
```bash
# Show Datadog dashboard
# Create agent via API
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{"name": "Demo Agent", "sop": "..."}'

# Show Datadog traces
# Point out: API latency, Bedrock calls, agent creation time
```

### 4. Live Demo - Voice Interaction (1 minute)
```bash
# Connect to voice WebSocket
# Speak to agent
# Show real-time Datadog metrics
# Point out: MiniMax latency, transcription, response time
```

### 5. Live Demo - Failover (30 seconds)
```bash
# Simulate MiniMax failure
# Show automatic failover to Gemini
# Point out: Datadog failover metric, recovery time
```

### 6. Datadog Dashboard (30 seconds)
"Here's our Datadog dashboard showing:
- API performance metrics
- LLM token usage and costs
- Voice session analytics
- Provider health and failover events"

### 7. Closing (30 seconds)
"Oratio meets all hackathon requirements: AWS Bedrock infrastructure, full Datadog observability, and a live working demo. We're production-ready with multi-provider redundancy and complete visibility. Thank you!"

**Total Time: 4-5 minutes**

---

## 🎤 Talking Points for Judges

### Technical Excellence
- "Built entirely on AWS Bedrock - AgentCore, Nova, Claude"
- "Full Datadog integration - APM, LLM Observability, custom metrics"
- "Multi-provider voice with automatic failover"
- "Production-ready with security, multi-tenancy, error handling"

### Innovation
- "Chameleon architecture - one runtime for unlimited agents"
- "Meta-agent pipeline - automatic code generation from SOPs"
- "Sub-second agent deployment vs weeks traditionally"
- "Real-time observability for all AI operations"

### Business Value
- "100x faster agent deployment"
- "10x cost reduction through shared infrastructure"
- "99.9% uptime with automatic failover"
- "Complete visibility into AI costs and performance"

### Demo Quality
- "Live working system, not just slides"
- "Real-time Datadog metrics during demo"
- "Actual failover demonstration"
- "Production-ready code on GitHub"

---

## ❓ Anticipated Judge Questions

### Q: "How does this compare to existing solutions?"
**A**: "Traditional platforms require separate deployments per agent, taking weeks. Our Chameleon architecture uses one runtime for all agents, enabling sub-second deployment. Plus, we have full Datadog observability built-in."

### Q: "What happens if both voice providers fail?"
**A**: "We gracefully degrade to text-only mode. The agent logic still works via Bedrock, and we alert via Datadog. In production, we'd add more providers."

### Q: "How do you handle agent memory across sessions?"
**A**: "We use AWS AgentCore's memory API, which provides persistent conversation history. Each agent has isolated memory, and we inject the last 10 turns on initialization."

### Q: "What's the cost per agent?"
**A**: "Agent creation costs ~$0.05 in Bedrock tokens. Runtime costs are pay-per-use: ~$0.01 per conversation. The Chameleon architecture means no fixed infrastructure costs per agent."

### Q: "Is this production-ready?"
**A**: "Yes. We have multi-tenant isolation, API key authentication, error handling, automatic failover, and full observability. We're using AWS best practices throughout."

### Q: "How does Datadog help?"
**A**: "Datadog gives us complete visibility: API latency, LLM token usage and costs, voice session analytics, and failover events. This is critical for production AI systems where costs and performance vary."

---

## 🚨 Troubleshooting (Day-Of)

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -e . --force-reinstall

# Check for port conflicts
lsof -i :8000
```

### Datadog Not Showing Traces
```bash
# Verify environment variables
echo $DD_API_KEY
echo $DD_SERVICE

# Check if ddtrace is installed
pip list | grep ddtrace

# Run with debug logging
DD_TRACE_DEBUG=true ddtrace-run uvicorn main:app
```

### MiniMax Connection Failed
```bash
# Verify API key
echo $MINIMAX_API_KEY

# Check if Gemini backup works
curl http://localhost:8000/health | jq .voice_providers.gemini

# Use Gemini as primary if needed
# (System will auto-failover)
```

### WiFi Issues
- Have mobile hotspot ready as backup
- Pre-download any needed resources
- Have offline demo video ready

---

## 📦 What to Bring

### Required
- [ ] Laptop (fully charged)
- [ ] Laptop charger
- [ ] Phone (for hotspot backup)
- [ ] Phone charger
- [ ] Government ID (for check-in)

### Recommended
- [ ] External monitor (if available)
- [ ] Mouse
- [ ] Headphones (for testing voice)
- [ ] Notebook and pen
- [ ] Business cards
- [ ] Water bottle

### Nice to Have
- [ ] Backup laptop
- [ ] USB drive with code backup
- [ ] Printed architecture diagrams
- [ ] Snacks

---

## 🎯 Success Criteria

### Minimum (Must Have)
- [ ] Backend running with Datadog
- [ ] Health endpoint working
- [ ] At least one voice provider working
- [ ] Datadog showing traces
- [ ] Can demonstrate live

### Target (Should Have)
- [ ] Both voice providers working
- [ ] Failover demonstration
- [ ] Custom Datadog dashboard
- [ ] Agent creation demo
- [ ] Voice interaction demo

### Stretch (Nice to Have)
- [ ] Frontend running
- [ ] Multiple demo agents
- [ ] Recorded demo video
- [ ] Presentation slides
- [ ] Architecture diagrams

---

## 🏆 Prize Eligibility Final Check

Before submission at 5:00 PM:

- [ ] ✅ Uses AWS infrastructure (Bedrock)
- [ ] ✅ Integrates Datadog observability
- [ ] ✅ Delivers live, working demo
- [ ] ✅ Code on GitHub
- [ ] ✅ Documentation complete

---

## 📞 Emergency Contacts

- **Hackathon Discord**: [Join link from email]
- **AWS Support**: Available at venue
- **Datadog Support**: Available at venue
- **Organizers**: Check Discord for contact info

---

## 💪 Final Reminders

1. **Stay Calm**: You've prepared well
2. **Test Early**: Verify everything works at venue
3. **Practice Demo**: Run through it multiple times
4. **Have Backup**: Video, screenshots, offline mode
5. **Network**: Talk to judges and sponsors
6. **Have Fun**: Enjoy the experience!

---

**You've got this! Good luck! 🚀**
