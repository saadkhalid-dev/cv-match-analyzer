from src.text_processor import normalize_text


def test_normalize_text_converts_to_lowercase():
    text = "Java PYTHON React"

    result = normalize_text(text)

    assert result == "java python react"


def test_normalize_text_removes_unnecessary_punctuation():
    text = "Java, Python! React?"

    result = normalize_text(text)

    assert result == "java python react"


def test_normalize_text_preserves_technology_characters():
    text = "C++ C# .NET Node.js"

    result = normalize_text(text)

    assert result == "c++ c# .net node.js"


def test_normalize_text_collapses_whitespace():
    text = "Java\n\n   Python     React"

    result = normalize_text(text)

    assert result == "java python react"