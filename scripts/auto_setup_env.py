#!/usr/bin/env python3
"""
Automated environment setup using AWS CLI and system tools
This script automatically detects and configures what it can
"""

import os
import subprocess
import secrets
import json
from pathlib import Path


def run_command(cmd, capture=True, timeout=10):
    """Run a shell command and return output"""
    try:
        if capture:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip(), result.returncode
        else:
            result = subprocess.run(cmd, shell=True, timeout=timeout)
            return "", result.returncode
    except subprocess.TimeoutExpired:
        return "", -1
    except Exception as e:
        return str(e), -1


def print_section(title):
    """Print a formatted section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_status(emoji, message):
    """Print a status message"""
    print(f"{emoji} {message}")


def get_aws_account_id():
    """Get AWS account ID from AWS CLI"""
    print_status("🔍", "Detecting AWS Account ID...")
    output, code = run_command("aws sts get-caller-identity --query Account --output text")
    if code == 0 and output:
        print_status("✅", f"Found AWS Account: {output}")
        return output
    print_status("⚠️", "Could not detect AWS account. Make sure AWS CLI is configured.")
    return ""


def get_aws_region():
    """Get default AWS region"""
    print_status("🔍", "Detecting AWS Region...")
    output, code = run_command("aws configure get region")
    if code == 0 and output:
        print_status("✅", f"Found AWS Region: {output}")
        return output
    print_status("ℹ️", "Using default region: us-east-1")
    return "us-east-1"


def check_bedrock_access():
    """Check if Bedrock is accessible"""
    print_status("🔍", "Checking Bedrock access...")
    output, code = run_command(
        "aws bedrock list-foundation-models --region us-east-1 --query 'modelSummaries[0].modelId' --output text",
        timeout=15
    )
    if code == 0 and output and "error" not in output.lower():
        print_status("✅", "Bedrock access confirmed")
        return True
    print_status("⚠️", "Bedrock access not confirmed. You may need to enable model access in AWS Console.")
    return False


def generate_jwt_secret():
    """Generate a secure JWT secret"""
    print_status("🔐", "Generating JWT secret...")
    secret = secrets.token_urlsafe(32)
    print_status("✅", f"Generated JWT secret: {secret[:20]}...")
    return secret


def check_datadog_keys():
    """Check if Datadog keys are in environment"""
    dd_api = os.getenv("DD_API_KEY", "")
    dd_app = os.getenv("DD_APP_KEY", "")
    
    if dd_api and dd_app:
        print_status("✅", "Found Datadog keys in environment")
        return dd_api, dd_app
    
    print_status("ℹ️", "Datadog keys not found in environment")
    return "", ""


def prompt_for_keys():
    """Prompt user for required API keys"""
    print_section("Required API Keys")
    print("Please provide the following API keys:")
    print("(Press Enter to skip optional keys)\n")
    
    keys = {}
    
    # Datadog (required)
    print("📊 Datadog API Keys (REQUIRED)")
    print("Get from: https://app.datadoghq.com/organization-settings/api-keys\n")
    keys["DD_API_KEY"] = input("Datadog API Key: ").strip()
    keys["DD_APP_KEY"] = input("Datadog Application Key: ").strip()
    
    # MiniMax (required)
    print("\n🎤 MiniMax Voice API (REQUIRED)")
    print("Apply for free credits: https://forms.gle/Fazk8r87QmudNLNd6\n")
    keys["MINIMAX_API_KEY"] = input("MiniMax API Key: ").strip()
    keys["MINIMAX_GROUP_ID"] = input("MiniMax Group ID: ").strip()
    
    # Google Gemini (required)
    print("\n🤖 Google Gemini API (REQUIRED)")
    print("Get from: https://aistudio.google.com/app/apikey\n")
    keys["GOOGLE_API_KEY"] = input("Google API Key: ").strip()
    
    return keys


def create_env_file(config):
    """Create .env file with configuration"""
    env_path = Path("backend/.env")
    
    # Check if file exists
    if env_path.exists():
        response = input("\n⚠️  .env file already exists. Overwrite? (yes/no): ").strip().lower()
        if response not in ["yes", "y"]:
            print_status("ℹ️", "Keeping existing .env file")
            return False
    
    # Create .env content
    content = f"""# AWS Configuration
