import json
import requests
import time

from typing import Any
from typing import Dict
from typing import Optional
from typing import Tuple

class PostRequestV2:
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
        logs = []

        def log(msg):
            logs.append(f"[{time.time()}] {msg}")

        response = {}
        status = 0
        mimetype = "application/json"

        log(f"Will execute")

        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)

        try:
            log(f"Will call {self.url}")
            api_response = requests.post(self.url, headers=self.headers, auth=auth, json=self.data)
            log(f"Did call {self.url}")
                
            log(f"Will parse response")
            status = api_response.status_code
            response = json.loads(api_response.text)
            log(f"Did parse response")
        except Exception as e:
            log(f"Did catch exception: {e}")
            if response is None:
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
