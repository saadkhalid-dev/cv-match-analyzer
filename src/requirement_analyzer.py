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
        "team members",
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


EDUCATION_TERMS = [
    "degree",
    "undergraduate",
    "university",
    "computer science",
    "software engineering",
    "computing",
    "stem degree",
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
]


def extract_soft_skills(text: str) -> set[str]:
    normalized_text = normalize_text(text)
    found_skills = set()

    for skill_name, phrases in SOFT_SKILLS.items():
        for phrase in phrases:
            if phrase in normalized_text:
                found_skills.add(skill_name)
                break

    return found_skills


def contains_any_term(text: str, terms: list[str]) -> bool:
    normalized_text = normalize_text(text)

    for term in terms:
        if term in normalized_text:
            return True

    return False


def split_into_sentences(text: str) -> list[str]:
    """
    Split text into simple readable sentences.

    This is deliberately lightweight rather than using a large NLP library.
    """

    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

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
    Return sentences containing at least one supplied requirement term.
    """

    matching_sentences = []

    for sentence in split_into_sentences(text):
        normalized_sentence = normalize_text(sentence)

        if any(term in normalized_sentence for term in terms):
            matching_sentences.append(sentence)

    return matching_sentences


def analyze_job_requirements(text: str) -> dict:
    education_evidence = extract_matching_sentences(
        text,
        EDUCATION_TERMS,
    )

    experience_evidence = extract_matching_sentences(
        text,
        EXPERIENCE_TERMS,
    )

    desirable_evidence = extract_matching_sentences(
        text,
        DESIRABLE_TERMS,
    )

    return {
        "technical_skills": extract_skills(text),
        "soft_skills": extract_soft_skills(text),
        "education_required": bool(education_evidence),
        "experience_required": bool(experience_evidence),
        "desirable_criteria_present": bool(desirable_evidence),
        "education_evidence": education_evidence,
        "experience_evidence": experience_evidence,
        "desirable_evidence": desirable_evidence,
    }