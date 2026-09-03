from src.scoring import (
    calculate_category_score,
    calculate_match_score,
    calculate_weighted_average,
)


def test_calculate_category_score():
    results = {
        "strong": {"java", "python"},
        "partial": {"git"},
        "missing": {"postgresql"},
    }

    score = calculate_category_score(
        results
    )

    assert score == 62


def test_category_without_requirements_returns_none():
    results = {
        "strong": set(),
        "partial": set(),
        "missing": set(),
    }

    score = calculate_category_score(
        results
    )

    assert score is None


def test_weighted_average_ignores_empty_categories():
    score = calculate_weighted_average(
        [
            (50, 0.35),
            (None, 0.25),
        ]
    )

    assert score == 50


def test_weighted_average_returns_zero_when_no_categories_exist():
    score = calculate_weighted_average(
        [
            (None, 0.35),
            (None, 0.25),
        ]
    )

    assert score == 0


def test_calculate_match_score_with_all_categories():
    technical = {
        "strong": {"java"},
        "partial": {"python"},
        "missing": set(),
    }

    soft_skills = {
        "strong": {"teamwork"},
        "partial": set(),
        "missing": set(),
    }

    education = {
        "strong": {"education"},
        "partial": set(),
        "missing": set(),
    }

    experience = {
        "strong": set(),
        "partial": {"experience"},
        "missing": set(),
    }

    desirable = {
        "strong": {"postgresql"},
        "partial": set(),
        "missing": set(),
    }

    result = calculate_match_score(
        technical,
        soft_skills,
        education,
        experience,
        desirable,
    )

    assert result["technical_score"] == 75
    assert result["soft_skill_score"] == 100
    assert result["education_score"] == 100
    assert result["experience_score"] == 50
    assert result["desirable_score"] == 100
    assert result["overall_score"] == 79