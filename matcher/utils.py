import pdfplumber
import docx
import re
import json
import nltk

nltk.download("punkt")
from nltk.tokenize import word_tokenize

# Predefined skill set (extend this list)
SKILL_SET = {"Python", "Django", "React", "SQL", "Docker", "Kubernetes", "AWS"}

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    return text

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def extract_name(text):
    lines = text.split("\n")
    for line in lines[:5]:  # Only check the first few lines
        words = word_tokenize(line)
        if len(words) > 1 and words[0].istitle() and words[1].istitle():
            return line.strip()
    return "Unknown"

def extract_email_from_text(text):
    """
    Extracts the first valid email found in the given text using regex.
    """
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    matches = re.findall(email_pattern, text)
    return matches[0] if matches else None

def parse_resume(text):
    """Extracts name, skills, education, and experience from resume text."""
    name = extract_name(text)
    email = extract_email_from_text(text)

    skills = list(set(word.lower() for word in word_tokenize(text)) & {s.lower() for s in SKILL_SET})
    education = list(set(re.findall(r"(?i)(B\.?Tech|M\.?Tech|BSc|MSc|PhD|Bachelor|Master)[^\n]+", text)))
    experience = re.findall(r"(?i)([\w\s]+ at [\w\s]+ \(\d{4} - (?:Present|\d{4})\))", text)
    

    return {
        "name": name,
        "email": email,
        "skills": skills,
        "education": education,
        "experience": experience,
    }


from jinja2 import Template

cover_letter_template = Template("""
Dear Hiring Manager,

I am excited to apply for the {{ job_title }} role at {{ company }}. With my expertise in {{ ', '.join(candidate_skills) }}, 
I believe I can contribute effectively to your team.

I look forward to discussing how my experience aligns with your requirements.

Sincerely,  
{{ candidate_name }}
""")

def generate_cover_letter(candidate, job):
    return cover_letter_template.render(
        job_title=job["title"],
        company=job["company"],
        candidate_skills=candidate["skills"],
        candidate_name=candidate["name"]
    )
