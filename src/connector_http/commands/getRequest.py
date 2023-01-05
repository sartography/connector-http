import requests

from typing import Dict
from typing import Optional
from typing import Tuple

class GetRequest:
    def __init__(self,
        url: str,
        headers: Optional[Dict[str, str]],
        params: Optional[Dict[str, str]],
        auth: Optional[Tuple[str, str]]
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.auth = tuple(auth) if auth is not None else None

    def execute(self, config, task_data):
        try:
            response = requests.get(self.url, self.params, headers=self.headers, auth=self.auth)

            return {
                "response": response.text,
                "status": response.status_code,
                "mimetype": "application/json",
            }
        except Exception as e:
            return {
                "response": f'{"error": {e}}',
                "status": 500,
                "mimetype": "application/json",
            }

