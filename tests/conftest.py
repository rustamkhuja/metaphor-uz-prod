import os
from pathlib import Path

os.environ["APP_ENV"] = "test"
os.environ["LLM_PRIMARY_PROVIDER"] = "mock"
os.environ["DATABASE_URL"] = "sqlite:///./test_metaphor.db"
os.environ["FREE_DAILY_LIMIT"] = "100"


def pytest_sessionfinish(session, exitstatus):
    Path("test_metaphor.db").unlink(missing_ok=True)
