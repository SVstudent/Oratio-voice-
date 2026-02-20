from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1", validation_alias="API_V1_PREFIX")
    PROJECT_NAME: str = Field(default="Oratio", validation_alias="PROJECT_NAME")

    # CORS
    CORS_ORIGINS: list[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        validation_alias="CORS_ORIGINS",
    )

    # AWS Configuration
    AWS_REGION: str = Field(default="us-east-1", validation_alias="AWS_REGION")
    AWS_ACCOUNT_ID: str = Field(default="", validation_alias="AWS_ACCOUNT_ID")

    # DynamoDB Tables
    USERS_TABLE: str = Field(default="oratio-users", validation_alias="USERS_TABLE")
    AGENTS_TABLE: str = Field(default="oratio-agents", validation_alias="AGENTS_TABLE")
    KNOWLEDGE_BASES_TABLE: str = Field(
        default="oratio-knowledgebases", validation_alias="KNOWLEDGE_BASES_TABLE"
    )
    SESSIONS_TABLE: str = Field(default="oratio-sessions", validation_alias="SESSIONS_TABLE")
    API_KEYS_TABLE: str = Field(default="oratio-api-keys", validation_alias="API_KEYS_TABLE")
    NOTIFICATIONS_TABLE: str = Field(
        default="oratio-notifications", validation_alias="NOTIFICATIONS_TABLE"
    )

    # S3 Buckets
    KB_BUCKET: str = Field(default="oratio-knowledge-bases", validation_alias="KB_BUCKET")
    CODE_BUCKET: str = Field(default="oratio-generated-code", validation_alias="CODE_BUCKET")
    RECORDINGS_BUCKET: str = Field(default="oratio-recordings", validation_alias="RECORDINGS_BUCKET")

    # Cognito
    COGNITO_USER_POOL_ID: str = Field(default="", validation_alias="COGNITO_USER_POOL_ID")
    COGNITO_CLIENT_ID: str = Field(default="", validation_alias="COGNITO_CLIENT_ID")
    COGNITO_REGION: str = Field(default="us-east-1", validation_alias="COGNITO_REGION")

    # JWT
    JWT_SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production", validation_alias="JWT_SECRET_KEY"
    )
    JWT_ALGORITHM: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES"
    )

    # Step Functions
    AGENT_CREATION_STATE_MACHINE_ARN: str = Field(
        default="", validation_alias="AGENT_CREATION_STATE_MACHINE_ARN"
    )

    # Bedrock
    BEDROCK_REGION: str = Field(default="us-east-1", validation_alias="BEDROCK_REGION")
    AGENTCREATOR_AGENT_ID: str = Field(default="", validation_alias="AGENTCREATOR_AGENT_ID")
    AGENTCREATOR_AGENT_ALIAS_ID: str = Field(
        default="", validation_alias="AGENTCREATOR_AGENT_ALIAS_ID"
    )

    # Datadog Observability
    DD_API_KEY: str = Field(default="", validation_alias="DD_API_KEY")
    DD_APP_KEY: str = Field(default="", validation_alias="DD_APP_KEY")
    DD_SERVICE: str = Field(default="oratio-backend", validation_alias="DD_SERVICE")
    DD_ENV: str = Field(default="hackathon", validation_alias="DD_ENV")
    DD_VERSION: str = Field(default="1.0.0", validation_alias="DD_VERSION")
    DD_TRACE_ENABLED: bool = Field(default=True, validation_alias="DD_TRACE_ENABLED")
    DD_LLM_OBS_ENABLED: bool = Field(default=True, validation_alias="DD_LLM_OBS_ENABLED")

    # MiniMax Voice
    MINIMAX_API_KEY: str = Field(default="", validation_alias="MINIMAX_API_KEY")
    MINIMAX_GROUP_ID: str = Field(default="", validation_alias="MINIMAX_GROUP_ID")
    MINIMAX_API_URL: str = Field(
        default="https://api.minimax.chat/v1/voice", validation_alias="MINIMAX_API_URL"
    )
    MINIMAX_VOICE_MODEL: str = Field(default="speech-01", validation_alias="MINIMAX_VOICE_MODEL")

    # Google Gemini (Backup)
    GOOGLE_API_KEY: str = Field(default="", validation_alias="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.0-flash-exp", validation_alias="GEMINI_MODEL")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
