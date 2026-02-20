# AWS x Datadog GenAI Hackathon - Oratio Adaptation Plan

## 🎯 Hackathon Requirements

### Core Requirements (Must Have)
- ✅ AWS Infrastructure (Amazon Bedrock) - Already implemented
- 🔄 Datadog Observability - **TO IMPLEMENT**
- 🔄 Live, working demo - **TO VERIFY**

### Our Additions
- 🔄 MiniMax Voice Model (primary)
- 🔄 Gemini Model (backup)
- ⏰ CopilotKit.ai (time permitting)
- ⏰ TestSprite (time permitting)

---

## 📋 Implementation Checklist

### Phase 1: Core Functionality Verification (Priority 1)
- [ ] Verify backend API is running
- [ ] Verify agent creation pipeline works
- [ ] Verify chat endpoint works
- [ ] Test Chameleon loader
- [ ] Document current working state

### Phase 2: Datadog Observability Integration (Priority 1 - REQUIRED)
- [ ] Install Datadog Python SDK (`ddtrace`)
- [ ] Configure Datadog APM for FastAPI backend
- [ ] Add custom metrics for agent operations
- [ ] Implement LLM Observability for Bedrock calls
- [ ] Create Datadog dashboard for demo
- [ ] Add distributed tracing across services
- [ ] Monitor agent creation pipeline
- [ ] Track voice/text session metrics

