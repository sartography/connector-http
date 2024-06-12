import json
from typing import Any
from unittest.mock import patch

from connector_http.commands.put_request_v2 import PutRequestV2


class TestPutRequestV2:
    expected_call_args = {
        "url": "http://example.com",
        "headers": {"Content-Type": "application/json"},
        "auth": None,
        "timeout": 300,
        "json": {},
    }

    def test_put_html_from_url(self) -> None:
        request = PutRequestV2(url="http://example.com")
        return_html = "<html>Hey</html>"
        with patch("requests.put") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.ok = True
            mock_request.return_value.text = return_html
            response = request.execute(None, {})
            assert mock_request.call_count == 1
            assert mock_request.call_args_list[0].kwargs == self.expected_call_args

        assert response["command_response"]["body"] == {"raw_response": return_html}
        assert response["command_response"]["http_status"] == 200
        assert response["command_response"]["mimetype"] == "application/json"
        assert response["error"] is None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0

    def test_put_json_from_url(self) -> None:
        request = PutRequestV2(url="http://example.com")
        return_json = {"hey": "we_return"}
        with patch("requests.put") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.ok = True
            mock_request.return_value.headers = {"Content-Type": "application/json"}
            mock_request.return_value.text = json.dumps(return_json)
            response = request.execute(None, {})
            assert mock_request.call_count == 1
            assert mock_request.call_args_list[0].kwargs == self.expected_call_args

        assert response is not None
        assert response["command_response"]["body"] == return_json
        assert response["command_response"]["http_status"] == 200
        assert response["command_response"]["mimetype"] == "application/json"
        assert response["error"] is None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0

    def test_put_can_handle_500(self, sleepless: Any) -> None:
        request = PutRequestV2(url="http://example.com")
        return_json = {"error": "we_did_error"}
        with patch("requests.put") as mock_request:
            mock_request.return_value.status_code = 500
            mock_request.return_value.headers = {"Content-Type": "application/json"}
            mock_request.return_value.text = json.dumps(return_json)
            response = request.execute(None, {})
            assert mock_request.call_count == 1
            assert mock_request.call_args_list[0].kwargs == self.expected_call_args

        assert response is not None
        assert response["command_response"]["body"] == return_json
        assert response["command_response"]["http_status"] == 500
        assert response["command_response"]["mimetype"] == "application/json"
        assert response["error"] is not None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0

    def test_put_does_not_change_content_type(self) -> None:
        request = PutRequestV2(url="http://example.com", headers={"Content-Type": "application/xml"})
        return_html = "<html>Hey</html>"
        with patch("requests.put") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.ok = True
            mock_request.return_value.text = return_html
            response = request.execute(None, {})
            assert mock_request.call_count == 1
            assert mock_request.call_args_list[0].kwargs == {
                **self.expected_call_args,
                **{"headers": {"Content-Type": "application/xml"}},
            }

        assert response["command_response"]["body"] == {"raw_response": return_html}
        assert response["command_response"]["http_status"] == 200
        assert response["command_response"]["mimetype"] == "application/json"
        assert response["error"] is None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0
