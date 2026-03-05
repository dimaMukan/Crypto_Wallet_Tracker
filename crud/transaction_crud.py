from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from models import Transaction as TransactionModel, Wallet as WalletModel
from sqlalchemy.exc import IntegrityError


def create_transaction(db: Session, transaction_create: TransactionCreate):
    wallet = db.query(WalletModel).filter(WalletModel.id == transaction_create.wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    existing_transaction = db.query(TransactionModel).filter(TransactionModel.hash == transaction_create.hash).first()
    if existing_transaction:
        return existing_transaction

    db_transaction = TransactionModel(**transaction_create.model_dump(exclude_unset=True))
    db.add(db_transaction)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        if "UNIQUE constraint failed: transaction.hash" in str(exc.orig):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Transaction with this hash already exists")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Database integrity error")
    db.refresh(db_transaction)
    return db_transaction


def get_transactions(db: Session):
    transactions = db.query(TransactionModel).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transactions


def get_transaction(db: Session, transaction_id: int):
    transaction = db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


def get_wallet_transactions(db: Session, wallet_id: int):
    wallet = db.query(WalletModel).filter(WalletModel.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")
    return wallet.transactions


def delete_transaction(db: Session, transaction_id: int):
    transaction = get_transaction(db, transaction_id)
    db.delete(transaction)
    db.commit()
    return transaction


def update_transaction(db: Session, transaction: TransactionModel, transaction_update: TransactionUpdate):
    if transaction_update.wallet_id is not None:
        wallet = db.query(WalletModel).filter(WalletModel.id == transaction_update.wallet_id).first()
        if not wallet:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Wallet not found")

    updated_transaction = transaction_update.model_dump(exclude_unset=True)
    for key, value in updated_transaction.items():
        setattr(transaction, key, value)
    db.commit()
    db.refresh(transaction)
    return transaction
