#!/usr/bin/env python3
"""
Interactive script to set up .env file for Oratio platform
"""

import os
import secrets
import subprocess
from pathlib import Path


def print_header(text):
    """Print a formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def print_step(number, text):
    """Print a step number"""
    print(f"\n🔹 Step {number}: {text}")


def get_input(prompt, default="", required=False, secret=False):
    """Get user input with optional default"""
    if default:
        prompt_text = f"{prompt} [{default}]: "
    else:
        prompt_text = f"{prompt}: "
    
    if secret:
        prompt_text += "(will not be displayed) "
    
    value = input(prompt_text).strip()
    
    if not value:
        value = default
    
    if required and not value:
        print("❌ This field is required!")
        return get_input(prompt, default, required, secret)
    
    return value


def get_aws_account_id():
    """Try to get AWS account ID from AWS CLI"""
    try:
        result = subprocess.run(
            ["aws", "sts", "get-caller-identity", "--query", "Account", "--output", "text"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def generate_jwt_secret():
    """Generate a secure JWT secret"""
    return secrets.token_urlsafe(32)


def main():
    print_header("Oratio Platform - Environment Setup")
    print("This script will help you create a .env file for the backend.")
    print("Press Enter to use default values shown in brackets.")
    
    # Check if .env already exists
    env_path = Path("backend/.env")
    if env_path.exists():
        overwrite = get_input("\n⚠️  .env file already exists. Overwrite? (yes/no)", "no")
        if overwrite.lower() not in ["yes", "y"]:
            print("Exiting without changes.")
            return
    
    config = {}
    
    # AWS Configuration
    print_header("AWS Configuration")
    print("You need an AWS account with Bedrock access.")
    
    print_step(1, "AWS Account ID")
    detected_account = get_aws_account_id()
    if detected_account:
        print(f"✅ Detected AWS Account ID: {detected_account}")
        config["AWS_ACCOUNT_ID"] = detected_account
    else:
        print("Run: aws sts get-caller-identity --query Account --output text")
        config["AWS_ACCOUNT_ID"] = get_input("AWS Account ID", required=True)
    
    config["AWS_REGION"] = get_input("AWS Region", "us-east-1")
    config["BEDROCK_REGION"] = get_input("Bedrock Region", config["AWS_REGION"])
    
    # JWT Configuration
    print_header("Authentication Configuration")
    print_step(2, "JWT Secret Key")
    print("Generating a secure JWT secret...")
    config["JWT_SECRET_KEY"] = generate_jwt_secret()
    print(f"✅ Generated: {config['JWT_SECRET_KEY'][:20]}...")
    
    config["JWT_ALGORITHM"] = "HS256"
    config["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
    
    # Cognito (Optional)
    print("\n🔹 Cognito (Optional - leave empty to skip)")
    config["COGNITO_USER_POOL_ID"] = get_input("Cognito User Pool ID (optional)", "")
    config["COGNITO_CLIENT_ID"] = get_input("Cognito Client ID (optional)", "")
    config["COGNITO_REGION"] = config["AWS_REGION"]
    
    # Datadog Configuration
    print_header("Datadog Observability (REQUIRED)")
    print("Get your API keys from: https://app.datadoghq.com/organization-settings/api-keys")
    
    print_step(3, "Datadog API Keys")
    config["DD_API_KEY"] = get_input("Datadog API Key", required=True, secret=True)
    config["DD_APP_KEY"] = get_input("Datadog Application Key", required=True, secret=True)
    config["DD_SERVICE"] = get_input("Service Name", "oratio-backend")
    config["DD_ENV"] = get_input("Environment", "hackathon")
    config["DD_VERSION"] = get_input("Version", "1.0.0")
    config["DD_TRACE_ENABLED"] = "true"
    config["DD_LLM_OBS_ENABLED"] = "true"
    
    # Voice Providers
    print_header("Voice Providers (REQUIRED)")
    
    print_step(4, "MiniMax Voice (Primary)")
    print("Apply for free credits: https://forms.gle/Fazk8r87QmudNLNd6")
    config["MINIMAX_API_KEY"] = get_input("MiniMax API Key", required=True, secret=True)
    config["MINIMAX_GROUP_ID"] = get_input("MiniMax Group ID", required=True)
    config["MINIMAX_API_URL"] = get_input("MiniMax API URL", "https://api.minimax.chat/v1/voice")
    config["MINIMAX_VOICE_MODEL"] = get_input("MiniMax Voice Model", "speech-01")
    
    print_step(5, "Google Gemini (Backup)")
    print("Get API key from: https://aistudio.google.com/app/apikey")
    config["GOOGLE_API_KEY"] = get_input("Google API Key", required=True, secret=True)
    config["GEMINI_MODEL"] = get_input("Gemini Model", "gemini-2.0-flash-exp")
    
    # Database Tables (Use defaults)
    print_header("Database Configuration")
    print("Using default table names (can be created later)")
    config["USERS_TABLE"] = "oratio-users"
    config["AGENTS_TABLE"] = "oratio-agents"
    config["SESSIONS_TABLE"] = "oratio-sessions"
    config["API_KEYS_TABLE"] = "oratio-api-keys"
    config["NOTIFICATIONS_TABLE"] = "oratio-notifications"
    config["KNOWLEDGE_BASES_TABLE"] = "oratio-knowledgebases"
    
    # S3 Buckets (Use defaults)
    print_header("Storage Configuration")
    print("Using default bucket names (can be created later)")
    config["KB_BUCKET"] = "oratio-knowledge-bases"
    config["CODE_BUCKET"] = "oratio-generated-code"
    config["RECORDINGS_BUCKET"] = "oratio-recordings"
    
    # Optional Services
    print_header("Optional Services")
    print("Leave empty to skip these features for now")
    config["AGENTCREATOR_AGENT_ID"] = get_input("AgentCreator Agent ID (optional)", "")
    config["AGENTCREATOR_AGENT_ALIAS_ID"] = get_input("AgentCreator Agent Alias ID (optional)", "")
    config["AGENT_CREATION_STATE_MACHINE_ARN"] = get_input("Step Functions ARN (optional)", "")
    
    # Write .env file
    print_header("Writing Configuration")
    
    env_content = """# AWS Configuration
