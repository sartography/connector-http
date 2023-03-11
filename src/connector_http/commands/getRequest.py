import requests

from typing import Dict
from typing import Optional
from typing import Tuple

class GetRequest:
    def __init__(self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        basic_auth_username: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password

    def execute(self, config, task_data):
        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)

        try:
            response = requests.get(self.url, self.params, headers=self.headers, auth=auth)

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

