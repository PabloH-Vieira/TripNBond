from sqlalchemy import create_engine
from sqlalchemy.orm import declaretive_base, sessionmaker
from app.core.config import settings

# Cria o motor de conexão usando a URL das configurações
engine = create_engine(settings.DATABASE_URL)

# Cria a fábrica de sessões (cada requisição gera uma)
SessionLocal = sessionmaker(autocmmit=False, autoflush=False, bind=engine)

# Base para criar as tabelas
Base = declaretive_base

# Função que injeta o banco de dados nas rotas do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()