AWS_REGION={config['AWS_REGION']}
AWS_ACCOUNT_ID={config['AWS_ACCOUNT_ID']}

# DynamoDB Tables
USERS_TABLE=oratio-users
AGENTS_TABLE=oratio-agents
SESSIONS_TABLE=oratio-sessions
API_KEYS_TABLE=oratio-api-keys
NOTIFICATIONS_TABLE=oratio-notifications
KNOWLEDGE_BASES_TABLE=oratio-knowledgebases

# S3 Buckets
KB_BUCKET=oratio-knowledge-bases
CODE_BUCKET=oratio-generated-code
RECORDINGS_BUCKET=oratio-recordings

# Cognito (Optional - leave empty for JWT-only auth)
COGNITO_USER_POOL_ID=
COGNITO_CLIENT_ID=
COGNITO_REGION={config['AWS_REGION']}

# JWT Authentication
JWT_SECRET_KEY={config['JWT_SECRET_KEY']}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Step Functions (Optional)
AGENT_CREATION_STATE_MACHINE_ARN=

# Bedrock
BEDROCK_REGION={config['BEDROCK_REGION']}
AGENTCREATOR_AGENT_ID=
AGENTCREATOR_AGENT_ALIAS_ID=

# ========================================
# HACKATHON REQUIREMENTS
# ========================================

# Datadog Observability (REQUIRED)
DD_API_KEY={config['DD_API_KEY']}
DD_APP_KEY={config['DD_APP_KEY']}
DD_SERVICE=oratio-backend
DD_ENV=hackathon
DD_VERSION=1.0.0
DD_TRACE_ENABLED=true
DD_LLM_OBS_ENABLED=true

# MiniMax Voice (PRIMARY - REQUIRED)
MINIMAX_API_KEY={config['MINIMAX_API_KEY']}
MINIMAX_GROUP_ID={config['MINIMAX_GROUP_ID']}
MINIMAX_API_URL=https://api.minimax.chat/v1/voice
MINIMAX_VOICE_MODEL=speech-01

