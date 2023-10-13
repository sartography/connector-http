import json
from typing import Any
from unittest.mock import patch

from connector_http.commands.post_request_v2 import PostRequestV2


class TestPostRequestV2:
    def test_html_from_url(self) -> None:
        request = PostRequestV2(url="http://example.com")
        result = None
        return_html = "<html>Hey</html>"
        with patch("requests.post") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.ok = True
            mock_request.return_value.text = return_html
            result = request.execute(None, {})
            assert mock_request.call_count == 1
        assert result is not None
        assert result["status"] == 200
        assert result["mimetype"] == "application/json"

        response = result["response"]
        assert response is not None
        assert response["command_response"] == {"raw_response": return_html}
        assert response["error"] is None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0

    def test_json_from_url(self) -> None:
        request = PostRequestV2(url="http://example.com")
        result = None
        return_json = {"hey": "we_return"}
        with patch("requests.post") as mock_request:
            mock_request.return_value.status_code = 200
            mock_request.return_value.ok = True
            mock_request.return_value.headers = {"Content-Type": "application/json"}
            mock_request.return_value.text = json.dumps(return_json)
            result = request.execute(None, {})
            assert mock_request.call_count == 1
        assert result is not None
        assert result["status"] == 200
        assert result["mimetype"] == "application/json"

        response = result["response"]
        assert response is not None
        assert response["command_response"] == return_json
        assert response["error"] is None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0

    def test_can_handle_500(self, sleepless: Any) -> None:
        request = PostRequestV2(url="http://example.com")
        result = None
        return_json = {"error": "we_did_error"}
        with patch("requests.post") as mock_request:
            mock_request.return_value.status_code = 500
            mock_request.return_value.headers = {"Content-Type": "application/json"}
            mock_request.return_value.text = json.dumps(return_json)
            result = request.execute(None, {})
            assert mock_request.call_count == 1
        assert result is not None
        assert result["status"] == 500
        assert result["mimetype"] == "application/json"

        response = result["response"]
        assert response is not None
        assert response["command_response"] == return_json
        assert response["error"] is not None
        assert response["spiff__logs"] is not None
        assert len(response["spiff__logs"]) > 0
