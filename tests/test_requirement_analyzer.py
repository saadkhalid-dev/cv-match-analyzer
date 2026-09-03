from src.requirement_analyzer import (
    analyze_job_requirements,
    extract_matching_sentences,
    extract_soft_skills,
    split_into_sentences,
)


def test_extract_soft_skills_finds_common_requirements():
    text = """
    We are looking for someone with excellent communication skills,
    strong problem solving ability and experience working in a team.
    """

    result = extract_soft_skills(text)

    assert result == {
        "communication",
        "problem solving",
        "teamwork",
    }


def test_extract_soft_skills_avoids_duplicates():
    text = """
    You should be a team player who enjoys collaboration and
    working in a team.
    """

    result = extract_soft_skills(text)

    assert result == {"teamwork"}


def test_split_into_sentences():
    text = (
        "Applicants should be studying towards a degree. "
        "Experience with Python would be beneficial. "
        "Strong communication skills are required."
    )

    result = split_into_sentences(text)

    assert result == [
        "Applicants should be studying towards a degree.",
        "Experience with Python would be beneficial.",
        "Strong communication skills are required.",
    ]


def test_extract_matching_sentences():
    text = (
        "Applicants should be studying towards a degree. "
        "Strong communication skills are required. "
        "Previous project experience would be beneficial."
    )

    result = extract_matching_sentences(
        text,
        ["experience"],
    )

    assert result == [
        "Previous project experience would be beneficial."
    ]


def test_analyze_job_requirements_combines_categories():
    text = """
    Technology Placement Student.

    Applicants should be studying towards a Software Engineering
    or Computer Science degree.

    Experience with Java, Python, Git and PostgreSQL would be beneficial.

    You should have strong communication and problem solving skills
    and enjoy collaborating with other team members.
    """

    result = analyze_job_requirements(text)

    assert result["technical_skills"] == {
        "java",
        "python",
        "git",
        "postgresql",
    }

    assert result["soft_skills"] == {
        "communication",
        "problem solving",
        "teamwork",
    }

    assert result["education_required"] is True
    assert result["experience_required"] is True
    assert result["desirable_criteria_present"] is True

    assert len(result["education_evidence"]) == 1
    assert len(result["experience_evidence"]) == 1
    assert len(result["desirable_evidence"]) == 1


def test_analyze_job_requirements_handles_minimal_job_description():
    text = """
    Entry-level technology role.

    We are looking for someone who is eager to learn.
    """

    result = analyze_job_requirements(text)

    assert result["technical_skills"] == set()
    assert result["soft_skills"] == {"adaptability"}
    assert result["education_required"] is False
    assert result["experience_required"] is False

    assert result["education_evidence"] == []
    assert result["experience_evidence"] == []