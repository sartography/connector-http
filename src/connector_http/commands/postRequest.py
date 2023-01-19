import requests

from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

class PostRequest:
    def __init__(self,
        url: str,
        headers: Optional[Dict[str, str]],
        basic_auth_username: Optional[str],
        basic_auth_password: Optional[str],
        data: Optional[Dict[str, Any]],
    ):
        self.url = url
        self.headers = headers or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password
        self.data = data

    def execute(self, config, task_data):
        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)

        try:
            response = requests.post(self.url, headers=self.headers, auth=auth, json=self.data)

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

