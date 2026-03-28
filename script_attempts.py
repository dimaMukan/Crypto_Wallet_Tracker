from datetime import timezone, datetime
from db.database import SessionLocal
from models.TrackedHolder import TrackedHolder
from core.etherscan_client import EtherscanClient, parse_usdc_transfer
from models.HolderTransactionEvent import HolderTransactionEvent
from core.settings import settings
from services.holder_transaction_sync_service import sync_all_active_holder_transactions

db = SessionLocal()

print("ETHERSCAN_API_KEY loaded:", bool(settings.etherscan_api_key))
print("ETHERSCAN_API_KEY prefix:", settings.etherscan_api_key[:6] if settings.etherscan_api_key else "EMPTY")
try:
    summary = sync_all_active_holder_transactions(db)
    print(summary)
finally:
    db.close()
