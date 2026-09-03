import re

from src.skill_extractor import extract_skills
from src.text_processor import normalize_text


SOFT_SKILLS = {
    "communication": [
        "communication",
        "communicate",
        "written communication",
        "verbal communication",
    ],
    "teamwork": [
        "teamwork",
        "team player",
        "working in a team",
        "work effectively in a team",
        "collaborate",
        "collaborating",
        "collaboration",
        "collaborative",
        "team members",
        "group project",
        "group projects",
        "group coursework",
    ],
    "problem solving": [
        "problem solving",
        "problem-solving",
        "analytical thinking",
        "analytical skills",
    ],
    "organisation": [
        "organised",
        "organized",
        "organisation",
        "organization",
        "time management",
    ],
    "adaptability": [
        "adaptable",
        "adaptability",
        "willingness to learn",
        "eager to learn",
        "quick learner",
    ],
}


SOFT_SKILL_EVIDENCE_PHRASES = {
    "communication": [
        "presented",
        "presentation",
        "communicated with",
        "explained",
        "customer",
        "customers",
        "client",
        "clients",
    ],
    "teamwork": [
        "collaborated",
        "worked with",
        "worked alongside",
        "group project",
        "group coursework",
        "team members",
        "with other students",
        "with other team members",
        "team of",
        "group of",
    ],
    "problem solving": [
        "solved",
        "debugged",
        "troubleshot",
        "identified the issue",
        "resolved",
        "investigated",
    ],
    "organisation": [
        "managed deadlines",
        "prioritised",
        "prioritized",
        "planned",
        "scheduled",
        "managed multiple",
    ],
    "adaptability": [
        "learned",
        "adapted",
        "self taught",
        "self-taught",
        "new technology",
        "new technologies",
    ],
}


EDUCATION_TERMS = [
    "degree",
    "undergraduate",
    "university",
    "computer science",
    "software engineering",
    "computing",
    "stem",
]


EDUCATION_CONTEXT_TERMS = [
    "degree",
    "undergraduate",
    "university",
    "student",
    "studying",
    "study",
    "graduate",
    "bachelor",
    "bachelor's",
    "masters",
    "master's",
]


EXPERIENCE_TERMS = [
    "experience",
    "previous experience",
    "commercial experience",
    "industry experience",
    "work experience",
    "project experience",
]


DESIRABLE_TERMS = [
    "desirable",
    "preferred",
    "advantageous",
    "nice to have",
    "beneficial",
    "would be a plus",
    "an advantage",
]


def extract_soft_skills(text: str) -> set[str]:
    """
    Extract known soft-skill categories from text.
    """

    normalized_text = normalize_text(text)
    found_skills = set()

    for skill_name, phrases in SOFT_SKILLS.items():
        for phrase in phrases:
            if phrase in normalized_text:
                found_skills.add(skill_name)
                break

    return found_skills


def contains_any_term(
    text: str,
    terms: list[str],
) -> bool:
    """
    Return True if the text contains at least one
    supplied term.
    """

    normalized_text = normalize_text(text)

    return any(
        term in normalized_text
        for term in terms
    )


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into readable sentences.

    New lines are also treated as possible boundaries
    because job descriptions commonly use bullet-style
    formatting.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text.strip(),
    )

    return [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]


def extract_matching_sentences(
    text: str,
    terms: list[str],
) -> list[str]:
    """
    Return sentences containing at least one
    supplied term.
    """

    matching_sentences = []

    for sentence in split_into_sentences(text):
        normalized_sentence = normalize_text(
            sentence
        )

        if any(
            term in normalized_sentence
            for term in terms
        ):
            matching_sentences.append(
                sentence
            )

    return matching_sentences


def is_desirable_sentence(
    sentence: str,
) -> bool:
    """
    Return True when a sentence describes a
    preferred rather than essential criterion.
    """

    return contains_any_term(
        sentence,
        DESIRABLE_TERMS,
    )


def extract_required_technical_skills(
    text: str,
) -> set[str]:
    """
    Extract technical skills that belong to required
    or general job criteria.

    Skills appearing only inside sentences explicitly
    marked as desirable or preferred are excluded.
    """

    required_skills = set()

    for sentence in split_into_sentences(text):
        if is_desirable_sentence(sentence):
            continue

        required_skills.update(
            extract_skills(sentence)
        )

    return required_skills


def is_education_sentence(
    sentence: str,
) -> bool:
    """
    Determine whether a sentence genuinely describes
    an education requirement.

    This avoids treating titles such as
    'Software Engineering Placement' as degree
    requirements.
    """

    normalized_sentence = normalize_text(
        sentence
    )

    contains_education_term = any(
        term in normalized_sentence
        for term in EDUCATION_TERMS
    )

    contains_education_context = any(
        term in normalized_sentence
        for term in EDUCATION_CONTEXT_TERMS
    )

    return (
        contains_education_term
        and contains_education_context
    )


def extract_required_education_sentences(
    text: str,
) -> list[str]:
    """
    Extract required education criteria while
    excluding desirable education criteria.
    """

    evidence = []

    for sentence in split_into_sentences(text):
        if not is_education_sentence(sentence):
            continue

        if is_desirable_sentence(sentence):
            continue

        evidence.append(sentence)

    return evidence


def extract_required_experience_sentences(
    text: str,
) -> list[str]:
    """
    Extract required experience criteria while
    excluding experience that is explicitly
    desirable.
    """

    evidence = []

    for sentence in split_into_sentences(text):
        normalized_sentence = normalize_text(
            sentence
        )

        contains_experience = any(
            term in normalized_sentence
            for term in EXPERIENCE_TERMS
        )

        if not contains_experience:
            continue

        if is_desirable_sentence(sentence):
            continue

        evidence.append(sentence)

    return evidence


def analyze_job_requirements(
    text: str,
) -> dict:
    """
    Analyse a job description and return its main
    requirement categories.
    """

    education_evidence = (
        extract_required_education_sentences(
            text
        )
    )

    experience_evidence = (
        extract_required_experience_sentences(
            text
        )
    )

    desirable_evidence = (
        extract_matching_sentences(
            text,
            DESIRABLE_TERMS,
        )
    )

    return {
        "technical_skills": extract_skills(
            text
        ),
        "required_technical_skills": (
            extract_required_technical_skills(
                text
            )
        ),
        "soft_skills": extract_soft_skills(
            text
        ),
        "education_required": bool(
            education_evidence
        ),
        "experience_required": bool(
            experience_evidence
        ),
        "desirable_criteria_present": bool(
            desirable_evidence
        ),
        "education_evidence": (
            education_evidence
        ),
        "experience_evidence": (
            experience_evidence
        ),
        "desirable_evidence": (
            desirable_evidence
        ),
    }