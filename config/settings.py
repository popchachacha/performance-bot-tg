"""
Конфигурация приложения
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Настройки приложения из переменных окружения"""
    
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    # Telegram Bot
    bot_token: str
    admin_ids: str  # Comma-separated list
    
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "performance_bot"
    db_user: str = "postgres"
    db_password: str
    
    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    
    # OpenAI
    openai_api_key: str
    
    # Payments
    yukassa_shop_id: str = ""
    yukassa_secret_key: str = ""
    
    # Telegram Channel
    stream_channel_id: int
    
    # Logging
    log_level: str = "INFO"
    
    @property
    def database_url(self) -> str:
        """Формирование URL для подключения к БД"""
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def redis_url(self) -> str:
        """Формирование URL для подключения к Redis"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"
    
    @property
    def admin_list(self) -> List[int]:
        """Список ID администраторов"""
        return [int(admin_id.strip()) for admin_id in self.admin_ids.split(',') if admin_id.strip()]


# Глобальный экземпляр настроек
settings = Settings()
