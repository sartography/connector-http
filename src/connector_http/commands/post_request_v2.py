from typing import Any

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import CommandResultDictV2
from spiffworkflow_connector_command.command_interface import ConnectorCommand

from connector_http.http_request_base import HttpRequestBase


class PostRequestV2(ConnectorCommand, HttpRequestBase):
    def execute(self, _config: Any, _task_data: dict) -> CommandResultDictV2:
        return self.run_request(requests.post)
