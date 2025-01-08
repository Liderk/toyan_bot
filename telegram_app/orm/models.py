from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, DATETIME, SmallInteger
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class User(Base):
    __tablename__ = 'users_user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=True, default='')
    last_name: Mapped[str] = mapped_column(String(150), nullable=True, default='')
    email: Mapped[str] = mapped_column(String(254), unique=True, nullable=False, default='')
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_staff: Mapped[bool] = mapped_column(Boolean, default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    date_joined: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=True, default='')
    team: Mapped[str] = mapped_column(String(100), nullable=True)
    is_commander: Mapped[bool] = mapped_column(Boolean, default=False)
    telegram_id: Mapped[int] = mapped_column(Integer, nullable=True)


class Games(Base):
    __tablename__ = 'events_games'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    descriptions: Mapped[str] = mapped_column(String(1000), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    organizers: Mapped[str] = mapped_column(String(250), nullable=False)
    big: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    city: Mapped[str] = mapped_column(String(50), nullable=False)
    game_area: Mapped[str] = mapped_column(String(50), nullable=False)
    side_commander: Mapped[str] = mapped_column(String(50), nullable=True)
    judas_commander: Mapped[str] = mapped_column(String(50), nullable=True)


class EventChoices:
    TRAINING = 1
    GATHERING = 2


class Event(Base):
    __tablename__ = 'events_event'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    event_type: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    descriptions: Mapped[str] = mapped_column(String(1500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    organizers: Mapped[str] = mapped_column(String(250), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
