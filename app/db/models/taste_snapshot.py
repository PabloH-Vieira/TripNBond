import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base  # adjust to your actual import path


class TasteProfileSnapshot(Base):
    __tablename__ = "taste_profile_snapshots"
    __table_args__ = (
        # One row per (account, time_range): a re-sync upserts this row
        # rather than accumulating an unbounded history log. Keeps storage
        # small and comfortably under Last.fm's 100MB reasonable-usage cap.
        UniqueConstraint("linked_account_id", "time_range", name="uq_account_time_range"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    linked_account_id: Mapped[uuid.UUID] = mapped_column(
        PGUUID(as_uuid=True),
        ForeignKey("linked_accounts.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Deliberately a plain string, not an enum: the two providers use
    # different vocabularies (Spotify: short_term/medium_term/long_term.
    # Last.fm: 7day/1month/3month/6month/12month/overall), and a future
    # provider will have its own again — there's no shared set of values
    # worth enforcing at the DB level.
    time_range: Mapped[str] = mapped_column(String(20), nullable=False)

    # [{provider_id, name, genres_or_tags: [...]}]
    top_artists: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # [{provider_id, isrc, name, artist_names: [...]}]
    top_tracks: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    # {"indie rock": 7, "mpb": 5, ...} — Spotify genres and Last.fm tags
    # merge into this same shape.
    genre_frequency: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    computed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    linked_account: Mapped["LinkedAccount"] = relationship(
        back_populates="taste_snapshots"
    )