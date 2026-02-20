# AWS Setup Guide for Oratio Platform

This guide helps you set up the AWS infrastructure needed for the Oratio platform. We'll use a **simplified approach** suitable for hackathons and development.

## 🎯 Quick Setup Strategy

For hackathon/development, we'll use:
- ✅ **AWS Bedrock** - Required for AI/LLM features
- ✅ **Local/Mock Auth** - Skip Cognito, use JWT only
- ✅ **Local Storage** - Skip DynamoDB/S3 initially, use in-memory or local files
- ⚠️ **Optional**: DynamoDB Local for testing
- ⚠️ **Optional**: LocalStack for S3 simulation

## 📋 Prerequisites

1. **AWS Account** - Free tier is sufficient
2. **AWS CLI** installed and configured
3. **Python 3.11+** installed
4. **Node.js 20+** installed (for frontend)

---

## Step 1: AWS Account Setup

### 1.1 Get Your AWS Account ID

```bash
# Install AWS CLI if not already installed
# macOS:
brew install awscli

# Configure AWS CLI
aws configure

# Get your account ID
aws sts get-caller-identity --query Account --output text
```

Copy the account ID and add to `.env`:
```bash
AWS_ACCOUNT_ID=123456789012  # Your actual account ID
```

### 1.2 Set Your Region

```bash
AWS_REGION=us-east-1  # Or your preferred region
BEDROCK_REGION=us-east-1
COGNITO_REGION=us-east-1
```

---

## Step 2: AWS Bedrock Setup (REQUIRED)

Bedrock is essential for AI features. You need to enable model access.

### 2.1 Enable Bedrock Models

1. Go to AWS Console → Bedrock → Model access
2. Click "Manage model access"
3. Enable these models:
   - ✅ **Claude 3.5 Sonnet** (for text generation)
   - ✅ **Claude 3 Haiku** (for fast responses)
   - ✅ **Titan Embeddings G1** (for knowledge bases)
   - ✅ **Nova Sonic** (for voice - if available in your region)

4. Wait for approval (usually instant for most models)

### 2.2 Test Bedrock Access

```bash
# Test Claude access
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
  --body '{"anthropic_version":"bedrock-2023-05-31","messages":[{"role":"user","content":"Hello"}],"max_tokens":100}' \
  --region us-east-1 \
  output.json

cat output.json
```

If successful, you're ready to use Bedrock!

---

## Step 3: Authentication Setup (SIMPLIFIED)

For hackathon, **skip Cognito** and use JWT-only authentication.

### 3.1 Generate JWT Secret

```bash
# Generate a secure random secret
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add to `.env`:
```bash
JWT_SECRET_KEY=your-generated-secret-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Leave Cognito empty for now
COGNITO_USER_POOL_ID=
COGNITO_CLIENT_ID=
```

### 3.2 (Optional) Set Up Cognito Later

If you want real user management:

```bash
# Create user pool
aws cognito-idp create-user-pool \
  --pool-name oratio-users \
  --auto-verified-attributes email \
  --region us-east-1

# Create app client
aws cognito-idp create-user-pool-client \
  --user-pool-id <pool-id-from-above> \
  --client-name oratio-web \
  --no-generate-secret \
  --region us-east-1
```

---

## Step 4: Database Setup (SIMPLIFIED OPTIONS)

### Option A: In-Memory (Fastest for Development)

No setup needed! The application can use in-memory storage for development.

Add to `.env`:
```bash
# Use default table names (won't be created yet)
USERS_TABLE=oratio-users
AGENTS_TABLE=oratio-agents
SESSIONS_TABLE=oratio-sessions
API_KEYS_TABLE=oratio-api-keys
NOTIFICATIONS_TABLE=oratio-notifications
KNOWLEDGE_BASES_TABLE=oratio-knowledgebases
```

### Option B: DynamoDB Local (Recommended for Testing)

```bash
# Install DynamoDB Local
docker run -p 8000:8000 amazon/dynamodb-local

