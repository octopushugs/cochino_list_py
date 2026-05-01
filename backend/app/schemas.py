from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class EstablishmentBase(BaseModel):
  id: int
  uuid: UUID
  name: str = Field(..., min_length=1)
  permit_name: Optional[str] = Field(None)
  created_at: datetime
  updated_at: datetime
  address: str = Field(..., min_length=1)
  address2: Optional[str] = Field(None)
  city: str = Field(..., min_length=1)
  state: str = Field(..., min_length=1)
  zip: str = Field(..., min_length=1)

  model_config = ConfigDict(from_attributes=True)

class ClosureBase(BaseModel):
  id: int
  uuid: UUID
  establishment_id: int
  closed_on: datetime
  reopened_on: Optional[datetime] = None
  reason: Optional[str] = Field(None)
  result: Optional[str] = Field(None)
  created_at: datetime
  updated_at: datetime

  model_config = ConfigDict(from_attributes=True)

class ClosureRead(ClosureBase):
  establishment: EstablishmentBase

  model_config = ConfigDict(from_attributes=True)
