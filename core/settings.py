import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
@dataclass(frozen=True)
class Settings:
    dune_api_key: str = os.getenv("DUNE_API_KEY", "")
    dune_top_holders_query_id: int = int(os.getenv("DUNE_TOP_HOLDERS_QUERY_ID", "0"))

settings = Settings()