def calculate_category_score(
    results: dict,
) -> int | None:
    """
    Strong evidence receives full credit.
    Partial evidence receives half credit.
    Missing evidence receives no credit.
    """

    strong_count = len(
        results["strong"]
    )

    partial_count = len(
        results["partial"]
    )

    missing_count = len(
        results["missing"]
    )

    total_requirements = (
        strong_count
        + partial_count
        + missing_count
    )

    if total_requirements == 0:
        return None

    earned_points = (
        strong_count
        + (partial_count * 0.5)
    )

    return round(
        (
            earned_points
            / total_requirements
        )
        * 100
    )


def calculate_weighted_average(
    categories: list[
        tuple[int | None, float]
    ],
) -> int:
    """
    Calculate a weighted average using only
    categories relevant to the job.
    """

    weighted_total = 0
    active_weight = 0

    for score, weight in categories:
        if score is None:
            continue

        weighted_total += (
            score * weight
        )

        active_weight += weight

    if active_weight == 0:
        return 0

    return round(
        weighted_total
        / active_weight
    )


def calculate_match_score(
    technical_results: dict,
    soft_skill_results: dict,
    education_results: dict,
    experience_results: dict,
    desirable_results: dict,
) -> dict:
    """
    Calculate the explainable CV match score.

    Weights:
        technical: 35%
        experience: 25%
        soft skills: 20%
        education: 10%
        desirable: 10%

    Categories absent from the job description are
    ignored and the remaining weights are normalised.
    """

    technical_score = (
        calculate_category_score(
            technical_results
        )
    )

    experience_score = (
        calculate_category_score(
            experience_results
        )
    )

    soft_skill_score = (
        calculate_category_score(
            soft_skill_results
        )
    )

    education_score = (
        calculate_category_score(
            education_results
        )
    )

    desirable_score = (
        calculate_category_score(
            desirable_results
        )
    )

    overall_score = (
        calculate_weighted_average(
            [
                (
                    technical_score,
                    0.35,
                ),
                (
                    experience_score,
                    0.25,
                ),
                (
                    soft_skill_score,
                    0.20,
                ),
                (
                    education_score,
                    0.10,
                ),
                (
                    desirable_score,
                    0.10,
                ),
            ]
        )
    )

    return {
        "technical_score": technical_score,
        "experience_score": experience_score,
        "soft_skill_score": soft_skill_score,
        "education_score": education_score,
        "desirable_score": desirable_score,
        "overall_score": overall_score,
    }