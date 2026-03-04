from schemas.transaction_schema import TransactionCreate, Transaction, TransactionUpdate
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from db.database import get_db
from crud.transaction_crud import get_transaction, create_transaction, get_transactions, delete_transaction, \
    update_transaction

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/", response_model=list[Transaction])
def get_transactions_router(db: Session = Depends(get_db)):
    db_transaction = get_transactions(db)
    return db_transaction


@router.get("/{transaction_id}", response_model=Transaction)
def get_by_id_transaction_router(transaction_id: int, db: Session = Depends(get_db)):
    transaction = get_transaction(db, transaction_id)
    return transaction


@router.patch("/{transaction_id}", response_model=Transaction)
def patch_transaction_router(transaction_id: int, transaction_update: TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = get_transaction(db, transaction_id)
    updated_transaction = update_transaction(db, db_transaction, transaction_update)
    return updated_transaction


@router.delete("/{transaction_id}", response_model=Transaction)
def delete_transaction_router(transaction_id: int, db: Session = Depends(get_db)):
    return delete_transaction(db, transaction_id)


@router.post("/", response_model=Transaction)
def create_transaction_router(transaction_create: TransactionCreate, db: Session = Depends(get_db)):
    return create_transaction(db, transaction_create)
