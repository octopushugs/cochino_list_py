from contextlib import asynccontextmanager
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .services import ScrapeAndPopulateService
from . import models, schemas, database

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    scheduler = AsyncIOScheduler()
    scraper = ScrapeAndPopulateService()
    # Schedule the job to run every day at midnight (hour=0, minute=0)
    scheduler.add_job(scraper.populate_closures_job, 'cron', hour=0, minute=0)
    scheduler.start()
    yield
    # Shutdown logic
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/establishments", response_model=List[schemas.EstablishmentBase])
def read_establishments(
  skip: int = 0,
  limit: int = 100,
  db: Session = Depends(database.get_db)
):
  query = select(models.Establishment).offset(skip).limit(limit)
  establishments = db.execute(query).scalars().all()
  return establishments

@app.get("/closures", response_model=List[schemas.ClosureRead])
def read_closures(
  db: Session = Depends(database.get_db)
):
  # Calculate the date 6 months ago
  six_months_ago = datetime.now() - timedelta(days=180)
  
  query = (
      select(models.Closure)
      .options(joinedload(models.Closure.establishment))
      .where(models.Closure.created_at >= six_months_ago)
  )
  return db.execute(query).scalars().all()