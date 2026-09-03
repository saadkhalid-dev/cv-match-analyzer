import sys
from pathlib import Path

from src.matcher import match_cv_to_job
from src.report import build_report_summary, render_report


def load_text_file(file_path: str) -> str:
    """
    Load a UTF-8 text file.

    Raises a clear error when the path does not exist,
    is not a file, or cannot be read.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    if not path.is_file():
        raise ValueError(
            f"Path is not a file: {file_path}"
        )

    try:
        return path.read_text(
            encoding="utf-8"
        )
    except UnicodeDecodeError as error:
        raise ValueError(
            f"File must be UTF-8 text: {file_path}"
        ) from error


def analyze_files(
    cv_path: str,
    job_path: str,
) -> str:
    """
    Load a CV and job description, run the complete
    analysis pipeline and return the rendered report.
    """

    cv_text = load_text_file(
        cv_path
    )

    job_text = load_text_file(
        job_path
    )

    if not cv_text.strip():
        raise ValueError(
            "CV file is empty."
        )

    if not job_text.strip():
        raise ValueError(
            "Job description file is empty."
        )

    match_result = match_cv_to_job(
        job_text,
        cv_text,
    )

    report_summary = build_report_summary(
        match_result
    )

    return render_report(
        report_summary
    )


def print_usage() -> None:
    """
    Print the expected command format.
    """

    print(
        "Usage:"
    )

    print(
        "  python main.py <cv_file> <job_description_file>"
    )

    print()

    print(
        "Example:"
    )

    print(
        r"  python main.py sample_data\cv.txt "
        r"sample_data\job_description.txt"
    )


def main() -> int:
    """
    Command-line entry point.

    Returns an exit code so the program can be used
    cleanly from terminals and scripts.
    """

    if len(sys.argv) != 3:
        print_usage()
        return 1

    cv_path = sys.argv[1]
    job_path = sys.argv[2]

    try:
        report = analyze_files(
            cv_path,
            job_path,
        )
    except (
        FileNotFoundError,
        ValueError,
        OSError,
    ) as error:
        print(
            f"Error: {error}"
        )
        return 1

    print(
        report
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )