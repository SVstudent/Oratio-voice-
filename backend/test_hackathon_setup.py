"""
Quick test script to verify hackathon setup

Run this to check if all components are configured correctly.
"""

import os
import sys
import asyncio


def check_env_var(name: str, required: bool = True) -> bool:
    """Check if environment variable is set"""
    value = os.getenv(name)
    if value:
        print(f"✅ {name}: {'*' * min(len(value), 20)}")
        return True
    else:
        symbol = "❌" if required else "⚠️ "
        print(f"{symbol} {name}: Not set")
        return not required


async def test_datadog():
    """Test Datadog configuration"""
    print("\n📊 Testing Datadog Configuration...")
    try:
        from observability.datadog_config import datadog_config, metrics

        print(f"✅ Datadog module imported")
        print(f"   Service: {datadog_config.service_name}")
        print(f"   Environment: {datadog_config.env}")
        print(f"   Tracing: {datadog_config.trace_enabled}")
        print(f"   LLM Obs: {datadog_config.llm_obs_enabled}")

        # Test metrics
        metrics.agent_created("test_agent", "test_user")
        print(f"✅ Datadog metrics working")

        return True
    except Exception as e:
        print(f"❌ Datadog error: {e}")
        return False


async def test_minimax():
    """Test MiniMax configuration"""
    print("\n🎤 Testing MiniMax Configuration...")
    try:
        from services.voice_providers.minimax_service import minimax_service

        print(f"✅ MiniMax module imported")
        print(f"   Available: {minimax_service.is_available()}")

        if minimax_service.is_available():
            # Test health check
            healthy = await minimax_service.health_check()
            print(f"   Health: {'✅ Healthy' if healthy else '⚠️  Unhealthy'}")
            return healthy
        else:
            print(f"⚠️  MiniMax not configured (API key missing)")
            return False

    except Exception as e:
        print(f"❌ MiniMax error: {e}")
        return False


async def test_gemini():
    """Test Gemini configuration"""
    print("\n🤖 Testing Gemini Configuration...")
    try:
        from services.voice_providers.gemini_service import gemini_service

        print(f"✅ Gemini module imported")
        print(f"   Available: {gemini_service.is_available()}")

        if gemini_service.is_available():
            # Test health check
            healthy = await gemini_service.health_check()
            print(f"   Health: {'✅ Healthy' if healthy else '⚠️  Unhealthy'}")
            return healthy
        else:
            print(f"⚠️  Gemini not configured (API key missing)")
            return False

    except Exception as e:
        print(f"❌ Gemini error: {e}")
        return False


async def test_voice_manager():
    """Test voice provider manager"""
    print("\n🎙️  Testing Voice Provider Manager...")
    try:
        from services.voice_providers.voice_manager import voice_manager

        print(f"✅ Voice manager module imported")

        # Initialize
        await voice_manager.initialize()

        # Get status
        status = voice_manager.get_provider_status()
        print(f"   Current provider: {status['current']}")
        print(f"   MiniMax: {status['minimax']}")
        print(f"   Gemini: {status['gemini']}")

        return True

    except Exception as e:
        print(f"❌ Voice manager error: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("🏆 AWS x Datadog GenAI Hackathon - Setup Verification")
    print("=" * 60)

    # Check environment variables
    print("\n🔑 Checking Environment Variables...")

    required_vars = {
        # Datadog (Required)
        "DD_API_KEY": True,
        "DD_APP_KEY": False,  # Optional but recommended
        "DD_SERVICE": True,
        "DD_ENV": True,
        # MiniMax (Required)
        "MINIMAX_API_KEY": True,
        "MINIMAX_GROUP_ID": True,
        # Gemini (Required)
        "GOOGLE_API_KEY": True,
        # AWS (Required)
        "AWS_REGION": True,
        "BEDROCK_REGION": True,
    }

    env_results = []
    for var, required in required_vars.items():
        result = check_env_var(var, required)
        env_results.append(result)

    # Run component tests
    datadog_ok = await test_datadog()
    minimax_ok = await test_minimax()
    gemini_ok = await test_gemini()
    voice_manager_ok = await test_voice_manager()

    # Summary
    print("\n" + "=" * 60)
    print("📋 Summary")
    print("=" * 60)

    all_env_ok = all(env_results)
    print(f"Environment Variables: {'✅ All set' if all_env_ok else '⚠️  Some missing'}")
    print(f"Datadog: {'✅ Working' if datadog_ok else '❌ Issues'}")
    print(f"MiniMax: {'✅ Working' if minimax_ok else '⚠️  Not configured'}")
    print(f"Gemini: {'✅ Working' if gemini_ok else '⚠️  Not configured'}")
    print(f"Voice Manager: {'✅ Working' if voice_manager_ok else '❌ Issues'}")

    # Prize eligibility check
    print("\n🏆 Prize Eligibility Check:")
    aws_ok = check_env_var("AWS_REGION", required=False) and check_env_var(
        "BEDROCK_REGION", required=False
    )
    print(f"   AWS Infrastructure: {'✅' if aws_ok else '❌'}")
    print(f"   Datadog Observability: {'✅' if datadog_ok else '❌'}")
    print(f"   Voice Provider: {'✅' if (minimax_ok or gemini_ok) else '❌'}")

    if aws_ok and datadog_ok and (minimax_ok or gemini_ok):
        print("\n🎉 All hackathon requirements met! You're ready to compete!")
    else:
        print("\n⚠️  Some requirements missing. Check the errors above.")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Add parent directory to path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Run tests
    asyncio.run(main())
