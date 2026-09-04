# CV Match Analyzer

A Python command-line application that compares a CV with a job description and produces an explainable match analysis.

The tool identifies technical requirements, soft skills, education, experience and desirable criteria, then evaluates how strongly the CV provides evidence for each area.

It is designed to support truthful CV tailoring rather than simply checking whether keywords appear.

---

## Features

- Extracts technical skills from CVs and job descriptions
- Identifies required technical skills separately from desirable criteria
- Detects common soft-skill requirements such as:
  - communication
  - teamwork
  - problem solving
  - organisation
  - adaptability
- Analyses education requirements
- Analyses general and commercial experience requirements
- Classifies CV evidence as:
  - strong
  - partial
  - missing
- Calculates category scores and an overall weighted match score
- Generates improvement suggestions for weak or missing evidence
- Avoids recommending experience or skills that are not genuinely supported by the CV
- Runs locally from the command line
- Includes automated tests covering the analysis pipeline

---

## Example

Given a job description requiring:

- Java
- Python
- Git
- teamwork
- communication
- Software Engineering education
- software development experience

the program can produce a report such as:

```text
CV MATCH ANALYSIS
========================================

Overall Match Score: 88%

TECHNICAL SKILLS
Score: 100%
  Strong evidence:
    - git
    - java
    - python
  Partial evidence:
    None
  Missing evidence:
    None

SOFT SKILLS
Score: 67%
  Strong evidence:
    - communication
    - teamwork
  Partial evidence:
    None
  Missing evidence:
    - problem solving

EDUCATION
Score: 100%

EXPERIENCE
Score: 100%

DESIRABLE CRITERIA
Score: 50%

IMPROVEMENT SUGGESTIONS
----------------------------------------
1. No evidence for problem solving was found.
2. The CV only partially supports a desirable commercial experience criterion.
```

The exact score and recommendations depend on the supplied CV and job description.

---

## How It Works

The application uses a rules-based analysis pipeline so that its results remain understandable and explainable.

### 1. Text Processing

Input text is normalised so that CV and job-description content can be compared consistently.

The text-processing stage handles differences such as capitalisation, punctuation and repeated whitespace before later analysis takes place.

### 2. Skill Extraction

A controlled vocabulary and boundary-aware regular expressions are used to identify technical skills while reducing incorrect substring matches.

For example:

- `C` is not incorrectly detected inside `C++`
- `SQL` is not incorrectly counted from `PostgreSQL`
- longer matching skill names are prioritised where necessary

The controlled vocabulary currently covers a selection of:

- programming languages
- frontend technologies
- backend technologies
- databases
- development tools

### 3. Requirement Analysis

The job description is analysed to identify different types of employer requirements, including:

- required technical skills
- soft skills
- education requirements
- experience requirements
- desirable criteria

Explicitly desirable technical requirements are kept separate from required technical skills so that optional criteria do not incorrectly increase the required-skills score.

### 4. Evidence Analysis

The CV is evaluated for evidence supporting each identified requirement.

Evidence is classified into three levels:

#### Strong

The CV demonstrates the requirement through relevant context or practical evidence.

For example, describing how a programming language was used within a project provides stronger evidence than simply listing the language.

#### Partial

The CV mentions or provides some support for the requirement but does not demonstrate it strongly enough for full credit.

#### Missing

No relevant evidence is identified in the CV.

Commercial or industry experience requirements are treated more strictly than general university or personal project experience.

### 5. Scoring

Each assessed category receives a score based on its evidence classifications.

- strong evidence receives full credit
- partial evidence receives half credit
- missing evidence receives no credit

The overall score uses the following weighting:

| Category | Weight |
| --- | ---: |
| Technical skills | 35% |
| Experience | 25% |
| Soft skills | 20% |
| Education | 10% |
| Desirable criteria | 10% |

If a category is not present in the job description, it is excluded from the weighted calculation rather than automatically receiving zero.

### 6. Report Generation

The final report presents:

- overall match score
- individual category scores
- strong evidence
- partial evidence
- missing evidence
- improvement suggestions

The suggestions focus on communicating genuine evidence more clearly rather than encouraging unsupported claims.

---

## Project Structure

