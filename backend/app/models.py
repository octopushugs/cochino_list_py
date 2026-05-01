import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, UUID, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base

class Establishment(Base):
  __tablename__ = "establishments"

  # Numerical Primary Key
  id: Mapped[int] = mapped_column(Integer, primary_key=True)

  # Separate UUID for external use
  uuid: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      unique=True,
      nullable=False,
      default=uuid.uuid4
  )
  
  name: Mapped[str] = mapped_column(String(1_000), nullable=False)
  permit_name: Mapped[str | None] = mapped_column(String(1_000))
  address: Mapped[str] = mapped_column(String(1_000), nullable=False)
  address2: Mapped[str | None] = mapped_column(String(1_000))
  city: Mapped[str] = mapped_column(String(1_000), nullable=False)
  state: Mapped[str] = mapped_column(String(1_000), nullable=False)
  zip: Mapped[str] = mapped_column(String(10), nullable=False)
  
  # Timestamps
  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      server_default=func.now(), 
      nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
      DateTime,
      server_default=func.now(),
      onupdate=func.now(), 
      nullable=False
  )

  closures: Mapped[list["Closure"]] = relationship("Closure", back_populates="establishment")

  def __repr__(self) -> str:
      return f"<Establishment(name={self.name!r}, id={self.id})>"
    
class Closure(Base):
  __tablename__ = "closures"

  # Numerical Primary Key
  id: Mapped[int] = mapped_column(Integer, primary_key=True)

  # Separate UUID for external use
  uuid: Mapped[uuid.UUID] = mapped_column(
      UUID(as_uuid=True),
      unique=True,
      nullable=False,
      default=uuid.uuid4
  )

  establishment_id: Mapped[int] = mapped_column(Integer, ForeignKey("establishments.id"), nullable=False)
  establishment: Mapped["Establishment"] = relationship("Establishment", back_populates="closures")
  closed_on: Mapped[datetime] = mapped_column(DateTime, nullable=False)
  reopened_on: Mapped[datetime | None] = mapped_column(DateTime)
  reason: Mapped[str | None] = mapped_column(String(1_000))
  result: Mapped[str | None] = mapped_column(String(255))

  # Timestamps
  created_at: Mapped[datetime] = mapped_column(
      DateTime,
      server_default=func.now(), 
      nullable=False
  )
  updated_at: Mapped[datetime] = mapped_column(
      DateTime,
      server_default=func.now(), 
      onupdate=func.now(), 
      nullable=False
  )

  def __repr__(self) -> str:
      return f"<Closure(id={self.id})>"