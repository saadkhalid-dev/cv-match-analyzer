from src.evidence_analyzer import (
    get_education_strength_for_requirement,
    get_experience_strength_for_requirement,
    get_soft_skill_evidence_strength,
    get_technical_skill_evidence_strength,
)


def test_technical_evidence_is_strong_with_project_context():
    cv_text = """
    Built a Java application for a university project.
    """

    result = get_technical_skill_evidence_strength(
        "java",
        cv_text,
    )

    assert result == "strong"


def test_technical_evidence_is_strong_with_usage_context():
    cv_text = """
    Used Python to process application data.
    """

    result = get_technical_skill_evidence_strength(
        "python",
        cv_text,
    )

    assert result == "strong"


def test_technical_evidence_is_partial_when_only_listed():
    cv_text = """
    Technical skills include Java, Python and Git.
    """

    result = get_technical_skill_evidence_strength(
        "java",
        cv_text,
    )

    assert result == "partial"


def test_listed_skill_does_not_borrow_evidence_from_later_project():
    cv_text = """
    SQL
    PostgreSQL

    PROJECT EXPERIENCE

    Built a Java application for a university project.
    """

    sql_result = get_technical_skill_evidence_strength(
        "sql",
        cv_text,
    )

    postgresql_result = get_technical_skill_evidence_strength(
        "postgresql",
        cv_text,
    )

    assert sql_result == "partial"
    assert postgresql_result == "partial"


def test_technical_evidence_is_missing_when_skill_not_present():
    cv_text = """
    Built several Python applications.
    """

    result = get_technical_skill_evidence_strength(
        "java",
        cv_text,
    )

    assert result == "missing"


def test_soft_skill_evidence_is_strong_with_practical_example():
    cv_text = """
    Collaborated with other students during
    group coursework.
    """

    result = get_soft_skill_evidence_strength(
        "teamwork",
        cv_text,
    )

    assert result == "strong"


def test_soft_skill_evidence_is_partial_when_only_mentioned():
    cv_text = """
    My strengths include teamwork and communication.
    """

    result = get_soft_skill_evidence_strength(
        "teamwork",
        cv_text,
    )

    assert result == "partial"


def test_soft_skill_evidence_is_missing_when_not_present():
    cv_text = """
    Built several personal Python applications.
    """

    result = get_soft_skill_evidence_strength(
        "teamwork",
        cv_text,
    )

    assert result == "missing"


def test_education_is_strong_for_matching_subject():
    requirement = """
    Applicants should be studying Software Engineering
    or Computer Science at university.
    """

    cv_text = """
    Software Engineering student at university.
    """

    result = get_education_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "strong"


def test_education_is_partial_for_different_subject():
    requirement = """
    Applicants should be studying Computer Science
    at university.
    """

    cv_text = """
    Undergraduate university student studying Mathematics.
    """

    result = get_education_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "partial"


def test_education_is_missing_without_education_evidence():
    requirement = """
    Applicants should be studying Computer Science
    at university.
    """

    cv_text = """
    Built several Python applications.
    """

    result = get_education_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "missing"


def test_general_experience_is_strong_with_project_work():
    requirement = """
    Experience developing software is required.
    """

    cv_text = """
    Built several Java and Python university projects.
    """

    result = get_experience_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "strong"


def test_commercial_experience_is_partial_with_only_projects():
    requirement = """
    Commercial experience is required.
    """

    cv_text = """
    Built several university software projects.
    """

    result = get_experience_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "partial"


def test_placement_interest_does_not_count_as_commercial_experience():
    requirement = """
    Commercial software development experience is required.
    """

    cv_text = """
    Software Engineering student interested in placement
    opportunities.

    Built several university software projects.
    """

    result = get_experience_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "partial"


def test_commercial_experience_is_strong_with_internship():
    requirement = """
    Previous industry experience is required.
    """

    cv_text = """
    Completed a software development internship.
    """

    result = get_experience_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "strong"


def test_experience_is_missing_without_relevant_evidence():
    requirement = """
    Experience developing software is required.
    """

    cv_text = """
    Technical skills include Java and Python.
    """

    result = get_experience_strength_for_requirement(
        requirement,
        cv_text,
    )

    assert result == "missing"