import json
import time

import requests

from typing import Dict
from typing import Optional
from typing import Tuple

class GetRequestV2:
    def __init__(self,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, str]] = None,
        basic_auth_username: Optional[str] = None,
        basic_auth_password: Optional[str] = None,
        attempts: Optional[int] = None,
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password

        if not isinstance(attempts, int) or attempts < 1 or attempts > 10:
            attempts = 1
        
        self.attempts = attempts

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
            log("Set auth")

        attempt = 1

        while attempt <= self.attempts:
            status = None
            if attempt > 1:
                log("Sleeping before next attempt")
                time.sleep(1)
            
            log(f"Will attempt {attempt} of {self.attempts}")
            api_response = None
            
            try:
                log(f"Will call {self.url}")
                api_response = requests.get(self.url, self.params, headers=self.headers, auth=auth)
                log(f"Did call {self.url}")
                
                log(f"Will parse response")
                status = api_response.status_code
                response = json.loads(api_response.text)
                log(f"Did parse response")
            except Exception as e:
                log(f"Did catch exception: {e}")
                response = f'{"error": {e}}',
                if status is None:
                    status = 500
            finally:
                log(f"Did attempt {attempt} of {self.attempts}")

            if status // 100 != 5:
                break

            attempt += 1

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
