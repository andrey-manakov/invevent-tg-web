from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, relationship
import os

Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String, nullable=True)
    friends = relationship("Friend", back_populates="user", foreign_keys="Friend.user_id")

class Friend(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    friend_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="friends", foreign_keys=[user_id])

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    datetime = Column(DateTime)
    lat = Column(Float)
    lng = Column(Float)
    creator = relationship("User")

class EventJoin(Base):
    __tablename__ = "eventjoins"
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

def init_db():
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
