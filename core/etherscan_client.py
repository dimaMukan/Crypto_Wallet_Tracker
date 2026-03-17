import requests
from core.settings import settings
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime, timezone


@dataclass
class HolderTransferDTO:
    transaction_hash: str
    from_address: str
    to_address: str
    value_raw: str
    amount_token: Decimal
    token_symbol: str
    token_decimals: int
    contract_address: str
    block_number: int
    block_timestamp: datetime
    direction: str


class EtherscanClient:
    def __init__(self):
        self.base_url = settings.etherscan_base_url
        self.api_key = settings.etherscan_api_key

    def get_usdc_transfers(
        self,
        address: str,
        startblock: int = 0,
        endblock: int = 9999999999,
        page: int = 1,
        offset: int = 10,
        sort: str = "desc",
    ) -> list[dict]:
        params = {
            "chainid": 1,
            "module": "account",
            "action": "tokentx",
            "contractaddress": settings.usdc_contract_address,
            "address": address,
            "startblock": startblock,
            "endblock": endblock,
            "page": page,
            "offset": offset,
            "sort": sort,
            "apikey": self.api_key,
        }

        response = requests.get(self.base_url, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        status = payload.get("status")
        message = payload.get("message", "")
        result = payload.get("result", [])

        if status == "0" and message == "No transactions found":
            return []

        if not isinstance(result, list):
            raise RuntimeError(f"Unexpected Etherscan response: {payload}")

        return result


def parse_usdc_transfer(row: dict, holder_address: str) -> HolderTransferDTO:
    holder_address = holder_address.lower()
    from_address = row["from"].lower()
    to_address = row["to"].lower()
    value_raw = str(row["value"])
    token_decimals = int(row["tokenDecimal"])

    if from_address == holder_address and to_address == holder_address:
        direction = "SELF"
    elif to_address == holder_address:
        direction = "IN"
    else:
        direction = "OUT"

    amount_token = Decimal(value_raw) / (Decimal(10) ** token_decimals)

    return HolderTransferDTO(
        transaction_hash=row["hash"],
        from_address=from_address,
        to_address=to_address,
        value_raw=value_raw,
        amount_token=amount_token,
        token_symbol=row["tokenSymbol"],
        token_decimals=token_decimals,
        contract_address=row["contractAddress"].lower(),
        block_number=int(row["blockNumber"]),
        block_timestamp=datetime.fromtimestamp(int(row["timeStamp"]), tz=timezone.utc),
        direction=direction,
    )