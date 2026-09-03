from src.evidence_analyzer import (
    get_education_strength_for_requirement,
    get_experience_strength_for_requirement,
    get_soft_skill_evidence_strength,
    get_technical_skill_evidence_strength,
)
from src.requirement_analyzer import (
    EDUCATION_TERMS,
    EXPERIENCE_TERMS,
    analyze_job_requirements,
    contains_any_term,
    extract_required_technical_skills,
    extract_soft_skills,
)
from src.scoring import calculate_match_score
from src.skill_extractor import extract_skills


def match_technical_skills(
    job_description: str,
    cv_text: str,
) -> dict:
    """
    Compare required technical skills from the job
    description with skills found in the CV.

    Desirable skills are excluded from the required
    technical category.
    """

    job_skills = extract_required_technical_skills(
        job_description
    )

    cv_skills = extract_skills(
        cv_text
    )

    return {
        "matched": job_skills.intersection(
            cv_skills
        ),
        "missing": job_skills.difference(
            cv_skills
        ),
    }


def match_technical_skill_evidence(
    job_description: str,
    cv_text: str,
) -> dict:
    """
    Classify required technical skills as strong,
    partial or missing based on CV evidence.
    """

    required_skills = extract_required_technical_skills(
        job_description
    )

    strong = set()
    partial = set()
    missing = set()

    for skill in required_skills:
        strength = get_technical_skill_evidence_strength(
            skill,
            cv_text,
        )

        if strength == "strong":
            strong.add(skill)

        elif strength == "partial":
            partial.add(skill)

        else:
            missing.add(skill)

    return {
        "strong": strong,
        "partial": partial,
        "missing": missing,
    }


def match_soft_skills(
    job_description: str,
    cv_text: str,
) -> dict:
    """
    Compare required soft skills against CV evidence.
    """

    required_skills = extract_soft_skills(
        job_description
    )

    strong = set()
    partial = set()
    missing = set()

    for skill in required_skills:
        strength = get_soft_skill_evidence_strength(
            skill,
            cv_text,
        )

        if strength == "strong":
            strong.add(skill)

        elif strength == "partial":
            partial.add(skill)

        else:
            missing.add(skill)

    return {
        "strong": strong,
        "partial": partial,
        "missing": missing,
    }


def get_education_evidence_strength(
    job_description: str,
    cv_text: str,
) -> str | None:
    """
    Evaluate required education criteria.

    Education fragments are combined before scoring
    so alternative subjects can be handled together.

    None means the job contains no required
    education criterion.
    """

    requirements = analyze_job_requirements(
        job_description
    )

    education_evidence = requirements[
        "education_evidence"
    ]

    if not education_evidence:
        return None

    combined_requirement = " ".join(
        education_evidence
    )

    return get_education_strength_for_requirement(
        combined_requirement,
        cv_text,
    )


def get_experience_evidence_strength(
    job_description: str,
    cv_text: str,
) -> str | None:
    """
    Evaluate required experience criteria.

    None means the job contains no required
    experience criterion.
    """

    requirements = analyze_job_requirements(
        job_description
    )

    experience_evidence = requirements[
        "experience_evidence"
    ]

    if not experience_evidence:
        return None

    strengths = [
        get_experience_strength_for_requirement(
            sentence,
            cv_text,
        )
        for sentence in experience_evidence
    ]

    if all(
        strength == "strong"
        for strength in strengths
    ):
        return "strong"

    if all(
        strength == "missing"
        for strength in strengths
    ):
        return "missing"

    return "partial"


def get_desirable_criterion_strength(
    criterion: str,
    cv_text: str,
) -> str:
    """
    Evaluate one desirable criterion.

    A desirable criterion may contain technical,
    soft-skill, education or experience requirements.
    """

    strengths = []

    technical_skills = extract_skills(
        criterion
    )

    soft_skills = extract_soft_skills(
        criterion
    )

    for skill in technical_skills:
        strengths.append(
            get_technical_skill_evidence_strength(
                skill,
                cv_text,
            )
        )

    for skill in soft_skills:
        strengths.append(
            get_soft_skill_evidence_strength(
                skill,
                cv_text,
            )
        )

    if contains_any_term(
        criterion,
        EDUCATION_TERMS,
    ):
        strengths.append(
            get_education_strength_for_requirement(
                criterion,
                cv_text,
            )
        )

    if contains_any_term(
        criterion,
        EXPERIENCE_TERMS,
    ):
        strengths.append(
            get_experience_strength_for_requirement(
                criterion,
                cv_text,
            )
        )

    if not strengths:
        return "missing"

    if all(
        strength == "strong"
        for strength in strengths
    ):
        return "strong"

    if all(
        strength == "missing"
        for strength in strengths
    ):
        return "missing"

    return "partial"


def match_desirable_criteria(
    job_description: str,
    cv_text: str,
) -> dict:
    """
    Evaluate recognised desirable criteria.
    """

    requirements = analyze_job_requirements(
        job_description
    )

    desirable_criteria = requirements[
        "desirable_evidence"
    ]

    strong = set()
    partial = set()
    missing = set()

    for criterion in desirable_criteria:
        strength = get_desirable_criterion_strength(
            criterion,
            cv_text,
        )

        if strength == "strong":
            strong.add(criterion)

        elif strength == "partial":
            partial.add(criterion)

        else:
            missing.add(criterion)

    return {
        "strong": strong,
        "partial": partial,
        "missing": missing,
    }


def build_single_requirement_result(
    requirement_name: str,
    strength: str | None,
) -> dict:
    """
    Convert a single requirement into the same
    result structure used by the other categories.
    """

    result = {
        "strong": set(),
        "partial": set(),
        "missing": set(),
    }

    if strength is None:
        return result

    result[strength].add(
        requirement_name
    )

    return result


def match_cv_to_job(
    job_description: str,
    cv_text: str,
) -> dict:
    """
    Run the complete CV-to-job comparison.
    """

    technical = match_technical_skill_evidence(
        job_description,
        cv_text,
    )

    soft_skills = match_soft_skills(
        job_description,
        cv_text,
    )

    education_strength = get_education_evidence_strength(
        job_description,
        cv_text,
    )

    experience_strength = get_experience_evidence_strength(
        job_description,
        cv_text,
    )

    education = build_single_requirement_result(
        "education",
        education_strength,
    )

    experience = build_single_requirement_result(
        "experience",
        experience_strength,
    )

    desirable = match_desirable_criteria(
        job_description,
        cv_text,
    )

    scores = calculate_match_score(
        technical,
        soft_skills,
        education,
        experience,
        desirable,
    )

    return {
        "technical": technical,
        "soft_skills": soft_skills,
        "education": education,
        "experience": experience,
        "desirable": desirable,
        "scores": scores,
    }