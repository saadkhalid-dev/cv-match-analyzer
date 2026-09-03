from src.requirement_analyzer import (
    analyze_job_requirements,
    extract_matching_sentences,
    extract_required_technical_skills,
    extract_soft_skills,
    split_into_sentences,
)


def test_extract_soft_skills_finds_common_skills():
    text = """
    Strong communication, teamwork and problem solving
    skills are required.
    """

    result = extract_soft_skills(text)

    assert result == {
        "communication",
        "teamwork",
        "problem solving",
    }


def test_extract_soft_skills_removes_duplicates():
    text = """
    Communication and verbal communication are important.
    """

    result = extract_soft_skills(text)

    assert result == {
        "communication",
    }


def test_split_into_sentences():
    text = (
        "Java experience required. "
        "Python would be beneficial. "
        "Strong teamwork is important."
    )

    result = split_into_sentences(text)

    assert result == [
        "Java experience required.",
        "Python would be beneficial.",
        "Strong teamwork is important.",
    ]


def test_split_into_sentences_handles_new_lines():
    text = """
    Java experience required
    Python would be beneficial
    Strong teamwork is important
    """

    result = split_into_sentences(text)

    assert result == [
        "Java experience required",
        "Python would be beneficial",
        "Strong teamwork is important",
    ]


def test_extract_matching_sentences():
    text = """
    Java experience is required.
    PostgreSQL would be beneficial.
    Strong teamwork is important.
    """

    result = extract_matching_sentences(
        text,
        ["beneficial"],
    )

    assert result == [
        "PostgreSQL would be beneficial."
    ]


def test_required_technical_skills_exclude_desirable_skills():
    text = """
    Java, Python and Git are required.
    PostgreSQL would be beneficial.
    """

    result = extract_required_technical_skills(
        text
    )

    assert result == {
        "java",
        "python",
        "git",
    }


def test_analyze_job_requirements_combines_categories():
    text = """
    We are looking for an undergraduate studying
    Software Engineering or Computer Science.

    Java and Python experience is required.

    Strong communication and teamwork skills are important.

    PostgreSQL would be beneficial.
    """

    result = analyze_job_requirements(text)

    assert "java" in result["technical_skills"]
    assert "python" in result["technical_skills"]
    assert "postgresql" in result["technical_skills"]

    assert result["required_technical_skills"] == {
        "java",
        "python",
    }

    assert "communication" in result["soft_skills"]
    assert "teamwork" in result["soft_skills"]

    assert result["education_required"] is True
    assert result["experience_required"] is True
    assert result["desirable_criteria_present"] is True


def test_job_title_is_not_treated_as_education_requirement():
    text = """
    Software Engineering Placement.

    Experience with Java and Python is required.
    """

    result = analyze_job_requirements(text)

    assert result["education_required"] is False
    assert result["education_evidence"] == []


def test_desirable_experience_is_not_treated_as_required():
    text = """
    Java knowledge is required.

    Previous project experience would be beneficial.
    """

    result = analyze_job_requirements(text)

    assert result["experience_required"] is False

    assert result["experience_evidence"] == []

    assert result["desirable_criteria_present"] is True

    assert result["desirable_evidence"] == [
        "Previous project experience would be beneficial."
    ]