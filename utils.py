def extract_skills_and_experiences(data):
    skills = [entry['skill'] for entry in data]
    experiences = [entry['experience'] for entry in data]
    return skills, experiences