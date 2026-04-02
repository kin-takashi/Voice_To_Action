"""
tests/test_parser.py
Unit test cho command parser — không cần mic hay email.
Chạy: python -m pytest tests/ -v
"""
import sys
sys.path.insert(0, "..")

from parser.command_parser import parse


def test_basic_command():
    result = parse("gửi 12345 cho gmail của tôi")
    assert result is not None
    assert result["action"] == "send_email"
    assert result["content"] == "12345"


def test_hello_world():
    result = parse("gửi hello world cho gmail của tôi")
    assert result is not None
    assert result["content"] == "hello world"


def test_without_cua_toi():
    result = parse("gửi abc cho gmail")
    assert result is not None
    assert result["content"] == "abc"


def test_with_toi_variant():
    result = parse("gửi test message tới gmail")
    assert result is not None
    assert result["content"] == "test message"


def test_empty_content_returns_none():
    result = parse("gửi cho gmail của tôi")
    assert result is None


def test_unrecognized_command():
    result = parse("hôm nay trời đẹp quá")
    assert result is None


def test_empty_string():
    result = parse("")
    assert result is None


def test_punctuation_normalized():
    result = parse("gửi hello, world! cho gmail của tôi.")
    assert result is not None
    assert "hello" in result["content"]


if __name__ == "__main__":
    tests = [
        test_basic_command,
        test_hello_world,
        test_without_cua_toi,
        test_with_toi_variant,
        test_empty_content_returns_none,
        test_unrecognized_command,
        test_empty_string,
        test_punctuation_normalized,
    ]
    passed = 0
    for t in tests:
        try:
            t()
            print(f"  ✅ {t.__name__}")
            passed += 1
        except AssertionError as e:
            print(f"  ❌ {t.__name__}: {e}")
    print(f"\nKết quả: {passed}/{len(tests)} passed")
