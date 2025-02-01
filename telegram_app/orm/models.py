from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, DATETIME, SmallInteger, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class Team(Base):
    __tablename__ = 'users_team'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    recruit: Mapped[bool] = mapped_column(Boolean, default=True)


class TelegramUser(Base):
    __tablename__ = 'users_telegramuser'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_id: Mapped[int] = mapped_column(Integer, ForeignKey('users_team.id'))
    team_rel: Mapped[Team] = relationship('Team')
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    date_joined: Mapped[datetime] = mapped_column(DATETIME, nullable=False)
    is_commander: Mapped[bool] = mapped_column(Boolean, default=False)
    responsible_person: Mapped[bool] = mapped_column(Boolean, default=False)
    telegram_id: Mapped[int] = mapped_column(Integer)
    telegram_username: Mapped[str] = mapped_column(String(256))
    callsign: Mapped[str] = mapped_column(String(256))


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
