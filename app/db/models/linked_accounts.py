import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, LargeBinary, String, UniqueConstraint, func
from sqlalchemy import Enum as SAEnum
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ProviderName(str, enum.Enum):
    SPOTIFY = "spotify"
    LASTFM = "lastfm"


class LinkStatus(str, enum.Enum):
    ACTIVE = "active"
    NEEDS_REAUTH = "needs_reauth"
    REVOKED = "revoked"


class LinkedAccount(Base):
    __tablename__ = "linked_accounts"
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_provider"),
    )

    # uuid from postgres provides a unique id when creating a ORM without having to access db in order to get a value from a sequence
    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # native_enum=False -> stored as a plain VARCHAR with a CHECK constraint,
    # so adding a third provider later is a normal migration, not an ALTER TYPE.
    provider: Mapped[ProviderName] = mapped_column(
        SAEnum(ProviderName, native_enum=False, length=20), nullable=False
    )

    # Spotify: opaque user id. Last.fm: the account's username (public by
    # design on their side) — still only meaningful paired with the
    # encrypted credential below.
    provider_user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Spotify: OAuth access token. Last.fm: the session key. Same
    # encrypted-at-rest treatment either way — see the token vault service.
    access_token_enc: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)

    # Spotify only. Always NULL for lastfm rows — its session key doesn't
    # expire, so there's nothing to refresh (MusicProviderAdapter.refresh()
    # is a documented no-op for that provider).
    refresh_token_enc: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)

    scope: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # NULL for lastfm; set for spotify (tokens expire ~hourly).
    token_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    status: Mapped[LinkStatus] = mapped_column(
        SAEnum(LinkStatus, native_enum=False, length=20),
        default=LinkStatus.ACTIVE,
        nullable=False,
    )

    connected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_synced_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="linked_accounts")
    taste_snapshots: Mapped[list["TasteProfileSnapshot"]] = relationship(
        back_populates="linked_account", cascade="all, delete-orphan"
    )