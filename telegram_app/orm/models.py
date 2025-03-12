from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean, TIMESTAMP, DATETIME, SmallInteger, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship, backref

Base = declarative_base()


class Team(Base):
    __tablename__ = 'users_team'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), unique=True)
    recruit: Mapped[bool] = mapped_column(Boolean, default=True)

    telegram_users: Mapped[list["TelegramUser"]] = relationship("TelegramUser", back_populates="team_rel")


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
    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)


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
    toyan_commander: Mapped[str] = mapped_column(String(50), nullable=True)
    game_map: Mapped[str] = mapped_column(String, nullable=True)
    location_map: Mapped[str] = mapped_column(String, nullable=True)


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
    location_map: Mapped[str] = mapped_column(String, nullable=True)


# Модель PeriodChoices (перечисление)
class PeriodChoices:
    HOURS = 1
    DAYS = 2
    WEEK = 3
    MONTH = 4


# Модель NotificationPeriod
class NotificationPeriod(Base):
    __tablename__ = 'events_notificationperiod'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    period: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    amount: Mapped[int] = mapped_column(SmallInteger, nullable=False)

    def __repr__(self):
        return f"NotificationPeriod(id={self.id}, period={self.period}, amount={self.amount})"


class ContentType(Base):
    __tablename__ = 'django_content_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    app_label: Mapped[str]
    model: Mapped[str]


@dataclass
class RecipientType:
    BOT: int = 1
    CHANNEL: int = 2


class GameEventNotification(Base):
    __tablename__ = 'events_gameeventnotification'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content_type_id: Mapped[int] = mapped_column(Integer, ForeignKey('django_content_type.id'), nullable=False)
    object_id: Mapped[int]
    notification_period_id: Mapped[int] = mapped_column(Integer,
                                                        ForeignKey('events_notificationperiod.id'), nullable=False)
    notified: Mapped[bool] = mapped_column(Boolean, default=False)
    notification_date: Mapped[datetime] = mapped_column(DATETIME, nullable=True)
    allow_discussion: Mapped[bool] = mapped_column(Boolean, default=True)
    message_for: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Relationships
    content_type: Mapped["ContentType"] = relationship(backref=backref('notifications'))
    notification_period: Mapped["NotificationPeriod"] = relationship(backref=backref('schedulers'))
