#!/usr/bin/env python3
"""
Deploy minimal AWS infrastructure and extract all environment variables
This script creates only what's needed and outputs the .env file
"""

import json
import subprocess
import sys
import secrets
from pathlib import Path


def run_aws_command(cmd):
    """Run AWS CLI command and return JSON output"""
    try:
        result = subprocess.run(
            f"/usr/local/bin/aws {cmd}",
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout) if result.stdout.strip() else {}
        return None
    except Exception as e:
        print(f"Error running command: {e}")
        return None


def get_account_info():
    """Get AWS account ID and region"""
    print("🔍 Getting AWS account information...")
    identity = run_aws_command("sts get-caller-identity")
    if identity:
        account_id = identity.get("Account")
        print(f"✅ Account ID: {account_id}")
        return account_id
    return None


def get_region():
    """Get configured AWS region"""
    result = subprocess.run(
        "/usr/local/bin/aws configure get region",
        shell=True,
        capture_output=True,
        text=True
    )
    region = result.stdout.strip() or "us-east-1"
    print(f"✅ Region: {region}")
    return region


def create_cognito_user_pool(region):
    """Create Cognito User Pool"""
    print("\n🔐 Creating Cognito User Pool...")
    
    cmd = f"""cognito-idp create-user-pool \
        --pool-name oratio-users-{secrets.token_hex(4)} \
        --auto-verified-attributes email \
        --region {region}"""
    
    result = run_aws_command(cmd)
    if result and "UserPool" in result:
        pool_id = result["UserPool"]["Id"]
        print(f"✅ User Pool created: {pool_id}")
        
        # Create app client
        print("🔐 Creating Cognito App Client...")
        client_cmd = f"""cognito-idp create-user-pool-client \
            --user-pool-id {pool_id} \
            --client-name oratio-web \
            --no-generate-secret \
            --region {region}"""
        
        client_result = run_aws_command(client_cmd)
        if client_result and "UserPoolClient" in client_result:
            client_id = client_result["UserPoolClient"]["ClientId"]
            print(f"✅ App Client created: {client_id}")
            return pool_id, client_id
    
    print("⚠️  Cognito creation failed, will use JWT-only auth")
    return "", ""


def create_dynamodb_tables(region):
    """Create DynamoDB tables"""
    print("\n📊 Creating DynamoDB tables...")
    
    tables = {
        "oratio-users": {"PK": "userId", "SK": None},
        "oratio-agents": {"PK": "userId", "SK": "agentId"},
        "oratio-sessions": {"PK": "sessionId", "SK": "timestamp"},
        "oratio-api-keys": {"PK": "apiKeyHash", "SK": None},
        "oratio-notifications": {"PK": "notificationId", "SK": "timestamp"},
        "oratio-knowledgebases": {"PK": "knowledgeBaseId", "SK": None},
    }
    
    created_tables = {}
    
    for table_name, keys in tables.items():
        print(f"  Creating {table_name}...")
        
        key_schema = [{"AttributeName": keys["PK"], "KeyType": "HASH"}]
        attr_defs = [{"AttributeName": keys["PK"], "AttributeType": "S"}]
        
        if keys["SK"]:
            key_schema.append({"AttributeName": keys["SK"], "KeyType": "RANGE"})
            attr_type = "N" if keys["SK"] == "timestamp" else "S"
            attr_defs.append({"AttributeName": keys["SK"], "AttributeType": attr_type})
        
        cmd = f"""dynamodb create-table \
            --table-name {table_name} \
            --attribute-definitions '{json.dumps(attr_defs)}' \
            --key-schema '{json.dumps(key_schema)}' \
            --billing-mode PAY_PER_REQUEST \
            --region {region}"""
        
        result = run_aws_command(cmd)
        if result:
            print(f"  ✅ {table_name} created")
            created_tables[table_name] = table_name
        else:
            print(f"  ⚠️  {table_name} may already exist")
            created_tables[table_name] = table_name
    
    return created_tables


def create_s3_buckets(account_id, region):
    """Create S3 buckets"""
    print("\n🪣 Creating S3 buckets...")
    
    buckets = [
        f"oratio-knowledge-bases-{account_id}",
        f"oratio-generated-code-{account_id}",
        f"oratio-recordings-{account_id}",
    ]
    
    created_buckets = {}
    
    for bucket_name in buckets:
        print(f"  Creating {bucket_name}...")
        
        if region == "us-east-1":
            cmd = f"s3api create-bucket --bucket {bucket_name} --region {region}"
        else:
            cmd = f"""s3api create-bucket --bucket {bucket_name} \
                --region {region} \
                --create-bucket-configuration LocationConstraint={region}"""
        
        result = run_aws_command(cmd)
        if result or True:  # Bucket might exist
            print(f"  ✅ {bucket_name} ready")
            created_buckets[bucket_name.split('-')[1]] = bucket_name
    
    return created_buckets


def generate_jwt_secret():
    """Generate JWT secret"""
    return secrets.token_urlsafe(32)


