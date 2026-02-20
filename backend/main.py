from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from config import settings
from routers import agents, auth, chat, api_keys, knowledge_bases

# Voice router requires AWS Bedrock Smithy SDK — optional for hackathon demo
try:
    from routers import voice_simple as voice
    VOICE_AVAILABLE = True
except ImportError:
    print("⚠️  Voice router not available (aws_sdk_bedrock_runtime not installed)")
    VOICE_AVAILABLE = False
    voice = None

# Import observability (optional - will work without ddtrace)
try:
    from observability.datadog_config import datadog_config, metrics
    DATADOG_AVAILABLE = True
except ImportError:
    print("⚠️  Datadog not available (ddtrace not installed)")
    DATADOG_AVAILABLE = False
    datadog_config = None
    metrics = None

# Import voice provider manager
from services.voice_providers.voice_manager import voice_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    print("🚀 Starting Oratio API...")
    if DATADOG_AVAILABLE:
        print(f"📊 Datadog: {datadog_config.service_name} ({datadog_config.env})")
    else:
        print("📊 Datadog: Not available (install ddtrace to enable)")

    # Initialize voice providers
    await voice_manager.initialize()

    yield

    # Shutdown
    print("👋 Shutting down Oratio API...")
    await voice_manager.shutdown()


app = FastAPI(
    title="Oratio API",
    description="AI-Architected Voice Agents for Modern Enterprises",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(agents.router, prefix=settings.API_V1_PREFIX)
app.include_router(api_keys.router, prefix=settings.API_V1_PREFIX)
app.include_router(knowledge_bases.router, prefix=settings.API_V1_PREFIX)
app.include_router(chat.router, prefix=settings.API_V1_PREFIX)
if VOICE_AVAILABLE:
    app.include_router(voice.router, prefix=settings.API_V1_PREFIX)  # Voice WebSocket (simplified)


@app.get("/")
async def root():
    return {
        "message": "Oratio API",
        "version": "0.1.0",
        "datadog_enabled": DATADOG_AVAILABLE and datadog_config.trace_enabled if DATADOG_AVAILABLE else False,
        "voice_provider": voice_manager.get_current_provider_name(),
    }


@app.get("/health")
async def health_check():
    """Health check endpoint with provider status"""
    provider_status = voice_manager.get_provider_status()

    return {
        "status": "healthy",
        "service": datadog_config.service_name if DATADOG_AVAILABLE else "oratio-backend",
        "environment": datadog_config.env if DATADOG_AVAILABLE else "development",
        "voice_providers": provider_status,
        "datadog_available": DATADOG_AVAILABLE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
