from .base import Base, now
from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, BigInteger
from sqlalchemy.orm import relationship


class TelegramChat(Base):
    __tablename__ = "telegram_chats"

    activator_id = Column(Integer, ForeignKey("players.id"), nullable=False, index=True)
    activator = relationship("Player", back_populates="telegram_chats")

    games = relationship("Game", back_populates="telegram_chat")

    chat_id = Column(BigInteger, nullable=False, primary_key=True, index=True)
    thread_id = Column(BigInteger, nullable=False)
    chat_title = Column(String, nullable=False)

    created_at = Column(DateTime, default=now, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False)
    message_with_tables_id = Column(BigInteger, nullable=True)
    message_with_tables = Column(String, nullable=True)
