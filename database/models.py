"""
Модели базы данных
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, String, Text, Integer, DateTime, Boolean, Numeric, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from database.session import Base


class UserRole(str, enum.Enum):
    """Роли пользователей"""
    USER = "user"
    ADMIN = "admin"
    MODERATOR = "moderator"


class EventStatus(str, enum.Enum):
    """Статусы событий"""
    UPCOMING = "upcoming"  # Предстоящее
    LIVE = "live"  # В эфире
    FINISHED = "finished"  # Завершено
    CANCELLED = "cancelled"  # Отменено


class OrderStatus(str, enum.Enum):
    """Статусы заказов"""
    PENDING = "pending"  # Ожидает оплаты
    PAID = "paid"  # Оплачен
    CANCELLED = "cancelled"  # Отменен
    REFUNDED = "refunded"  # Возвращен


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    telegram_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    language_code: Mapped[str] = mapped_column(String(10), default="ru")
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER)
    is_premium: Mapped[bool] = mapped_column(Boolean, default=False)
    balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="user")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.telegram_id} (@{self.username})>"


class Event(Base):
    """Модель события (спектакля)"""
    __tablename__ = "events"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    poster_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=120)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    max_viewers: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    stream_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    invite_link: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    status: Mapped[EventStatus] = mapped_column(SQLEnum(EventStatus), default=EventStatus.UPCOMING)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    orders: Mapped[list["Order"]] = relationship("Order", back_populates="event")
    tickets: Mapped[list["Ticket"]] = relationship("Ticket", back_populates="event")
    
    def __repr__(self):
        return f"<Event {self.id}: {self.title}>"


class Order(Base):
    """Модель заказа"""
    __tablename__ = "orders"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.PENDING)
    payment_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="orders")
    event: Mapped["Event"] = relationship("Event", back_populates="orders")
    ticket: Mapped[Optional["Ticket"]] = relationship("Ticket", back_populates="order", uselist=False)
    
    def __repr__(self):
        return f"<Order {self.id}: {self.amount} ({self.status})>"


class Ticket(Base):
    """Модель билета"""
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.telegram_id"), nullable=False)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey("events.id"), nullable=False)
    access_token: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    qr_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_used: Mapped[bool] = mapped_column(Boolean, default=False)
    used_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    # Relationships
    order: Mapped["Order"] = relationship("Order", back_populates="ticket")
    user: Mapped["User"] = relationship("User", back_populates="tickets")
    event: Mapped["Event"] = relationship("Event", back_populates="tickets")
    
    def __repr__(self):
        return f"<Ticket {self.id} for Event {self.event_id}>"


class ContentPost(Base):
    """Модель поста контента (для ИИ-генерации)"""
    __tablename__ = "content_posts"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    content_type: Mapped[str] = mapped_column(String(50), nullable=False)  # text, image, video
    content_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    content_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    scheduled_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    published_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pending")  # pending, published, failed
    channel_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    message_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ContentPost {self.id}: {self.content_type}>"
