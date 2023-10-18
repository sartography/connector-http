from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from connector_http.http_request_base import HttpRequestBase


class GetRequestV2(ConnectorCommand, HttpRequestBase):
    def __init__(self,
        url: str,
        headers: dict[str, str] | None = None,
        params: dict[str, str] | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
        attempts: int | None = None,
    ):
        HttpRequestBase.__init__(self, url=url, headers=headers, params=params, basic_auth_username=basic_auth_username, basic_auth_password=basic_auth_password)
        if not isinstance(attempts, int) or attempts < 1 or attempts > 10:
            attempts = 1
        self.attempts = attempts

    def execute(self, _config: Any, _task_data: dict) -> ConnectorProxyResponseDict:
        return self.run_request(requests.get)
