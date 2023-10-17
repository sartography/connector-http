import json
import time
from collections.abc import Callable

import requests  # type: ignore
from spiffworkflow_connector_command.command_interface import CommandErrorDict
from spiffworkflow_connector_command.command_interface import CommandResponseDict
from spiffworkflow_connector_command.command_interface import ConnectorProxyResponseDict


class HttpRequestBase:
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
        self.attempts = 1

    def _create_error_from_exception(self, exception: Exception, http_response: requests.Response | None) -> CommandErrorDict:
        return self._create_error(
            error_code=exception.__class__.__name__, http_response=http_response, additional_message=str(exception)
        )

    def _create_error(
        self, error_code: str, http_response: requests.Response | None, additional_message: str = ""
    ) -> CommandErrorDict:
        raw_response = http_response.text if http_response is not None else None
        message = f"Received Error: {additional_message}. Raw http_response was: {raw_response}"
        error: CommandErrorDict = {"error_code": error_code, "message": message}
        return error

    def run_request(self, request_function: Callable) -> ConnectorProxyResponseDict:
        logs = []

        def log(msg: str) -> None:
            print(f"LOG: {msg}")
            logs.append(f"[{time.time()}] {msg}")

        log("Will execute")

        auth = None
        if self.basic_auth_username is not None and self.basic_auth_password is not None:
            auth = (self.basic_auth_username, self.basic_auth_password)
            log("Set auth")

        attempt = 1
        command_response: dict = {}
        error: CommandErrorDict | None = None
        status = 0
        mimetype = "application/json"
        http_response = None
        while attempt <= self.attempts:
            command_response = {}
            status = 0
            if attempt > 1:
                log("Sleeping before next attempt")
                time.sleep(1)

            log(f"Will attempt {attempt} of {self.attempts}")
            http_response = None

            try:
                log(f"Will call {self.url}")
                http_response = request_function(self.url, self.params, headers=self.headers, auth=auth, timeout=300)
                log(f"Did call {self.url}")

                log("Will parse http_response")
                status = http_response.status_code
            except Exception as e:
                log(f"Did catch exception: {e}")
                error = self._create_error_from_exception(exception=e, http_response=http_response)
                if status < 300:
                    status = 500
            finally:
                log(f"Did attempt {attempt} of {self.attempts}")

            # check for 500 level status
            if status // 100 != 5:
                break

            attempt += 1

        log("Did execute")

        if http_response is not None:
            command_response = {"raw_response": http_response.text}
            # this string can include modifiers like UTF-8, which is why it's not using ==
            if 'application/json' in http_response.headers.get('Content-Type', ''):
                try:
                    command_response = json.loads(http_response.text)
                except Exception as e:
                    error = self._create_error_from_exception(exception=e, http_response=http_response)
            log("Did parse http_response")

        if status >= 400 and error is None:
            error = self._create_error(error_code=f"HttpError{status}", http_response=http_response)

        return_response: CommandResponseDict = {
            "body": json.dumps(command_response),
            "mimetype": mimetype,
            "http_status": status,
        }
        result: ConnectorProxyResponseDict = {
            "command_response": return_response,
            "error": error,
            "command_response_version": 2,
            "spiff__logs": logs,
        }

        return result
