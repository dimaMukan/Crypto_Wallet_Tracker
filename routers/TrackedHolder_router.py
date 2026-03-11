from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.settings import settings
from core.dune_client import DuneClient
from crud.TrackedHolder_crud import get_top_holders, upsert_top_holders
from db.database import get_db
from schemas.TrackedHolder_schema import TrackedHolderOut
from requests.exceptions import RequestException



router = APIRouter(prefix="/holders", tags=["holders"])

@router.get("/top", response_model=list[TrackedHolderOut])
def get_top_holders_router(limit: int = 10, db: Session = Depends(get_db)):
    return get_top_holders(db, limit)

@router.post("/sync-top", response_model=list[TrackedHolderOut])
def sync_top_holders_router(db: Session = Depends(get_db)):
    if not settings.dune_api_key or not settings.dune_top_holders_query_id:
        raise HTTPException(status_code=500, detail="Dune settings are missing")

    client = DuneClient(settings.dune_api_key)
    try:
        rows = client.fetch_rows(settings.dune_top_holders_query_id)
    except (RequestException, TimeoutError, RuntimeError, KeyError, ValueError) as e:
        raise HTTPException(status_code=502, detail=f"Dune API error: {e}")

    required = {"address", "rank", "balance_wei"}
    for row in rows[:10]:
        if not required.issubset(row.keys()):
            raise HTTPException(status_code=500, detail="Dune query must return address, rank, balance_wei")
    upsert_top_holders(db, rows)
    return get_top_holders(db, limit=10)