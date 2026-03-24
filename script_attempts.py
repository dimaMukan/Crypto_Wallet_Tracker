from datetime import timezone, datetime
from db.database import SessionLocal
from models.TrackedHolder import TrackedHolder
from core.etherscan_client import EtherscanClient, parse_usdc_transfer
from models.HolderTransactionEvent import HolderTransactionEvent
from core.settings import settings


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



db = SessionLocal()

print("ETHERSCAN_API_KEY loaded:", bool(settings.etherscan_api_key))
print("ETHERSCAN_API_KEY prefix:", settings.etherscan_api_key[:6] if settings.etherscan_api_key else "EMPTY")
try:
    holders = (
        db.query(TrackedHolder)
        .filter(TrackedHolder.is_active == True)
        .order_by(TrackedHolder.rank.asc())
        .all()
    )

    if not holders:
        raise RuntimeError("No active tracked holder found")

    print("Holders count:", len(holders))

    client = EtherscanClient()

    for holder in holders:
        print(f"\nProcessing holder: {holder.address}")
        rows = get_rows_for_holder(client, holder)
        max_block_seen = holder.last_scanned_block or 0
        seen_event_keys = set()

        if not rows:
            holder.last_tx_sync_at = datetime.now(timezone.utc)
            db.commit()
            continue

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
                if dto.block_number > max_block_seen:
                    max_block_seen = dto.block_number
                continue

            event = dto_to_event(holder.id, dto)
            db.add(event)
            seen_event_keys.add(event_key)

            if dto.block_number > max_block_seen:
                max_block_seen = dto.block_number

            print("DTO:", dto)
            print("EVENT:", event.transaction_hash, event.value_raw, event.direction, event.token_symbol)

        holder.last_scanned_block = max_block_seen
        holder.last_tx_sync_at = datetime.now(timezone.utc)
        db.commit()

finally:
    db.close()
