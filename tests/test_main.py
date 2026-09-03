from pathlib import Path

import pytest

from main import analyze_files, load_text_file


def test_load_text_file_reads_utf8_file(
    tmp_path: Path,
):
    file_path = tmp_path / "example.txt"

    file_path.write_text(
        "Software Engineering student.",
        encoding="utf-8",
    )

    result = load_text_file(
        str(file_path)
    )

    assert result == "Software Engineering student."


def test_load_text_file_raises_for_missing_file(
    tmp_path: Path,
):
    missing_path = tmp_path / "missing.txt"

    with pytest.raises(
        FileNotFoundError
    ):
        load_text_file(
            str(missing_path)
        )


def test_load_text_file_rejects_directory(
    tmp_path: Path,
):
    with pytest.raises(
        ValueError
    ):
        load_text_file(
            str(tmp_path)
        )


def test_analyze_files_rejects_empty_cv(
    tmp_path: Path,
):
    cv_path = tmp_path / "cv.txt"
    job_path = tmp_path / "job.txt"

    cv_path.write_text(
        "",
        encoding="utf-8",
    )

    job_path.write_text(
        "Java is required.",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="CV file is empty",
    ):
        analyze_files(
            str(cv_path),
            str(job_path),
        )


def test_analyze_files_rejects_empty_job_description(
    tmp_path: Path,
):
    cv_path = tmp_path / "cv.txt"
    job_path = tmp_path / "job.txt"

    cv_path.write_text(
        "Built a Java project.",
        encoding="utf-8",
    )

    job_path.write_text(
        "",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="Job description file is empty",
    ):
        analyze_files(
            str(cv_path),
            str(job_path),
        )


def test_analyze_files_returns_rendered_report(
    tmp_path: Path,
):
    cv_path = tmp_path / "cv.txt"
    job_path = tmp_path / "job.txt"

    cv_path.write_text(
        """
        Software Engineering student at university.

        Built a Java application for a university project.

        Technical skills include Python.

        Collaborated with other students during
        group coursework.

        Communication is one of my strengths.
        """,
        encoding="utf-8",
    )

    job_path.write_text(
        """
        Applicants should be studying Software Engineering.

        Experience developing software is required.

        Java, Python and Git are required.

        Strong communication and teamwork skills are important.
        """,
        encoding="utf-8",
    )

    result = analyze_files(
        str(cv_path),
        str(job_path),
    )

    assert "CV MATCH ANALYSIS" in result
    assert "Overall Match Score:" in result
    assert "java" in result
    assert "python" in result
    assert "git" in result
    assert "IMPROVEMENT SUGGESTIONS" in result