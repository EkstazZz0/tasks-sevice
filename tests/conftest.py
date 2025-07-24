import pytest
from fastapi.testclient import TestClient

from app.main import app

def client():
    with TestClient(app=app) as c:
        yield c