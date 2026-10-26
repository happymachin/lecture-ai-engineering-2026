from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_token_usage(monkeypatch, capsys):
    usage = SimpleNamespace(prompt_token_count=123, response_token_count=45)
    response = SimpleNamespace(text="回答です", usage_metadata=usage)

    class FakeModels:
        def generate_content(self, model, contents):
            assert model == ask_module.MODEL
            assert contents == "テスト質問"
            return response

    class FakeClient:
        def __init__(self, api_key):
            assert api_key == "dummy-api-key"
            self.models = FakeModels()

    monkeypatch.setattr(ask_module.genai, "Client", FakeClient)
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "dummy-api-key")

    result = ask_module.ask("テスト質問")

    captured = capsys.readouterr()
    assert result == "回答です"
    assert "入力トークン数: 123" in captured.out
    assert "出力トークン数: 45" in captured.out
