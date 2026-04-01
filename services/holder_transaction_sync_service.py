from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from core.etherscan_client import EtherscanClient, parse_usdc_transfer
from models.HolderTransactionEvent import HolderTransactionEvent
from models.TrackedHolder import TrackedHolder

@dataclass
class HolderSyncError:
    holder_id: int
    address: str
    message: str

@dataclass
class HolderSyncSummary:
    holders_processed: int = 0
    events_added: int = 0
    duplicates_skipped: int = 0
    errors: list[HolderSyncError] = field(default_factory=list)

'''dto to our model HolderTransactionEvent'''
def dto_to_event(holder_id: int, dto) -> HolderTransactionEvent:
    return HolderTransactionEvent(
        holder_id=holder_id,
        transaction_hash=dto.transaction_hash,
        direction=dto.direction,
        from_address=dto.from_address,
        to_address=dto.to_address,
        value_raw=dto.value_raw,
        token_symbol=dto.token_symbol,
        token_decimals=dto.token_decimals,
        contract_address=dto.contract_address,
        source="etherscan",
        block_number=dto.block_number,
        block_timestamp=dto.block_timestamp,
    )

'''getting all the tx for holder'''
def get_rows_for_holder(client, holder):
    # first sync, last 100tx
    if holder.last_scanned_block is None:
        rows = client.get_usdc_transfers(
            holder.address,
            page=1,
            offset=100,
            sort="desc",
        )
        return list(reversed(rows))

    # other syncs, get new transactions
    startblock = max(holder.last_scanned_block - 1, 0)
    page = 1
    page_size = 100
    all_rows = []

    while True:
        rows = client.get_usdc_transfers(
            holder.address,
            startblock=startblock,
            page=page,
            offset=page_size,
            sort="asc",
        )

        if not rows:
            break
        all_rows.extend(rows)

        if len(rows) < page_size: # exit from loop after all data saved
            break
        page += 1
    return all_rows

def get_latest_100_rows_for_holder(client: EtherscanClient,
                                   holder: TrackedHolder ) -> list[dict]:
    rows = client.get_usdc_transfers(
        holder.address,
        page=1,
        offset=100,
        sort="desc",
    )
    return list(reversed(rows))

def process_rows_for_holder(db: Session,
                            holder: TrackedHolder,
                            rows: list[dict],
                            summary: HolderSyncSummary,
                            max_block_seen: int,
                            seen_event_keys: set[tuple[int, str, str, str | None, str]]
                            ) -> int:
    for row in rows:
        dto = parse_usdc_transfer(row, holder.address)
        event_key = (
            holder.id,
            dto.transaction_hash,
            dto.from_address,
            dto.to_address,
            dto.value_raw,
        )

        if event_key in seen_event_keys:
            summary.duplicates_skipped += 1
            if dto.block_number > max_block_seen:
                max_block_seen = dto.block_number
            continue

        existing_event = (
            db.query(HolderTransactionEvent)
            .filter(
                HolderTransactionEvent.holder_id == holder.id,
                HolderTransactionEvent.transaction_hash == dto.transaction_hash,
                HolderTransactionEvent.from_address == dto.from_address,
                HolderTransactionEvent.to_address == dto.to_address,
                HolderTransactionEvent.value_raw == dto.value_raw,
            )
            .first()
        )

        if existing_event:
            seen_event_keys.add(event_key)
            summary.duplicates_skipped += 1
            if dto.block_number > max_block_seen:
                max_block_seen = dto.block_number
            continue

        event = dto_to_event(holder.id, dto)
        db.add(event)
        seen_event_keys.add(event_key)
        summary.events_added += 1

        if dto.block_number > max_block_seen:
            max_block_seen = dto.block_number
    return max_block_seen


def sync_one_holder_transactions(db: Session,
                                 holder: TrackedHolder,
                                 mode: str = "incremental",
                                 client: EtherscanClient | None = None
                                 ) -> HolderSyncSummary:
    summary = HolderSyncSummary()
    client = client or EtherscanClient()

    try:
        # rows = get_rows_for_holder(client, holder)
        max_block_seen = holder.last_scanned_block or 0
        seen_event_keys: set[tuple[int, str, str, str | None, str]] = set()
        if mode == "latest_100":
            rows = get_latest_100_rows_for_holder(client, holder)

            if not rows:
                holder.last_tx_sync_at = datetime.now(timezone.utc)
                db.commit()
                summary.holders_processed = 1
                return summary

            max_block_seen = process_rows_for_holder(
                db=db,
                holder=holder,
                rows=rows,
                summary=summary,
                max_block_seen=max_block_seen,
                seen_event_keys=seen_event_keys,
            )

        holder.last_scanned_block = max_block_seen
        holder.last_tx_sync_at = datetime.now(timezone.utc)
        db.commit()
        summary.holders_processed = 1
        return summary

    except Exception as e:
        db.rollback()
        summary.errors.append(
            HolderSyncError(
                holder_id=holder.id,
                address=holder.address,
                message=str(e),
            )
        )
        return summary

def sync_all_active_holder_transactions(db: Session) -> HolderSyncSummary:
    summary = HolderSyncSummary()
    client = EtherscanClient()

    holders = (
        db.query(TrackedHolder)
        .filter(TrackedHolder.is_active == True)
        .order_by(TrackedHolder.rank.asc())
        .all()
    )
    for holder in holders:
        holder_summary = sync_one_holder_transactions(db=db, holder=holder, client=client)
        summary.holders_processed += holder_summary.holders_processed
        summary.events_added += holder_summary.events_added
        summary.duplicates_skipped += holder_summary.duplicates_skipped
        summary.errors.extend(holder_summary.errors)

    return summary