AWS_REGION={AWS_REGION}
AWS_ACCOUNT_ID={AWS_ACCOUNT_ID}

# DynamoDB Tables
USERS_TABLE={USERS_TABLE}
AGENTS_TABLE={AGENTS_TABLE}
SESSIONS_TABLE={SESSIONS_TABLE}
API_KEYS_TABLE={API_KEYS_TABLE}
NOTIFICATIONS_TABLE={NOTIFICATIONS_TABLE}
KNOWLEDGE_BASES_TABLE={KNOWLEDGE_BASES_TABLE}

# S3 Buckets
KB_BUCKET={KB_BUCKET}
CODE_BUCKET={CODE_BUCKET}
RECORDINGS_BUCKET={RECORDINGS_BUCKET}

# Cognito
COGNITO_USER_POOL_ID={COGNITO_USER_POOL_ID}
COGNITO_CLIENT_ID={COGNITO_CLIENT_ID}
COGNITO_REGION={COGNITO_REGION}

# JWT
JWT_SECRET_KEY={JWT_SECRET_KEY}
JWT_ALGORITHM={JWT_ALGORITHM}
ACCESS_TOKEN_EXPIRE_MINUTES={ACCESS_TOKEN_EXPIRE_MINUTES}

# Step Functions
AGENT_CREATION_STATE_MACHINE_ARN={AGENT_CREATION_STATE_MACHINE_ARN}

# Bedrock
BEDROCK_REGION={BEDROCK_REGION}
AGENTCREATOR_AGENT_ID={AGENTCREATOR_AGENT_ID}
AGENTCREATOR_AGENT_ALIAS_ID={AGENTCREATOR_AGENT_ALIAS_ID}

# ========================================
# HACKATHON REQUIREMENTS
# ========================================

# Datadog Observability (REQUIRED)
DD_API_KEY={DD_API_KEY}
DD_APP_KEY={DD_APP_KEY}
DD_SERVICE={DD_SERVICE}
DD_ENV={DD_ENV}
DD_VERSION={DD_VERSION}
DD_TRACE_ENABLED={DD_TRACE_ENABLED}
DD_LLM_OBS_ENABLED={DD_LLM_OBS_ENABLED}

# MiniMax Voice (PRIMARY - REQUIRED)
MINIMAX_API_KEY={MINIMAX_API_KEY}
MINIMAX_GROUP_ID={MINIMAX_GROUP_ID}
MINIMAX_API_URL={MINIMAX_API_URL}
MINIMAX_VOICE_MODEL={MINIMAX_VOICE_MODEL}

# Google Gemini (BACKUP - REQUIRED)
GOOGLE_API_KEY={GOOGLE_API_KEY}
GEMINI_MODEL={GEMINI_MODEL}
""".format(**config)
    
    # Create backend directory if it doesn't exist
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write file
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"✅ Configuration written to: {env_path}")
    
    # Summary
    print_header("Setup Complete!")
    print("✅ .env file created successfully")
    print("\n📋 Next Steps:")
    print("1. Review the .env file: backend/.env")
    print("2. Enable Bedrock models in AWS Console")
    print("3. Test your setup: cd backend && python test_hackathon_setup.py")
    print("4. Start the server: cd backend && uvicorn main:app --reload")
    print("\n📚 For detailed setup instructions, see: AWS_SETUP_GUIDE.md")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Please check your inputs and try again")
