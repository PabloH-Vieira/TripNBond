from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TripNBond API"
    DATABASE_URL: str
    SECRET_KEY: str

    # Diz ao Pydantic para ler o arquivo .env
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Instancia as configurações para serem importadas em outros arquivos
settings = Settings()