import pytest
from arkbrain import ArkBrain, ArkBrainError, ToolExecutionError, APIError

def test_arkbrain_requires_api_key(monkeypatch):
    monkeypatch.delenv('GOOGLE_GENAI_API_KEY', raising=False)
    with pytest.raises(ValueError, match="GOOGLE_GENAI_API_KEY"):
        ArkBrain()
