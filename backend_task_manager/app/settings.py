import os
from pydantic import BaseModel


class Settings(BaseModel):
    # App
    APP_NAME: str = "Task Manager"
    ENV: str = os.getenv("ENV", "dev")  # dev / prod

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-change-me")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))  # 24h

    # Demo user (useful for free deployments)
    CREATE_DEMO_USER: bool = os.getenv("CREATE_DEMO_USER", "true").lower() == "true"
    DEMO_USERNAME: str = os.getenv("DEMO_USERNAME", "demo")
    DEMO_PASSWORD: str = os.getenv("DEMO_PASSWORD", "demo1234")

    # CORS
    # Comma-separated list of allowed origins. Example:
    # CORS_ORIGINS="https://example.com,https://www.example.com"
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    def cors_origins_list(self) -> list[str]:
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [x.strip() for x in self.CORS_ORIGINS.split(",") if x.strip()]


settings = Settings()
