# Quick Environment Setup Guide

## 🚀 Fastest Way to Get Started

### Option 1: Interactive Setup (Recommended)

```bash
python3 scripts/setup_env.py
```

This will guide you through all required configuration step-by-step.

---

## Option 2: Manual Setup

### Step 1: Get AWS Account ID

```bash
aws sts get-caller-identity --query Account --output text
```

### Step 2: Generate JWT Secret

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Get API Keys

You need these API keys:

1. **Datadog** (REQUIRED)
   - Go to: https://app.datadoghq.com/organization-settings/api-keys
   - Create API Key and Application Key

2. **MiniMax** (REQUIRED)
   - Apply for free credits: https://forms.gle/Fazk8r87QmudNLNd6
   - Get API Key and Group ID

3. **Google Gemini** (REQUIRED)
   - Go to: https://aistudio.google.com/app/apikey
   - Create API Key

### Step 4: Create .env File

```bash
cd backend
cp .env.example .env
# Edit .env with your values
```

### Step 5: Enable Bedrock Models

1. Go to AWS Console → Bedrock → Model access
2. Enable:
   - Claude 3.5 Sonnet
   - Claude 3 Haiku
   - Titan Embeddings
   - Nova Sonic (if available)

---

## 🧪 Test Your Setup

```bash
cd backend
python test_hackathon_setup.py
```

---

## 📝 Minimum Required Variables

```bash
# AWS (REQUIRED)
AWS_ACCOUNT_ID=your-account-id
AWS_REGION=us-east-1
BEDROCK_REGION=us-east-1

# JWT (REQUIRED)
JWT_SECRET_KEY=your-generated-secret

# Datadog (REQUIRED)
DD_API_KEY=your-datadog-api-key
DD_APP_KEY=your-datadog-app-key

# Voice Providers (REQUIRED)
MINIMAX_API_KEY=your-minimax-key
MINIMAX_GROUP_ID=your-group-id
GOOGLE_API_KEY=your-google-key
```

Everything else can use default values!

---

## 🆘 Quick Troubleshooting

### "AWS credentials not found"
```bash
aws configure
```

### "Bedrock access denied"
- Enable models in AWS Console → Bedrock → Model access

### "Module not found"
```bash
cd backend
pip install -r requirements.txt
```

---

## 📚 Full Documentation

- Detailed setup: `AWS_SETUP_GUIDE.md`
- Hackathon plan: `HACKATHON_PLAN.md`
- Quick reference: `QUICK_REFERENCE.md`
