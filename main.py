from src.requirement_analyzer import analyze_job_requirements


job_description = """
Software Engineering Placement.

We are looking for an undergraduate studying Software Engineering
or Computer Science.

You will work with Java, Python, PostgreSQL and Git.

The successful candidate should have strong communication skills,
good problem solving ability and enjoy collaborating within a team.

Previous project experience would be beneficial.
"""


requirements = analyze_job_requirements(job_description)


print("JOB REQUIREMENTS")
print("----------------")

print("\nTechnical skills:")
for skill in sorted(requirements["technical_skills"]):
    print(f"- {skill}")

print("\nSoft skills:")
for skill in sorted(requirements["soft_skills"]):
    print(f"- {skill}")

print("\nEducation:")
for sentence in requirements["education_evidence"]:
    print(f"- {sentence}")

print("\nExperience:")
for sentence in requirements["experience_evidence"]:
    print(f"- {sentence}")

print("\nDesirable criteria:")
for sentence in requirements["desirable_evidence"]:
    print(f"- {sentence}")