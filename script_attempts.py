from db.database import SessionLocal
from models.TrackedHolder import TrackedHolder
from core.etherscan_client import EtherscanClient, parse_usdc_transfer
from models.HolderTransactionEvent import HolderTransactionEvent


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


db = SessionLocal()

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
#here we need to add a cursor
    for holder in holders:
        print(f"\nProcessing holder: {holder.address}")

        rows = client.get_usdc_transfers(holder.address,startblock=..., offset=10)

        for row in rows:
            dto = parse_usdc_transfer(row, holder.address)
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
                continue

            event = dto_to_event(holder.id, dto)
            db.add(event)

            print("DTO:", dto)
            print("EVENT:", event.transaction_hash, event.value_raw, event.direction, event.token_symbol)
        db.commit()

finally:
    db.close()
