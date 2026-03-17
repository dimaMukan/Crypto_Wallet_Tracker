import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()
@dataclass(frozen=True)
class Settings:
    dune_api_key: str = os.getenv("DUNE_API_KEY", "")
    dune_top_holders_query_id: int = int(os.getenv("DUNE_TOP_HOLDERS_QUERY_ID", "0"))
    etherscan_api_key: str = os.getenv("ETHERSCAN_API_KEY", "")
    etherscan_base_url: str = os.getenv("ETHERSCAN_BASE_URL", "https://api.etherscan.io/v2/api")
    usdc_contract_address: str = os.getenv(
        "USDC_CONTRACT_ADDRESS",
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
    )
settings = Settings()