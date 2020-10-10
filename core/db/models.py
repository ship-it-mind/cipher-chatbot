from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from cryptography.fernet import Fernet

from core.db.database import Base


class User(Base):
    __tablename__ = "users"

    fb_id = Column(String, primary_key=True, unique=True, index=True)
    last_intent = Column(String)
    state = Column(String)
    last_used_key = Column(String)

    keys = relationship("Key", back_populates="owner")


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, default=Fernet.generate_key().decode())
    owner_id = Column(Integer, ForeignKey("users.fb_id"))

    owner = relationship("User", back_populates="keys")