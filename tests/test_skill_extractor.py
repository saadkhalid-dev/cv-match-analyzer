from src.skill_extractor import extract_skills


def test_extract_skills_finds_multiple_technologies():
    text = """
    Software engineer with experience using Python, Java, React,
    PostgreSQL and Git.
    """

    result = extract_skills(text)

    assert result == {"python", "java", "react", "postgresql", "git"}


def test_extract_skills_is_case_insensitive():
    text = "PYTHON, Java and REACT"

    result = extract_skills(text)

    assert result == {"python", "java", "react"}


def test_extract_skills_removes_duplicates():
    text = "Python Python python PYTHON"

    result = extract_skills(text)

    assert result == {"python"}


def test_extract_skills_returns_empty_set_when_no_skills_found():
    text = "Strong communicator with excellent organisational ability."

    result = extract_skills(text)

    assert result == set()


def test_extract_skills_does_not_match_partial_words():
    text = "I enjoy programming and working with documentation."

    result = extract_skills(text)

    assert "c" not in result


def test_extract_skills_does_not_match_skills_inside_other_skills():
    text = "Experience using PostgreSQL databases."

    result = extract_skills(text)

    assert "postgresql" in result
    assert "postgres" not in result
    assert "sql" not in result


def test_extract_skills_handles_special_character_names():
    text = "Experience with C++, C#, Next.js and Node.js."

    result = extract_skills(text)

    assert result == {"c++", "c#", "next.js", "node.js"}