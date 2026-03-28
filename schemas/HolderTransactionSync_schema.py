from pydantic import BaseModel

class HolderSyncErrorOut(BaseModel):
    holder_id: int
    address: str
    message: str

class HolderTransactionSyncSummaryOut(BaseModel):
    holders_processed: int
    events_added: int
    duplicates_skipped: int
    errors: list[HolderSyncErrorOut]