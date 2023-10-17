
from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import CommandResultDictV1
from spiffworkflow_connector_command.command_interface import ConnectorCommand


class GetRequest(ConnectorCommand):
    def __init__(self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
    ):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}
        self.basic_auth_username = basic_auth_username
        self.basic_auth_password = basic_auth_password

    # backend
    #   spiffworkflow-proxy
    #     GetRequest returns CommandResultDictV1
    def execute(self, _config: Any, _task_data: Any) -> CommandResultDictV1:
        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)

        try:
            response = requests.get(self.url, self.params, headers=self.headers, auth=auth, timeout=300)

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

