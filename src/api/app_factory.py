"""Application factory helper for tests."""

from src.api.main import app

def create_app(*args, **kwargs):
    return app
