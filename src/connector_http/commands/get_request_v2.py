from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from connector_http.http_request_base import HttpRequestBase


class GetRequestV2(ConnectorCommand, HttpRequestBase):
    def __init__(self,
        attempts: int | None = None, **kwargs: Any
    ):
        HttpRequestBase.__init__(self, **kwargs)
        if not isinstance(attempts, int) or attempts < 1 or attempts > 10:
            attempts = 1
        self.attempts = attempts

    def execute(self, _config: Any, _task_data: dict) -> ConnectorProxyResponseDict:
        return self.run_request(requests.get)
