from src.matcher import (
    build_single_requirement_result,
    get_desirable_criterion_strength,
    get_education_evidence_strength,
    get_experience_evidence_strength,
    match_cv_to_job,
    match_desirable_criteria,
    match_soft_skills,
    match_technical_skill_evidence,
    match_technical_skills,
)


def test_match_technical_skills_excludes_desirable_skills():
    job_description = """
    Experience with Java, Python, PostgreSQL and Git is desirable.
    """

    cv_text = """
    Software Engineering student with experience using
    Java, Python and Git in university projects.
    """

    result = match_technical_skills(
        job_description,
        cv_text,
    )

    assert result["matched"] == set()
    assert result["missing"] == set()


def test_match_technical_skills_handles_no_matches():
    job_description = """
    Experience with Java and PostgreSQL is required.
    """

    cv_text = """
    Built projects using Python and React.
    """

    result = match_technical_skills(
        job_description,
        cv_text,
    )

    assert result["matched"] == set()

    assert result["missing"] == {
        "java",
        "postgresql",
    }


def test_match_technical_skill_evidence_separates_strength():
    job_description = """
    Experience with Java, Python and Git is required.
    """

    cv_text = """
    Built a Java application for a university project.

    Technical skills: Python.
    """

    result = match_technical_skill_evidence(
        job_description,
        cv_text,
    )

    assert result["strong"] == {
        "java",
    }

    assert result["partial"] == {
        "python",
    }

    assert result["missing"] == {
        "git",
    }


def test_match_soft_skills_separates_evidence_strength():
    job_description = """
    Strong teamwork, communication and problem solving
    skills are required.
    """

    cv_text = """
    Collaborated with other students on a Java group project.

    Communication is one of my key skills.
    """

    result = match_soft_skills(
        job_description,
        cv_text,
    )

    assert result["strong"] == {
        "teamwork",
    }

    assert result["partial"] == {
        "communication",
    }

    assert result["missing"] == {
        "problem solving",
    }


def test_education_evidence_is_strong_for_matching_degree():
    job_description = """
    Applicants should be studying Software Engineering
    or Computer Science at university.
    """

    cv_text = """
    Software Engineering student at university.
    """

    result = get_education_evidence_strength(
        job_description,
        cv_text,
    )

    assert result == "strong"


def test_education_evidence_is_partial_for_different_degree():
    job_description = """
    Applicants should be studying Computer Science
    at university.
    """

    cv_text = """
    Undergraduate university student studying Mathematics.
    """

    result = get_education_evidence_strength(
        job_description,
        cv_text,
    )

    assert result == "partial"


def test_education_returns_none_when_job_has_no_requirement():
    job_description = """
    Java and Python skills are required.
    """

    cv_text = """
    Software Engineering student.
    """

    result = get_education_evidence_strength(
        job_description,
        cv_text,
    )

    assert result is None


def test_general_experience_accepts_project_evidence():
    job_description = """
    Previous experience developing software is required.
    """

    cv_text = """
    Built several Java and Python university projects.
    """

    result = get_experience_evidence_strength(
        job_description,
        cv_text,
    )

    assert result == "strong"


def test_commercial_experience_is_partial_with_only_projects():
    job_description = """
    Previous commercial experience is required.
    """

    cv_text = """
    Built several university software projects.
    """

    result = get_experience_evidence_strength(
        job_description,
        cv_text,
    )

    assert result == "partial"


def test_commercial_experience_is_strong_with_work_evidence():
    job_description = """
    Previous industry experience is required.
    """

    cv_text = """
    Completed a software development internship
    and worked with a development team.
    """

    result = get_experience_evidence_strength(
        job_description,
        cv_text,
    )

    assert result == "strong"


def test_desirable_technical_criterion_can_be_strong():
    criterion = """
    Experience with PostgreSQL would be beneficial.
    """

    cv_text = """
    Built a university project using PostgreSQL.
    """

    result = get_desirable_criterion_strength(
        criterion,
        cv_text,
    )

    assert result == "strong"


def test_desirable_criterion_can_be_partial():
    criterion = """
    Experience with PostgreSQL and Git would be beneficial.
    """

    cv_text = """
    Built a university project using PostgreSQL.
    """

    result = get_desirable_criterion_strength(
        criterion,
        cv_text,
    )

    assert result == "partial"


def test_match_desirable_criteria():
    job_description = """
    Java is required.

    PostgreSQL would be beneficial.

    Previous project experience would be advantageous.
    """

    cv_text = """
    Built a Java and PostgreSQL university project.
    """

    result = match_desirable_criteria(
        job_description,
        cv_text,
    )

    assert len(result["strong"]) == 2
    assert result["partial"] == set()
    assert result["missing"] == set()


def test_build_single_requirement_result():
    result = build_single_requirement_result(
        "education",
        "strong",
    )

    assert result == {
        "strong": {"education"},
        "partial": set(),
        "missing": set(),
    }


def test_match_cv_to_job_combines_full_analysis():
    job_description = """
    Software Engineering Placement.

    Applicants should be studying Software Engineering
    or Computer Science at university.

    Experience developing software is required.

    Java, Python and Git are required.

    Strong communication and teamwork skills are important.

    PostgreSQL would be beneficial.
    """

    cv_text = """
    Software Engineering student at university.

    Built a Java application for a university project.

    Technical skills include Python.

    Collaborated with other students during group coursework.

    Communication is one of my strengths.

    Built another project using PostgreSQL.
    """

    result = match_cv_to_job(
        job_description,
        cv_text,
    )

    assert result["technical"]["strong"] == {
        "java",
    }

    assert result["technical"]["partial"] == {
        "python",
    }

    assert result["technical"]["missing"] == {
        "git",
    }

    assert result["education"]["strong"] == {
        "education",
    }

    assert result["experience"]["strong"] == {
        "experience",
    }

    assert result["desirable"]["strong"] == {
        "PostgreSQL would be beneficial.",
    }

    assert result["desirable"]["partial"] == set()
    assert result["desirable"]["missing"] == set()

    assert result["scores"]["technical_score"] == 50
    assert result["scores"]["soft_skill_score"] == 75
    assert result["scores"]["education_score"] == 100
    assert result["scores"]["experience_score"] == 100
    assert result["scores"]["desirable_score"] == 100
    assert result["scores"]["overall_score"] == 78