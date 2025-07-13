import uuid
from sqlalchemy import ARRAY, UUID, Column, String, DateTime, text, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        index=True,
    )
    user_name = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=True)
    name = Column(String, nullable=True)
    profile_img = Column(String, nullable=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=text("now()")
    )


class Chat(Base):
    __tablename__ = "chats"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user1_id = Column(UUID(as_uuid=True), nullable=False)
    user2_id = Column(UUID(as_uuid=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))


class Message(Base):
    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chat_id = Column(UUID(as_uuid=True), nullable=False)
    sender_id = Column(UUID(as_uuid=True), nullable=False)
    content = Column(String, nullable=True)
    attachment_url = Column(String, nullable=True)
    seen = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=text("now()"))
