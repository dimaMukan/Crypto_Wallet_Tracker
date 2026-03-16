from sqlalchemy.orm import Session
from models import TrackedHolder

def get_top_holders(db:Session, limit: int = 10) -> list[TrackedHolder]:
    return db.query(TrackedHolder).filter(TrackedHolder.is_active == True).order_by(TrackedHolder.rank.asc()).limit(limit).all()


def upsert_top_holders(db: Session, rows: list[dict]) -> list[TrackedHolder]:
    seen = set()
    touched = []

    for row in rows[:10]:
        address = str(row["address"]).lower()
        rank = int(row["rank"])
        balance_raw = str(row["balance_raw"])
        seen.add(address)

        holder = db.query(TrackedHolder).filter(TrackedHolder.address == address).first()
        if holder:
            holder.rank = rank
            holder.balance_raw = balance_raw
            holder.is_active = True
            holder.source = "dune"
        else:
            holder = TrackedHolder(
                address=address,
                rank=rank,
                balance_raw=balance_raw,
                source="dune",
                is_active=True,
            )
            db.add(holder)
        touched.append(holder)
    if seen:
        db.query(TrackedHolder).filter(~TrackedHolder.address.in_(seen)).update(
            {"is_active": False},
            synchronize_session=False,
        )
    db.commit()
    for holder in touched:
        db.refresh(holder)
    return touched




