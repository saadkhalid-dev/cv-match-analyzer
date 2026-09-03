from src.report import (
    build_category_summary,
    build_missing_suggestion,
    build_partial_suggestion,
    build_report_summary,
    build_suggestions,
    format_item,
    format_items,
    format_score,
    render_category,
    render_report,
)


def test_format_item_converts_internal_education_name():
    assert format_item(
        "education"
    ) == "Education requirement"


def test_format_item_keeps_normal_skill_name():
    assert format_item(
        "java"
    ) == "java"


def test_format_items_returns_sorted_labels():
    result = format_items(
        {
            "python",
            "java",
            "git",
        }
    )

    assert result == [
        "git",
        "java",
        "python",
    ]


def test_build_category_summary():
    results = {
        "strong": {
            "java",
        },
        "partial": {
            "python",
        },
        "missing": {
            "git",
        },
    }

    summary = build_category_summary(
        results
    )

    assert summary == {
        "strong": [
            "java",
        ],
        "partial": [
            "python",
        ],
        "missing": [
            "git",
        ],
    }


def test_partial_technical_suggestion_encourages_evidence():
    result = build_partial_suggestion(
        "technical",
        "python",
    )

    assert "python" in result
    assert "where you used it" in result


def test_missing_technical_suggestion_does_not_encourage_fabrication():
    result = build_missing_suggestion(
        "technical",
        "git",
    )

    assert "git" in result
    assert "genuinely" in result


def test_missing_experience_suggestion_distinguishes_projects_from_commercial_work():
    result = build_missing_suggestion(
        "experience",
        "experience",
    )

    assert "commercial experience" in result


def test_build_suggestions_ignores_strong_evidence():
    match_result = {
        "technical": {
            "strong": {
                "java",
            },
            "partial": {
                "python",
            },
            "missing": {
                "git",
            },
        },
        "soft_skills": {
            "strong": {
                "teamwork",
            },
            "partial": set(),
            "missing": set(),
        },
        "education": {
            "strong": {
                "education",
            },
            "partial": set(),
            "missing": set(),
        },
        "experience": {
            "strong": {
                "experience",
            },
            "partial": set(),
            "missing": set(),
        },
        "desirable": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
    }

    suggestions = build_suggestions(
        match_result
    )

    assert len(suggestions) == 2

    assert any(
        "python" in suggestion
        for suggestion in suggestions
    )

    assert any(
        "git" in suggestion
        for suggestion in suggestions
    )

    assert all(
        "java" not in suggestion
        for suggestion in suggestions
    )


def test_build_suggestions_has_predictable_order():
    match_result = {
        "technical": {
            "strong": set(),
            "partial": {
                "python",
                "java",
            },
            "missing": {
                "git",
            },
        },
        "soft_skills": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
        "education": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
        "experience": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
        "desirable": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
    }

    suggestions = build_suggestions(
        match_result
    )

    assert "java" in suggestions[0]
    assert "python" in suggestions[1]
    assert "git" in suggestions[2]


def test_format_score_formats_integer():
    assert format_score(
        78
    ) == "78%"


def test_format_score_handles_unassessed_category():
    assert format_score(
        None
    ) == "Not assessed"


def test_render_category_contains_evidence_groups():
    category = {
        "strong": [
            "java",
        ],
        "partial": [
            "python",
        ],
        "missing": [
            "git",
        ],
    }

    result = render_category(
        "TECHNICAL SKILLS",
        category,
        50,
    )

    rendered = "\n".join(
        result
    )

    assert "TECHNICAL SKILLS" in rendered
    assert "Score: 50%" in rendered
    assert "Strong evidence" in rendered
    assert "java" in rendered
    assert "Partial evidence" in rendered
    assert "python" in rendered
    assert "Missing evidence" in rendered
    assert "git" in rendered


def test_build_report_summary():
    match_result = {
        "technical": {
            "strong": {
                "java",
            },
            "partial": {
                "python",
            },
            "missing": {
                "git",
            },
        },
        "soft_skills": {
            "strong": {
                "teamwork",
            },
            "partial": {
                "communication",
            },
            "missing": set(),
        },
        "education": {
            "strong": {
                "education",
            },
            "partial": set(),
            "missing": set(),
        },
        "experience": {
            "strong": {
                "experience",
            },
            "partial": set(),
            "missing": set(),
        },
        "desirable": {
            "strong": {
                "PostgreSQL would be beneficial.",
            },
            "partial": set(),
            "missing": set(),
        },
        "scores": {
            "technical_score": 50,
            "soft_skill_score": 75,
            "education_score": 100,
            "experience_score": 100,
            "desirable_score": 100,
            "overall_score": 78,
        },
    }

    report = build_report_summary(
        match_result
    )

    assert report["overall_score"] == 78

    assert report["categories"][
        "technical"
    ] == {
        "strong": [
            "java",
        ],
        "partial": [
            "python",
        ],
        "missing": [
            "git",
        ],
    }

    assert report["categories"][
        "education"
    ]["strong"] == [
        "Education requirement",
    ]

    assert report["scores"][
        "technical"
    ] == 50

    assert report["scores"][
        "soft_skills"
    ] == 75

    assert len(
        report["suggestions"]
    ) == 3


def test_render_report_contains_main_sections():
    match_result = {
        "technical": {
            "strong": {
                "java",
            },
            "partial": {
                "python",
            },
            "missing": {
                "git",
            },
        },
        "soft_skills": {
            "strong": {
                "teamwork",
            },
            "partial": set(),
            "missing": set(),
        },
        "education": {
            "strong": {
                "education",
            },
            "partial": set(),
            "missing": set(),
        },
        "experience": {
            "strong": {
                "experience",
            },
            "partial": set(),
            "missing": set(),
        },
        "desirable": {
            "strong": set(),
            "partial": set(),
            "missing": set(),
        },
        "scores": {
            "technical_score": 50,
            "soft_skill_score": 100,
            "education_score": 100,
            "experience_score": 100,
            "desirable_score": None,
            "overall_score": 75,
        },
    }

    summary = build_report_summary(
        match_result
    )

    result = render_report(
        summary
    )

    assert "CV MATCH ANALYSIS" in result
    assert "Overall Match Score: 75%" in result
    assert "TECHNICAL SKILLS" in result
    assert "SOFT SKILLS" in result
    assert "EDUCATION" in result
    assert "EXPERIENCE" in result
    assert "DESIRABLE CRITERIA" in result
    assert "Score: Not assessed" in result
    assert "IMPROVEMENT SUGGESTIONS" in result
    assert "python" in result
    assert "git" in result