### Phase 3: MiniMax Voice Integration (Priority 1 - REQUIRED)
- [ ] Research MiniMax API documentation
- [ ] Apply for MiniMax free credits (https://forms.gle/Fazk8r87QmudNLNd6)
- [ ] Install MiniMax Python SDK
- [ ] Create MiniMax voice service wrapper
- [ ] Implement WebSocket handler for MiniMax
- [ ] Add audio streaming support
- [ ] Test voice quality and latency

### Phase 4: Gemini Backup Integration (Priority 2)
- [ ] Install Google Generative AI SDK
- [ ] Create Gemini service wrapper
- [ ] Implement fallback logic (MiniMax → Gemini)
- [ ] Add health checks for both services
- [ ] Test failover mechanism

### Phase 5: Enhanced Demo Features (Priority 3)
- [ ] Create demo agent with sample SOP
- [ ] Prepare demo script
- [ ] Create Datadog dashboard screenshots
- [ ] Document architecture changes
- [ ] Prepare presentation materials

### Phase 6: Optional Integrations (Time Permitting)
- [ ] CopilotKit.ai integration for UI
- [ ] TestSprite for testing automation

---

## 🏗️ Architecture Changes

### Current Architecture
```
Frontend (Next.js) → Backend (FastAPI) → AWS Bedrock (Nova Sonic)
                                       → AgentCore (Chameleon)
```

### New Hackathon Architecture
```
Frontend (Next.js) → Backend (FastAPI) → MiniMax Voice (Primary)
                                       → Gemini Voice (Backup)
                                       → AWS Bedrock (Text/Agent Logic)
                                       → AgentCore (Chameleon)
                                       ↓
                                    Datadog APM
                                    (Observability Layer)
```

---

## 📦 New Dependencies

### Backend (Python)
```toml
# Datadog
ddtrace = "^2.0.0"
datadog-api-client = "^2.0.0"

# MiniMax
minimax-sdk = "^1.0.0"  # TBD - check actual package name

# Gemini
google-generativeai = "^0.3.0"

# Additional
websockets = "^12.0"
```

### Environment Variables
```bash
# Datadog
DD_API_KEY=<datadog-api-key>
DD_APP_KEY=<datadog-app-key>
DD_SERVICE=oratio-backend
DD_ENV=hackathon
DD_VERSION=1.0.0
DD_TRACE_ENABLED=true

# MiniMax
MINIMAX_API_KEY=<minimax-api-key>
MINIMAX_GROUP_ID=<minimax-group-id>

# Gemini
GOOGLE_API_KEY=<gemini-api-key>
```

---

## 🎯 Demo Flow

### 1. Agent Creation (Show Datadog Traces)
- User uploads SOP document
- Backend triggers agent creation
- Datadog shows: API latency, S3 upload time, Bedrock invocation
- AgentCreator generates code
- Datadog shows: LLM token usage, generation time, success rate

### 2. Voice Interaction (Show MiniMax + Datadog)
- Customer calls agent via WebSocket
- MiniMax processes voice input
- Datadog shows: Audio latency, transcription accuracy, response time
- Agent responds with business logic
- Datadog shows: Agent execution time, tool usage, memory access

### 3. Failover Demo (Show Gemini Backup)
- Simulate MiniMax failure
- System automatically fails over to Gemini
- Datadog shows: Error detection, failover time, recovery

### 4. Dashboard View
- Real-time metrics on Datadog dashboard
- Agent performance analytics
- Cost tracking (token usage)
- Error rates and alerts

---

## 🚀 Quick Start Commands

### 1. Install Dependencies
```bash
cd backend
pip install ddtrace datadog-api-client google-generativeai websockets
```

### 2. Set Environment Variables
```bash
export DD_API_KEY=<your-key>
export DD_SERVICE=oratio-backend
export DD_ENV=hackathon
export MINIMAX_API_KEY=<your-key>
export GOOGLE_API_KEY=<your-key>
```

### 3. Run with Datadog
```bash
ddtrace-run uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Test Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Create agent
curl -X POST http://localhost:8000/api/v1/agents \
  -H "Authorization: Bearer <token>" \
  -d '{"name": "Demo Agent", "sop": "..."}'

# Voice WebSocket
wscat -c ws://localhost:8000/api/v1/voice/ws/<agent_id>/<session_id>
```

---

## 📊 Datadog Dashboard Metrics

### Key Metrics to Track
1. **API Performance**
   - Request latency (p50, p95, p99)
   - Throughput (requests/sec)
   - Error rate

2. **LLM Operations**
   - Token usage per request
   - Model latency
   - Cost per interaction
   - Success/failure rate

3. **Voice Operations**
   - Audio processing time
   - Transcription accuracy
   - End-to-end latency
   - MiniMax vs Gemini usage ratio

4. **Agent Operations**
   - Agent creation time
   - Code generation success rate
   - Memory access latency
   - Tool execution time

5. **Business Metrics**
   - Active agents count
   - Total sessions
   - Average session duration
   - Customer satisfaction (if available)

---

## 🎤 Presentation Talking Points

1. **Problem**: Traditional AI agent deployment is slow and expensive
2. **Solution**: Oratio's Chameleon architecture - one runtime for unlimited agents
3. **Innovation**: Meta-agent generates custom code automatically
4. **Observability**: Full Datadog integration for production monitoring
5. **Voice**: MiniMax for high-quality voice with Gemini failover
6. **AWS**: Built entirely on AWS Bedrock infrastructure
7. **Demo**: Live agent creation and voice interaction with real-time metrics

---

## ⏱️ Time Allocation (6 hours total)

- **Hour 1**: Verify current functionality, set up Datadog (Priority 1)
- **Hour 2**: Implement Datadog APM and custom metrics (Priority 1)
- **Hour 3**: Integrate MiniMax voice service (Priority 1)
- **Hour 4**: Add Gemini backup and failover logic (Priority 2)
- **Hour 5**: Create demo agent, test end-to-end, create dashboard (Priority 1)
- **Hour 6**: Prepare presentation, screenshots, and final testing (Priority 1)

---

## 🏆 Prize Eligibility Checklist

- [x] Uses AWS infrastructure (Bedrock) ✅
- [ ] Integrates Datadog observability ⏳
- [ ] Delivers live, working demo ⏳
- [ ] Production-ready system ✅ (mostly)
- [ ] Clear value proposition ✅

---

## 📝 Notes

- MiniMax credits: Apply ASAP at https://forms.gle/Fazk8r87QmudNLNd6
- Datadog trial: Sign up for free trial if needed
- Keep it simple: Focus on core demo flow
- Document everything: Screenshots, metrics, architecture diagrams
- Practice demo: Run through at least twice before judging

---

## 🔗 Resources

- MiniMax Docs: [TBD - add after research]
- Datadog Python APM: https://docs.datadoghq.com/tracing/setup_overview/setup/python/
- Datadog LLM Observability: https://docs.datadoghq.com/llm_observability/
- Gemini API: https://ai.google.dev/docs
- AWS Bedrock: https://docs.aws.amazon.com/bedrock/

---

**Last Updated**: Pre-hackathon preparation
**Status**: Ready to implement
**Estimated Completion**: 6 hours
