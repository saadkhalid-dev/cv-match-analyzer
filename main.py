from src.skill_extractor import extract_skills


sample_job_description = """
We are looking for a Software Engineering placement student.

The successful candidate will work with Java, Python and React.
Experience with PostgreSQL, Git and GitHub would be beneficial.

You should be a strong communicator with an interest in technology.
"""

skills = extract_skills(sample_job_description)

print("Detected skills:")

for skill in sorted(skills):
    print(f"- {skill}")