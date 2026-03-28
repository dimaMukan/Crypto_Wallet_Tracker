from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.settings import settings
from core.dune_client import DuneClient
from crud.TrackedHolder_crud import get_top_holders, upsert_top_holders, get_holder_events, get_holder_by_id
from db.database import get_db
from schemas.TrackedHolder_schema import TrackedHolderOut
from schemas.HolderTransactionEvent_schema import HolderTransactionEventOut
from requests.exceptions import RequestException
from services.holder_transaction_sync_service import sync_all_active_holder_transactions, sync_one_holder_transactions
from schemas.HolderTransactionSync_schema import HolderSyncErrorOut, HolderTransactionSyncSummaryOut



router = APIRouter(prefix="/holders", tags=["holders"])

def to_sync_summary_out(summary) -> HolderTransactionSyncSummaryOut:
    return HolderTransactionSyncSummaryOut(
        holders_processed=summary.holders_processed,
        events_added=summary.events_added,
        duplicates_skipped=summary.duplicates_skipped,
        errors=[
            HolderSyncErrorOut(
                holder_id=error.holder_id,
                address=error.address,
                message=error.message,
            )
            for error in summary.errors
        ],
    )

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

    required = {"address", "rank", "balance_raw"}
    for row in rows[:10]:
        if not required.issubset(row.keys()):
            raise HTTPException(status_code=500, detail="Dune query must return address, rank, balance_raw")
    upsert_top_holders(db, rows)
    return get_top_holders(db, limit=10)


@router.get("/{holder_id}", response_model=TrackedHolderOut)
def get_holder_router(holder_id: int, db: Session = Depends(get_db)):
    holder = get_holder_by_id(db, holder_id)
    if not holder:
        raise HTTPException(status_code=404, detail="Holder not found")
    return holder


@router.get("/{holder_id}/events", response_model=list[HolderTransactionEventOut])
def get_holder_events_router(holder_id: int, limit: int | None = None, db: Session = Depends(get_db)):
    holder = get_holder_by_id(db, holder_id)
    if not holder:
        raise HTTPException(status_code=404, detail="Holder not found")
    return get_holder_events(db, holder_id=holder_id, limit=limit)

@router.post("/sync-transactions", response_model=HolderTransactionSyncSummaryOut)
def sync_all_holder_transactions_router(db: Session = Depends(get_db)):
    summary = sync_all_active_holder_transactions(db)
    return to_sync_summary_out(summary)

@router.post("/{holder_id}/sync-transactions", response_model=HolderTransactionSyncSummaryOut)
def sync_one_holder_transactions_router(holder_id: int, db: Session = Depends(get_db)):
    holder = get_holder_by_id(db, holder_id)
    if not holder:
        raise HTTPException(status_code=404, detail="Holder not found")
    summary = sync_one_holder_transactions(db, holder)
    return to_sync_summary_out(summary)
