import pytest
import time
from typing import Any


@pytest.fixture
def sleepless(monkeypatch: Any) -> None:

    def sleep(seconds: int) -> None:
        pass

    monkeypatch.setattr(time, 'sleep', sleep)
