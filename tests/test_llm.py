from app.services.llm import LLMRouter


def test_parse_json_with_fence():
    parsed = LLMRouter.parse_json('```json\n{"variants": []}\n```')
    assert parsed == {"variants": []}


def test_extract_responses_output():
    data = {"output": [{"type": "message", "content": [{"type": "output_text", "text": "ok"}]}]}
    assert LLMRouter._extract_output_text(data) == "ok"
