from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import ConnectorCommand
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict

from connector_http.http_request_base import HttpRequestBase


class PostRequestV2(ConnectorCommand, HttpRequestBase):
    def execute(self, _config: Any, _task_data: dict) -> ConnectorProxyResponseDict:
        return self.run_request(requests.post)
