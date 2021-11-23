import os
import subprocess
import sys
from typing import List

import pytest


@pytest.fixture
def test_dir():
    return os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def flow_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))


class CliRunner:
    @staticmethod
    def run(cmd: List[str], flow_dir: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, os.path.join(flow_dir, cmd[0]), *cmd[1:]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
        )


@pytest.fixture
def runner():
    return CliRunner
