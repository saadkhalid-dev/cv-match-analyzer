def format_item(item: str) -> str:
    """
    Convert an internal requirement name into a
    cleaner label for user-facing output.
    """

    if item == "education":
        return "Education requirement"

    if item == "experience":
        return "Experience requirement"

    return item


def format_items(items: set[str]) -> list[str]:
    """
    Return requirement names in a predictable,
    readable order.
    """

    return [
        format_item(item)
        for item in sorted(items)
    ]


def build_category_summary(
    category_results: dict,
) -> dict:
    """
    Convert one matcher category into a
    user-facing summary.
    """

    return {
        "strong": format_items(
            category_results["strong"]
        ),
        "partial": format_items(
            category_results["partial"]
        ),
        "missing": format_items(
            category_results["missing"]
        ),
    }


def build_partial_suggestion(
    category: str,
    item: str,
) -> str:
    """
    Create a truthful suggestion for a requirement
    that is present in the CV but weakly supported.
    """

    label = format_item(item)

    if category == "technical":
        return (
            f"Strengthen evidence for {label} by describing "
            "where you used it, what you built, or what you "
            "achieved with it."
        )

    if category == "soft_skills":
        return (
            f"Support {label} with a specific example from "
            "coursework, employment, projects or teamwork."
        )

    if category == "education":
        return (
            "Make the relevant degree, subject and current "
            "study status clearer if they are already true."
        )

    if category == "experience":
        return (
            "Describe the relevant project or work experience "
            "more clearly, including your contribution and "
            "what you delivered."
        )

    if category == "desirable":
        return (
            f"The CV only partially supports this desirable "
            f"criterion: {label} Add clearer evidence if you "
            "genuinely have it."
        )

    return (
        f"Add clearer evidence for {label} if it is "
        "genuinely supported by your experience."
    )


def build_missing_suggestion(
    category: str,
    item: str,
) -> str:
    """
    Create a truthful suggestion for a requirement
    that currently has no recognised CV evidence.
    """

    label = format_item(item)

    if category == "technical":
        return (
            f"No evidence for {label} was found. Only add it "
            "to the CV if you genuinely have relevant "
            "knowledge or experience."
        )

    if category == "soft_skills":
        return (
            f"No evidence for {label} was found. If you have "
            "a genuine example, demonstrate it through an "
            "achievement or responsibility rather than simply "
            "listing the skill."
        )

    if category == "education":
        return (
            "The CV does not appear to show the requested "
            "education requirement. Do not claim a different "
            "qualification or subject."
        )

    if category == "experience":
        return (
            "The CV does not currently show the requested "
            "experience. Do not present project work as "
            "commercial experience unless that is accurate."
        )

    if category == "desirable":
        return (
            f"No evidence was found for this desirable "
            f"criterion: {label} It can be left out if you "
            "do not genuinely meet it."
        )

    return (
        f"No evidence for {label} was found. Only add "
        "information that is accurate."
    )


def build_suggestions(
    match_result: dict,
) -> list[str]:
    """
    Build deterministic CV-improvement suggestions
    from partial and missing requirements.

    Strong evidence produces no suggestion.
    """

    suggestions = []

    categories = [
        "technical",
        "soft_skills",
        "education",
        "experience",
        "desirable",
    ]

    for category in categories:
        results = match_result[category]

        for item in sorted(
            results["partial"]
        ):
            suggestions.append(
                build_partial_suggestion(
                    category,
                    item,
                )
            )

        for item in sorted(
            results["missing"]
        ):
            suggestions.append(
                build_missing_suggestion(
                    category,
                    item,
                )
            )

    return suggestions


def build_report_summary(
    match_result: dict,
) -> dict:
    """
    Build the structured summary used by the
    final report.
    """

    scores = match_result["scores"]

    return {
        "overall_score": scores[
            "overall_score"
        ],
        "categories": {
            "technical": build_category_summary(
                match_result["technical"]
            ),
            "soft_skills": build_category_summary(
                match_result["soft_skills"]
            ),
            "education": build_category_summary(
                match_result["education"]
            ),
            "experience": build_category_summary(
                match_result["experience"]
            ),
            "desirable": build_category_summary(
                match_result["desirable"]
            ),
        },
        "scores": {
            "technical": scores[
                "technical_score"
            ],
            "soft_skills": scores[
                "soft_skill_score"
            ],
            "education": scores[
                "education_score"
            ],
            "experience": scores[
                "experience_score"
            ],
            "desirable": scores[
                "desirable_score"
            ],
        },
        "suggestions": build_suggestions(
            match_result
        ),
    }


def format_score(
    score: int | None,
) -> str:
    """
    Format a category score for display.

    None means the job did not contain a recognised
    requirement for that category.
    """

    if score is None:
        return "Not assessed"

    return f"{score}%"


def render_item_group(
    title: str,
    items: list[str],
) -> list[str]:
    """
    Render one strong, partial or missing item group.
    """

    lines = [
        f"  {title}:"
    ]

    if not items:
        lines.append(
            "    None"
        )

        return lines

    for item in items:
        lines.append(
            f"    - {item}"
        )

    return lines


def render_category(
    title: str,
    category: dict,
    score: int | None,
) -> list[str]:
    """
    Render one report category.
    """

    lines = [
        title,
        f"Score: {format_score(score)}",
    ]

    lines.extend(
        render_item_group(
            "Strong evidence",
            category["strong"],
        )
    )

    lines.extend(
        render_item_group(
            "Partial evidence",
            category["partial"],
        )
    )

    lines.extend(
        render_item_group(
            "Missing evidence",
            category["missing"],
        )
    )

    return lines


def render_report(
    report_summary: dict,
) -> str:
    """
    Render the structured report summary as
    clean terminal-friendly text.
    """

    categories = report_summary[
        "categories"
    ]

    scores = report_summary[
        "scores"
    ]

    lines = [
        "CV MATCH ANALYSIS",
        "=" * 40,
        "",
        (
            "Overall Match Score: "
            f"{report_summary['overall_score']}%"
        ),
        "",
    ]

    category_details = [
        (
            "TECHNICAL SKILLS",
            "technical",
        ),
        (
            "SOFT SKILLS",
            "soft_skills",
        ),
        (
            "EDUCATION",
            "education",
        ),
        (
            "EXPERIENCE",
            "experience",
        ),
        (
            "DESIRABLE CRITERIA",
            "desirable",
        ),
    ]

    for title, key in category_details:
        lines.extend(
            render_category(
                title,
                categories[key],
                scores[key],
            )
        )

        lines.append("")

    lines.extend(
        [
            "IMPROVEMENT SUGGESTIONS",
            "-" * 40,
        ]
    )

    suggestions = report_summary[
        "suggestions"
    ]

    if suggestions:
        for number, suggestion in enumerate(
            suggestions,
            start=1,
        ):
            lines.append(
                f"{number}. {suggestion}"
            )
    else:
        lines.append(
            "No specific improvement suggestions were generated."
        )

    return "\n".join(lines)