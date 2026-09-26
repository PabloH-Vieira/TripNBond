import uuid
from app.db.session import SessionLocal
from app.db.models import User, LinkedAccount, TasteProfileSnapshot
from app.db.models.linked_accounts import ProviderName, LinkStatus

def seed_db():
    # Inicia a sessão com o banco de dados
    db = SessionLocal()

    try:
        print("Iniciando a limpeza do banco de dados (opcional)...")
        # Para testes locais, é útil limpar os dados antigos antes de popular
        db.query(User).delete()
        db.commit()

        print("Populando usuários...")
        user1 = User(
            email="alice@example.com",
            display_name="Alice Silva",
            password_hash="fake_hash_123"
        )
        user2 = User(
            email="bob@example.com",
            display_name="Bob Oliveira",
            password_hash="fake_hash_456"
        )
        db.add_all([user1, user2])
        db.commit() # Commit para gerar os UUIDs no banco

        print("Populando contas conectadas...")
        # Simula a Alice conectando sua conta do Spotify
        spotify_account = LinkedAccount(
            user_id=user1.id,
            provider=ProviderName.SPOTIFY,
            provider_user_id="alice_spotify_88",
            access_token_enc=b"fake_encrypted_access_token",
            refresh_token_enc=b"fake_encrypted_refresh_token",
            scope="user-read-private user-top-read",
            status=LinkStatus.ACTIVE
        )
        db.add(spotify_account)
        db.commit()

        print("Populando histórico musical (Taste Snapshots)...")
        # Simula o processamento dos dados do Spotify da Alice
        snapshot = TasteProfileSnapshot(
            linked_account_id=spotify_account.id,
            time_range="medium_term",
            top_artists=[
                {"name": "Arctic Monkeys", "id": "7Ln80lUS6He07XvHI8qqHH", "genres": ["garage rock", "indie rock"]},
                {"name": "Dua Lipa", "id": "6M2wZ9GZgrQXHCFfjv46we", "genres": ["dance pop", "pop"]}
            ],
            top_tracks=[
                {"name": "Do I Wanna Know?", "artist_names": ["Arctic Monkeys"]},
                {"name": "Levitating", "artist_names": ["Dua Lipa"]}
            ],
            genre_frequency={
                "indie rock": 10,
                "dance pop": 8,
                "garage rock": 5
            }
        )
        db.add(snapshot)
        db.commit()

        print("✅ Banco de dados populado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao popular o banco de dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()