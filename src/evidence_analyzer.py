from src.requirement_analyzer import (
    EDUCATION_CONTEXT_TERMS,
    SOFT_SKILL_EVIDENCE_PHRASES,
    extract_soft_skills,
    split_into_sentences,
)
from src.skill_extractor import extract_skills
from src.text_processor import normalize_text


TECHNICAL_EVIDENCE_TERMS = [
    "built",
    "developed",
    "created",
    "implemented",
    "project",
    "projects",
    "experience",
    "used",
    "using",
    "worked with",
]


EDUCATION_SUBJECT_TERMS = [
    "software engineering",
    "computer science",
    "computing",
    "stem",
]


COMMERCIAL_REQUIREMENT_TERMS = [
    "commercial",
    "industry",
    "industrial experience",
    "work experience",
    "professional experience",
    "employment experience",
    "internship",
    "placement experience",
]


COMMERCIAL_EVIDENCE_TERMS = [
    "commercial experience",
    "industry experience",
    "industrial experience",
    "work experience",
    "professional experience",
    "internship",
    "intern",
    "industrial placement",
    "placement experience",
    "completed a placement",
    "completed an internship",
    "employment",
    "employed",
    "worked at",
    "worked as",
]


PROJECT_EXPERIENCE_TERMS = [
    "project",
    "projects",
    "coursework",
    "built",
    "developed",
    "implemented",
    "created",
]


def get_technical_skill_evidence_strength(
    skill: str,
    cv_text: str,
) -> str:
    """
    Classify technical-skill evidence as strong,
    partial or missing.

    Strong evidence means the skill appears in the
    same sentence or line as practical usage or
    project context.

    Partial evidence means the skill is mentioned
    without supporting usage evidence.
    """

    cv_skills = extract_skills(
        cv_text
    )

    if skill not in cv_skills:
        return "missing"

    sentences = split_into_sentences(
        cv_text
    )

    for sentence in sentences:
        sentence_skills = extract_skills(
            sentence
        )

        if skill not in sentence_skills:
            continue

        normalized_sentence = normalize_text(
            sentence
        )

        has_evidence_context = any(
            term in normalized_sentence
            for term in TECHNICAL_EVIDENCE_TERMS
        )

        if has_evidence_context:
            return "strong"

    return "partial"


def get_soft_skill_evidence_strength(
    skill: str,
    cv_text: str,
) -> str:
    """
    Classify soft-skill evidence as strong,
    partial or missing.

    Strong evidence requires a recognised phrase
    showing the skill in practice.

    Partial evidence means the CV mentions the skill
    without demonstrating it.
    """

    normalized_cv = normalize_text(
        cv_text
    )

    detected_cv_skills = extract_soft_skills(
        cv_text
    )

    evidence_phrases = (
        SOFT_SKILL_EVIDENCE_PHRASES.get(
            skill,
            [],
        )
    )

    for phrase in evidence_phrases:
        if phrase in normalized_cv:
            return "strong"

    if skill in detected_cv_skills:
        return "partial"

    return "missing"


def get_education_strength_for_requirement(
    requirement_text: str,
    cv_text: str,
) -> str:
    """
    Compare one education requirement with the CV.

    If a job accepts several recognised subjects,
    matching any one of them is treated as strong
    evidence.
    """

    normalized_requirement = normalize_text(
        requirement_text
    )

    normalized_cv = normalize_text(
        cv_text
    )

    required_subjects = {
        subject
        for subject in EDUCATION_SUBJECT_TERMS
        if subject in normalized_requirement
    }

    cv_subjects = {
        subject
        for subject in EDUCATION_SUBJECT_TERMS
        if subject in normalized_cv
    }

    cv_has_education_context = any(
        term in normalized_cv
        for term in EDUCATION_CONTEXT_TERMS
    )

    if required_subjects:
        matching_subjects = (
            required_subjects.intersection(
                cv_subjects
            )
        )

        if matching_subjects:
            return "strong"

        if (
            "stem" in required_subjects
            and cv_subjects
        ):
            return "strong"

        if cv_has_education_context:
            return "partial"

        return "missing"

    if cv_has_education_context:
        return "strong"

    return "missing"


def get_experience_strength_for_requirement(
    requirement_text: str,
    cv_text: str,
) -> str:
    """
    Compare one experience requirement with the CV.

    Commercial, professional or industry requirements
    are treated more strictly than general project
    experience.
    """

    normalized_requirement = normalize_text(
        requirement_text
    )

    normalized_cv = normalize_text(
        cv_text
    )

    requires_commercial_experience = any(
        term in normalized_requirement
        for term in COMMERCIAL_REQUIREMENT_TERMS
    )

    cv_has_commercial_experience = any(
        term in normalized_cv
        for term in COMMERCIAL_EVIDENCE_TERMS
    )

    cv_has_project_experience = any(
        term in normalized_cv
        for term in PROJECT_EXPERIENCE_TERMS
    )

    cv_mentions_experience = (
        "experience" in normalized_cv
    )

    if requires_commercial_experience:
        if cv_has_commercial_experience:
            return "strong"

        if (
            cv_has_project_experience
            or cv_mentions_experience
        ):
            return "partial"

        return "missing"

    if (
        cv_has_commercial_experience
        or cv_has_project_experience
    ):
        return "strong"

    if cv_mentions_experience:
        return "partial"

    return "missing"