import json
import time
from typing import Any

import requests


class PostRequestV2:
    def __init__(self,
        url: str,
        headers: dict[str, str] | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
        data: dict[str, Any] | None = None,
    ):
        self.url = url
        self.headers = headers or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password
        self.data = data

    def execute(self, config, task_data):
        logs = []

        def log(msg):
            logs.append(f"[{time.time()}] {msg}")

        response = {}
        status = 0
        mimetype = "application/json"

        log("Will execute")

        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)
            log("basic auth has been set")

        try:
            log(f"Will call {self.url} with data {self.data}")
            api_response = requests.post(self.url, headers=self.headers, auth=auth, json=self.data, timeout=300)
            log(f"Did call {self.url}")

            log(f"Will parse response with status code {api_response.status_code}")
            status = api_response.status_code
            response = json.loads(api_response.text) if api_response.text else {}
            log("Did parse response")
        except Exception as e:
            log(f"Did catch exception: {e}")
            if len(response) == 0:
                response = f'{"error": {e}, "raw_response": {api_response.text}}',
            if status == 0:
                status = 500
        finally:
            log("Did execute")

        result = {
            "response": {
                "api_response": response,
                "spiff__logs": logs,
            },
            "status": status,
            "mimetype": mimetype,
        }

        return result
