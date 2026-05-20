from datetime import datetime
from sqlalchemy import select
from .. import database, models

# TODO: We need a script that can look at existing closures and update 
# them as necessary. Requirements:
#   * When creating Closures, use find_or_create, unique on establishment and date, and scoped
#     to the last 14 days to prevent reading too much historic data
#   * If one exists, verify that the stored data matches the scraped data, update if it doesn't
class PopulateService:
  def __init__(self):
    pass

  @staticmethod
  def _sanitize_name(name: str | None) -> str | None:
    """Strips whitespace and trailing caret characters from names."""
    if name:
      return name.strip().rstrip('^')
    return name

  def populate_records(self, scraped_data: list[dict]):
    """
    Processes a list of scraped closure data.
    Finds or creates establishments and records new closures.
    """
    with database.SessionLocal() as db:
      for entry in scraped_data:
        sanitized_name = self._sanitize_name(entry["establishment_name"])
        sanitized_permit = self._sanitize_name(entry.get("permit_name"))
        timestamp = datetime.now()

        # Check if the establishment already exists

        stmt = select(models.Establishment).where(
          models.Establishment.name == sanitized_name,
          models.Establishment.permit_name == sanitized_permit,
          models.Establishment.address == entry["address"]
        )
        establishment = db.execute(stmt).scalar_one_or_none()

        if not establishment:
          establishment = models.Establishment(
            name=sanitized_name,
            permit_name=sanitized_permit,
            address=entry["address"],
            city=entry["city"],
            state="CA",  # Defaulting to CA for Orange County, update if we expand to other locales
            zip=entry["zip"],
            created_at=timestamp,
            updated_at=timestamp
          )
          db.add(establishment)
          # Flush to get the establishment.id for the closure record
          db.flush()

        try:
          closed_on = datetime.strptime(entry["closed_on"], "%Y-%m-%d")
        except (ValueError, TypeError):
          print(f"Skipping row due to invalid date: {entry.get('closed_on')}")
          continue

        reopened_on = None
        if entry.get("reopened_on"):
          try:
            reopened_on = datetime.strptime(entry["reopened_on"], "%Y-%m-%d")
          except ValueError:
            reopened_on = None

        closure_stmt = select(models.Closure).where(
          models.Closure.establishment_id == establishment.id,
          models.Closure.closed_on == closed_on
        )
        existing_closure = db.execute(closure_stmt).scalar_one_or_none()

        if not existing_closure:
          new_closure = models.Closure(
            establishment_id=establishment.id,
            closed_on=closed_on,
            reopened_on=reopened_on,
            reason=entry.get("reason"),
            result=entry.get("result"),
            created_at=timestamp,
            updated_at=timestamp
          )
          db.add(new_closure)

      db.commit()
      print(f"Successfully processed {len(scraped_data)} records.")