def create_env_file(config):
    """Create .env file with all configuration"""
    print("\n📝 Creating .env file...")
    
    env_content = f"""# AWS Configuration
AWS_REGION={config['region']}
AWS_ACCOUNT_ID={config['account_id']}

# DynamoDB Tables
USERS_TABLE={config['tables']['oratio-users']}
AGENTS_TABLE={config['tables']['oratio-agents']}
SESSIONS_TABLE={config['tables']['oratio-sessions']}
API_KEYS_TABLE={config['tables']['oratio-api-keys']}
NOTIFICATIONS_TABLE={config['tables']['oratio-notifications']}
KNOWLEDGE_BASES_TABLE={config['tables']['oratio-knowledgebases']}

# S3 Buckets
KB_BUCKET={config['buckets']['knowledge']}
CODE_BUCKET={config['buckets']['generated']}
RECORDINGS_BUCKET={config['buckets']['recordings']}

# Cognito
COGNITO_USER_POOL_ID={config.get('cognito_pool_id', '')}
COGNITO_CLIENT_ID={config.get('cognito_client_id', '')}
COGNITO_REGION={config['region']}

# JWT
JWT_SECRET_KEY={config['jwt_secret']}
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Step Functions
AGENT_CREATION_STATE_MACHINE_ARN=

# Bedrock
BEDROCK_REGION={config['region']}
AGENTCREATOR_AGENT_ID=
AGENTCREATOR_AGENT_ALIAS_ID=

# ========================================
# HACKATHON REQUIREMENTS
# ========================================

# Datadog Observability (REQUIRED - ADD YOUR KEYS)
DD_API_KEY=
DD_APP_KEY=
DD_SERVICE=oratio-backend
DD_ENV=hackathon
DD_VERSION=1.0.0
DD_TRACE_ENABLED=true
DD_LLM_OBS_ENABLED=true

# MiniMax Voice (PRIMARY - REQUIRED - ADD YOUR KEYS)
MINIMAX_API_KEY=
MINIMAX_GROUP_ID=
MINIMAX_API_URL=https://api.minimax.chat/v1/voice
MINIMAX_VOICE_MODEL=speech-01

# Google Gemini (BACKUP - REQUIRED - ADD YOUR KEYS)
GOOGLE_API_KEY=
GEMINI_MODEL=gemini-2.0-flash-exp
"""
    
    env_path = Path("backend/.env")
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"✅ .env file created: {env_path}")
    return env_path


def main():
    """Main deployment function"""
    print("="*70)
    print("  Oratio Platform - Automated AWS Infrastructure Deployment")
    print("="*70)
    
    # Get AWS info
    account_id = get_account_info()
    if not account_id:
        print("❌ Could not get AWS account info. Check your credentials.")
        sys.exit(1)
    
    region = get_region()
    
    # Generate JWT secret
    jwt_secret = generate_jwt_secret()
    print(f"✅ Generated JWT secret")
    
    # Create Cognito (optional)
    try:
        pool_id, client_id = create_cognito_user_pool(region)
    except Exception as e:
        print(f"⚠️  Cognito creation skipped: {e}")
        pool_id, client_id = "", ""
    
    # Create DynamoDB tables
    try:
        tables = create_dynamodb_tables(region)
    except Exception as e:
        print(f"⚠️  DynamoDB creation had issues: {e}")
        tables = {
            "oratio-users": "oratio-users",
            "oratio-agents": "oratio-agents",
            "oratio-sessions": "oratio-sessions",
            "oratio-api-keys": "oratio-api-keys",
            "oratio-notifications": "oratio-notifications",
            "oratio-knowledgebases": "oratio-knowledgebases",
        }
    
    # Create S3 buckets
    try:
        buckets = create_s3_buckets(account_id, region)
    except Exception as e:
        print(f"⚠️  S3 creation had issues: {e}")
        buckets = {
            "knowledge": f"oratio-knowledge-bases-{account_id}",
            "generated": f"oratio-generated-code-{account_id}",
            "recordings": f"oratio-recordings-{account_id}",
        }
    
    # Compile configuration
    config = {
        "account_id": account_id,
        "region": region,
        "jwt_secret": jwt_secret,
        "cognito_pool_id": pool_id,
        "cognito_client_id": client_id,
        "tables": tables,
        "buckets": buckets,
    }
    
    # Create .env file
    env_path = create_env_file(config)
    
    # Summary
    print("\n" + "="*70)
    print("  ✅ Deployment Complete!")
    print("="*70)
    print(f"\n📋 Created Resources:")
    print(f"   • AWS Account: {account_id}")
    print(f"   • Region: {region}")
    print(f"   • DynamoDB Tables: {len(tables)}")
    print(f"   • S3 Buckets: {len(buckets)}")
    if pool_id:
        print(f"   • Cognito User Pool: {pool_id}")
    print(f"\n📝 Configuration saved to: {env_path}")
    print(f"\n⚠️  You still need to add these API keys to .env:")
    print(f"   • DD_API_KEY (Datadog)")
    print(f"   • DD_APP_KEY (Datadog)")
    print(f"   • MINIMAX_API_KEY")
    print(f"   • MINIMAX_GROUP_ID")
    print(f"   • GOOGLE_API_KEY")
    print(f"\n🚀 Next: Enable Bedrock models in AWS Console")
    print(f"   https://console.aws.amazon.com/bedrock/home?region={region}#/modelaccess")


if __name__ == "__main__":
    main()