# Google Gemini (BACKUP - REQUIRED)
GOOGLE_API_KEY={config['GOOGLE_API_KEY']}
GEMINI_MODEL=gemini-2.0-flash-exp
"""
    
    # Write file
    env_path.parent.mkdir(parents=True, exist_ok=True)
    with open(env_path, "w") as f:
        f.write(content)
    
    print_status("✅", f"Created .env file: {env_path}")
    return True


def update_datadog_mcp_config(dd_api_key, dd_app_key):
    """Update Datadog MCP configuration"""
    mcp_path = Path(".kiro/settings/mcp.json")
    
    if not mcp_path.exists():
        print_status("⚠️", "MCP config not found, skipping Datadog MCP update")
        return
    
    try:
        with open(mcp_path, "r") as f:
            config = json.load(f)
        
        if "mcpServers" in config and "datadog" in config["mcpServers"]:
            config["mcpServers"]["datadog"]["env"]["DD_API_KEY"] = dd_api_key
            config["mcpServers"]["datadog"]["env"]["DD_APP_KEY"] = dd_app_key
            
            with open(mcp_path, "w") as f:
                json.dump(config, f, indent=2)
            
            print_status("✅", "Updated Datadog MCP configuration")
        else:
            print_status("ℹ️", "Datadog MCP server not configured")
    
    except Exception as e:
        print_status("⚠️", f"Could not update MCP config: {e}")


def print_next_steps(config):
    """Print next steps for the user"""
    print_section("Setup Complete! 🎉")
    
    print("✅ Configuration Summary:")
    print(f"   • AWS Account: {config['AWS_ACCOUNT_ID']}")
    print(f"   • AWS Region: {config['AWS_REGION']}")
    print(f"   • JWT Secret: Generated")
    print(f"   • Datadog: {'Configured' if config['DD_API_KEY'] else 'Not configured'}")
    print(f"   • MiniMax: {'Configured' if config['MINIMAX_API_KEY'] else 'Not configured'}")
    print(f"   • Gemini: {'Configured' if config['GOOGLE_API_KEY'] else 'Not configured'}")
    
    print("\n📋 Next Steps:")
    print("   1. Enable Bedrock models in AWS Console:")
    print("      → Go to: https://console.aws.amazon.com/bedrock/home#/modelaccess")
    print("      → Enable: Claude 3.5 Sonnet, Claude 3 Haiku, Titan Embeddings")
    print()
    print("   2. Test your setup:")
    print("      → cd backend")
    print("      → python test_hackathon_setup.py")
    print()
    print("   3. Start the backend:")
    print("      → cd backend")
    print("      → uvicorn main:app --reload")
    print()
    print("   4. (Optional) Create DynamoDB tables:")
    print("      → python scripts/create_dynamodb_tables.py")
    print()
    print("   5. (Optional) Create S3 buckets:")
    print("      → python scripts/create_s3_buckets.py")
    
    print("\n📚 Documentation:")
    print("   • Full setup guide: AWS_SETUP_GUIDE.md")
    print("   • Quick reference: QUICK_ENV_SETUP.md")
    print("   • Hackathon plan: HACKATHON_PLAN.md")


def main():
    """Main setup function"""
    print_section("Oratio Platform - Automated Setup")
    print("This script will automatically detect and configure your environment.\n")
    
    # Auto-detect what we can
    config = {}
    
    print_section("Step 1: Auto-Detection")
    config["AWS_ACCOUNT_ID"] = get_aws_account_id()
    config["AWS_REGION"] = get_aws_region()
    config["BEDROCK_REGION"] = config["AWS_REGION"]
    config["JWT_SECRET_KEY"] = generate_jwt_secret()
    
    # Check Bedrock access
    check_bedrock_access()
    
    # Check for existing Datadog keys
    dd_api, dd_app = check_datadog_keys()
    
    # Prompt for required keys
    print_section("Step 2: API Keys")
    
    if not dd_api or not dd_app:
        print_status("ℹ️", "We need some API keys that couldn't be auto-detected")
        api_keys = prompt_for_keys()
    else:
        print_status("✅", "Using Datadog keys from environment")
        api_keys = {
            "DD_API_KEY": dd_api,
            "DD_APP_KEY": dd_app,
            "MINIMAX_API_KEY": "",
            "MINIMAX_GROUP_ID": "",
            "GOOGLE_API_KEY": ""
        }
        
        # Still need voice provider keys
        print("\n🎤 Voice Provider Keys (REQUIRED)")
        api_keys["MINIMAX_API_KEY"] = input("MiniMax API Key: ").strip()
        api_keys["MINIMAX_GROUP_ID"] = input("MiniMax Group ID: ").strip()
        api_keys["GOOGLE_API_KEY"] = input("Google API Key: ").strip()
    
    # Merge configs
    config.update(api_keys)
    
    # Validate required keys
    required_keys = ["DD_API_KEY", "DD_APP_KEY", "MINIMAX_API_KEY", "MINIMAX_GROUP_ID", "GOOGLE_API_KEY"]
    missing_keys = [k for k in required_keys if not config.get(k)]
    
    if missing_keys:
        print_status("❌", f"Missing required keys: {', '.join(missing_keys)}")
        print_status("ℹ️", "You can run this script again or manually edit backend/.env")
    
    # Create .env file
    print_section("Step 3: Creating Configuration")
    if create_env_file(config):
        # Update Datadog MCP config if we have keys
        if config.get("DD_API_KEY") and config.get("DD_APP_KEY"):
            update_datadog_mcp_config(config["DD_API_KEY"], config["DD_APP_KEY"])
    
    # Print next steps
    print_next_steps(config)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
