import re

from src.text_processor import normalize_text


SKILLS = {
    "languages": [
        "java",
        "python",
        "c",
        "c++",
        "c#",
        "javascript",
        "typescript",
        "sql",
    ],
    "frontend": [
        "html",
        "css",
        "react",
        "next.js",
    ],
    "backend": [
        "node.js",
        "django",
        "flask",
        "fastapi",
        "spring",
    ],
    "databases": [
        "postgresql",
        "postgres",
        "mysql",
        "sqlite",
        "mongodb",
        "supabase",
    ],
    "tools": [
        "git",
        "github",
        "docker",
        "linux",
    ],
}


def build_skill_pattern(skill: str) -> str:
    """
    Build a regex pattern that matches a technical skill as a complete term.

    This prevents partial-word matches such as:
        "c" inside "communication"
        "sql" inside "postgresql"
    """

    escaped_skill = re.escape(skill)

    return rf"(?<![a-z0-9]){escaped_skill}(?![a-z0-9])"


def spans_overlap(
    first: tuple[int, int],
    second: tuple[int, int],
) -> bool:
    """
    Return True when two text ranges overlap.
    """

    first_start, first_end = first
    second_start, second_end = second

    return first_start < second_end and second_start < first_end


def extract_skills(text: str) -> set[str]:
    """
    Extract known technical skills from supplied text.

    Longer skill names are checked first so a shorter skill cannot also
    match characters that already belong to a more specific technology.

    Example:
        "C++" is detected as "c++", not both "c++" and "c".
    """

    normalized_text = normalize_text(text)

    all_skills = {
        skill
        for category_skills in SKILLS.values()
        for skill in category_skills
    }

    ordered_skills = sorted(all_skills, key=len, reverse=True)

    found_skills: set[str] = set()
    occupied_spans: list[tuple[int, int]] = []

    for skill in ordered_skills:
        pattern = build_skill_pattern(skill)

        for match in re.finditer(pattern, normalized_text):
            match_span = match.span()

            overlaps_existing_match = any(
                spans_overlap(match_span, occupied_span)
                for occupied_span in occupied_spans
            )

            if not overlaps_existing_match:
                found_skills.add(skill)
                occupied_spans.append(match_span)

    return found_skills