from app.services.safety import classify


def test_normal_message_is_allowed():
    result = classify("Мы поссорились, хочу извиниться")
    assert result.blocked is False
    assert result.level == "low"


def test_direct_threat_is_blocked():
    result = classify("Я тебя убью")
    assert result.blocked is True
    assert result.level == "high"
