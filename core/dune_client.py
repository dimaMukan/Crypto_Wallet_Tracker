import time
import requests

class DuneClient:
    BASE_URL = "https://api.dune.com/api/v1"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "X-Dune-API-Key": api_key,
            "Content-Type": "application/json",
        }

    def execute_query(self, query_id: int) -> str:
        url = f"{self.BASE_URL}/query/{query_id}/execute"
        resp = requests.post(url, headers=self.headers, json={"performance": "medium"}, timeout=30)
        resp.raise_for_status()
        return resp.json()["execution_id"]


    def wait_until_done(self, execution_id: str, timeout_sec: int = 120) -> None:
        url = f"{self.BASE_URL}/execution/{execution_id}/status"
        started = time.time()
        while True:
            resp = requests.get(url, headers=self.headers, timeout=30)
            resp.raise_for_status()
            state = resp.json().get("state", "")
            if state in {"QUERY_STATE_COMPLETED", "QUERY_STATE_COMPLETED_PARTIAL"}:
                return
            if state in {"QUERY_STATE_FAILED", "QUERY_STATE_CANCELED", "QUERY_STATE_EXPIRED"}:
                raise RuntimeError(f"Dune execution failed with state={state}")
            if time.time() - started > timeout_sec:
                raise TimeoutError("Dune query timeout")
            time.sleep(2)


    def get_results(self, execution_id: str) -> list[dict]:
        url = f"{self.BASE_URL}/execution/{execution_id}/results"
        resp = requests.get(url, headers=self.headers, params={"limit": 100}, timeout=30)
        resp.raise_for_status()
        return resp.json().get("result", {}).get("rows", [])


    def fetch_rows(self, query_id: int) -> list[dict]:
        execution_id = self.execute_query(query_id)
        self.wait_until_done(execution_id)
        return self.get_results(execution_id)

