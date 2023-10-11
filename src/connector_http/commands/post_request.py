from typing import Any

import requests


class PostRequest:
    def __init__(self,
        url: str,
        headers: dict[str, str] | None,
        basic_auth_username: str | None,
        basic_auth_password: str | None,
        data: dict[str, Any] | None,
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
            response = requests.post(self.url, headers=self.headers, auth=auth, json=self.data, timeout=300)

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