# Create tables
python scripts/create_local_tables.py
```

### Option C: Real DynamoDB (Production-Ready)

```bash
# Use AWS CDK to create tables
cd infrastructure
pip install -r requirements.txt
cdk bootstrap
cdk deploy OratioDatabaseStack
```

---

## Step 5: Storage Setup (SIMPLIFIED OPTIONS)

### Option A: Local File Storage (Fastest)

Create local directories:
```bash
mkdir -p local_storage/knowledge-bases
mkdir -p local_storage/generated-code
mkdir -p local_storage/recordings
```

Add to `.env`:
```bash
# Use local paths (modify code to use local storage)
KB_BUCKET=oratio-knowledge-bases
CODE_BUCKET=oratio-generated-code
RECORDINGS_BUCKET=oratio-recordings
```

### Option B: Real S3 Buckets

```bash
# Create S3 buckets
aws s3 mb s3://oratio-knowledge-bases-$(aws sts get-caller-identity --query Account --output text)
aws s3 mb s3://oratio-generated-code-$(aws sts get-caller-identity --query Account --output text)
aws s3 mb s3://oratio-recordings-$(aws sts get-caller-identity --query Account --output text)
```

Add to `.env`:
```bash
KB_BUCKET=oratio-knowledge-bases-123456789012
CODE_BUCKET=oratio-generated-code-123456789012
RECORDINGS_BUCKET=oratio-recordings-123456789012
```

---

## Step 6: Bedrock Agent Setup (OPTIONAL)

For the meta-agent (AgentCreator), you need to deploy an agent to Bedrock.

### 6.1 Skip for Now

Leave empty in `.env`:
```bash
AGENTCREATOR_AGENT_ID=
AGENTCREATOR_AGENT_ALIAS_ID=
```

### 6.2 (Later) Deploy Agent

```bash
# Use CDK or console to create agent
cd infrastructure
cdk deploy OratioAgentStack
```

---

## Step 7: Step Functions (OPTIONAL)

For agent creation workflow orchestration.

### 7.1 Skip for Now

Leave empty in `.env`:
```bash
AGENT_CREATION_STATE_MACHINE_ARN=
```

### 7.2 (Later) Deploy Step Functions

```bash
cd infrastructure
cdk deploy OratioWorkflowStack
```

---

## 🚀 Minimal Working Configuration

Here's the **absolute minimum** to get started:

```bash
# AWS Configuration (REQUIRED)
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012  # Your actual account ID

# Bedrock (REQUIRED)
BEDROCK_REGION=us-east-1

# JWT (REQUIRED)
JWT_SECRET_KEY=your-generated-secret-here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Datadog (REQUIRED for hackathon)
DD_API_KEY=your-datadog-api-key
DD_APP_KEY=your-datadog-app-key
DD_SERVICE=oratio-backend
DD_ENV=hackathon
DD_VERSION=1.0.0
DD_TRACE_ENABLED=true
DD_LLM_OBS_ENABLED=true

# Voice Providers (REQUIRED)
MINIMAX_API_KEY=your-minimax-key
MINIMAX_GROUP_ID=your-group-id
GOOGLE_API_KEY=your-google-key

# Everything else can use defaults
USERS_TABLE=oratio-users
AGENTS_TABLE=oratio-agents
SESSIONS_TABLE=oratio-sessions
API_KEYS_TABLE=oratio-api-keys
NOTIFICATIONS_TABLE=oratio-notifications
KNOWLEDGE_BASES_TABLE=oratio-knowledgebases
KB_BUCKET=oratio-knowledge-bases
CODE_BUCKET=oratio-generated-code
RECORDINGS_BUCKET=oratio-recordings
COGNITO_USER_POOL_ID=
COGNITO_CLIENT_ID=
AGENTCREATOR_AGENT_ID=
AGENTCREATOR_AGENT_ALIAS_ID=
AGENT_CREATION_STATE_MACHINE_ARN=
```

---

## 🧪 Testing Your Setup

```bash
# Navigate to backend
cd backend

# Create .env file
cp .env.example .env
# Edit .env with your values

# Install dependencies
pip install -r requirements.txt

# Run test script
python test_hackathon_setup.py

# Start the server
uvicorn main:app --reload
```

---

## 📝 Next Steps

1. ✅ Get AWS Account ID
2. ✅ Enable Bedrock models
3. ✅ Generate JWT secret
4. ✅ Get Datadog API keys
5. ✅ Get MiniMax API key
6. ✅ Get Google API key
7. ✅ Create `.env` file
8. ✅ Test setup
9. ⚠️ (Optional) Set up DynamoDB
10. ⚠️ (Optional) Set up S3
11. ⚠️ (Optional) Set up Cognito
12. ⚠️ (Optional) Deploy agents

---

## 🆘 Troubleshooting

### "Access Denied" errors
- Check AWS credentials: `aws sts get-caller-identity`
- Verify IAM permissions for Bedrock, DynamoDB, S3

### "Model not found" errors
- Enable model access in Bedrock console
- Wait a few minutes for approval

### "Table not found" errors
- Create DynamoDB tables or use in-memory storage
- Check table names match `.env` configuration

### Import errors
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.11+)

---

## 💡 Pro Tips

1. **Use AWS Free Tier** - Most services have generous free tiers
2. **Start Simple** - Get voice working first, add features later
3. **Mock What You Can** - Use in-memory storage for development
4. **Monitor Costs** - Set up billing alerts in AWS Console
5. **Use LocalStack** - For local AWS service simulation

---

## 📚 Resources

- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS CLI Configuration](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [DynamoDB Local](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBLocal.html)
- [LocalStack](https://localstack.cloud/)
