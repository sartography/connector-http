from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from connector_http.http_request_base import HttpRequestBase


class PutRequestV2(ConnectorCommand, HttpRequestBase):
    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        data: dict[str, str] | None = None,
        basic_auth_username: str | None = None,
        basic_auth_password: str | None = None,
    ):
        HttpRequestBase.__init__(
            self, url=url, headers=headers, basic_auth_username=basic_auth_username, basic_auth_password=basic_auth_password
        )

        self.data = data or {}

    def execute(self, _config: Any, _task_data: dict) -> ConnectorProxyResponseDict:
        return self.run_request(requests.put)