```text
cv-match-analyzer/
├── sample_data/
│   ├── cv.txt
│   └── job_description.txt
├── src/
│   ├── __init__.py
│   ├── evidence_analyzer.py
│   ├── matcher.py
│   ├── report.py
│   ├── requirement_analyzer.py
│   ├── scoring.py
│   ├── skill_extractor.py
│   └── text_processor.py
├── tests/
│   ├── test_evidence_analyzer.py
│   ├── test_main.py
│   ├── test_matcher.py
│   ├── test_report.py
│   ├── test_requirement_analyzer.py
│   ├── test_scoring.py
│   ├── test_skill_extractor.py
│   └── test_text_processor.py
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```

---

## Getting Started

### Requirements

- Python 3.12 or newer
- pytest for running the automated tests

### Clone the Repository

```bash
git clone https://github.com/saadkhalid-dev/cv-match-analyzer.git
```

Move into the project directory:

```bash
cd cv-match-analyzer
```

Install the development dependency:

```bash
python -m pip install -r requirements.txt
```

---

## Running the Analyzer

The application accepts two UTF-8 text files:

1. a CV
2. a job description

Run:

```bash
python main.py sample_data/cv.txt sample_data/job_description.txt
```

On Windows PowerShell, you can also use:

```powershell
python main.py sample_data\cv.txt sample_data\job_description.txt
```

The sample files can be replaced with other plain-text CV and job-description files.

---

## Running the Tests

Run the complete automated test suite with:

```bash
python -m pytest
```

The test suite covers:

- text normalisation
- technical skill extraction
- job requirement analysis
- CV evidence analysis
- requirement matching
- category and overall scoring
- report generation
- command-line file handling
- error handling for invalid input files

---

## Engineering Decisions

### Rules-Based Rather Than AI-Generated Scoring

The current version deliberately uses deterministic rules instead of relying on an external AI model.

This keeps the analysis:

- explainable
- reproducible
- locally runnable
- independent of external APIs
- straightforward to test

The project is therefore not intended to replicate a commercial Applicant Tracking System or claim to predict an employer's actual hiring decision.

### Evidence Matters More Than Keyword Presence

A technology appearing somewhere in a CV does not automatically provide the same strength of evidence as demonstrating its use.

For example:

```text
Python
```

provides weaker evidence than:

```text
Developed a Python application to process structured data.
```

This distinction allows the analyzer to identify situations where a candidate genuinely knows a technology but could communicate that experience more effectively.

### Required and Desirable Criteria Are Separated

Job descriptions frequently contain both essential and desirable requirements.

A desirable skill should not incorrectly increase the score for required technical skills, so explicitly desirable criteria are analysed independently.

### Commercial Experience Is Treated Separately

University projects can demonstrate valuable software development experience, but they should not automatically be treated as commercial industry experience.

The evidence analyzer therefore applies stricter rules when a job description specifically asks for commercial, professional or industry experience.

### Truthful CV Tailoring

The application does not advise users to claim experience or skills that are unsupported by their CV.

When evidence is missing, suggestions encourage clearer evidence only when the candidate genuinely possesses it.

---

## Current Limitations

The analyzer uses a controlled vocabulary and rules-based text processing, so it cannot understand every possible way an employer may phrase a requirement.

Current limitations include:

- input is limited to plain UTF-8 text rather than PDF or DOCX
- the technical-skill vocabulary is intentionally limited
- complex job-description layouts may not always be interpreted perfectly
- semantic similarity between differently worded requirements is limited
- evidence strength is based on deterministic language rules rather than full natural-language understanding
- unusual formatting or section structures may reduce extraction accuracy

These limitations keep the current implementation transparent, testable and appropriate for the scope of the project.

---

## Future Improvements

Possible future improvements include:

- PDF and DOCX input support
- configurable technical-skill vocabularies
- improved recognition of job-description sections
- more advanced evidence matching
- improved handling of differently phrased but related requirements
- report export to a file
- a graphical or web-based interface

---

## Why I Built It

I built this project while preparing for software engineering placement applications.

Job descriptions often contain a mixture of technical requirements, education criteria, experience expectations, desirable skills and interpersonal requirements. I wanted to create a tool that could break those requirements down and show where a CV contains strong evidence, weaker evidence or genuine gaps.

The project also gave me practical experience with:

- Python application structure
- regular expressions
- collections and sets
- text processing
- modular program design
- scoring algorithms
- file handling
- command-line interfaces
- automated testing
- separating responsibilities across modules

It also provided an opportunity to think about an important software-design problem: producing useful recommendations while keeping the underlying decision process understandable and testable.