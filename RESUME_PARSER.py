# Install required libraries:
# pip install pdfplumber spacy
# python -m spacy download en_core_web_sm

import pdfplumber
import spacy
import re

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Skills list
SKILLS = [
    "Python", "Java", "C", "C++", "JavaScript", "HTML", "CSS",
    "SQL", "Machine Learning", "Artificial Intelligence",
    "Data Science", "NLP", "Deep Learning", "Git", "OpenCV"
]

def extract_text(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_email(text):
    email = re.findall(r'[\w\.-]+@[\w\.-]+', text)
    return email[0] if email else "Not Found"

def extract_phone(text):
    phone = re.findall(r'\+?\d[\d\s-]{8,15}', text)
    return phone[0] if phone else "Not Found"

def extract_name(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            return ent.text
    return "Not Found"

def extract_skills(text):
    found = []
    for skill in SKILLS:
        if skill.lower() in text.lower():
            found.append(skill)
    return found

def extract_section(text, keywords):
    lines = text.split("\n")
    section = []

    capture = False

    for line in lines:
        if any(word.lower() in line.lower() for word in keywords):
            capture = True
            continue

        if capture:
            if line.strip() == "":
                break
            section.append(line)

    return section

pdf_file = "resume.pdf"

text = extract_text(pdf_file)

print("=" * 50)
print("RESUME DETAILS")
print("=" * 50)

print("Name :", extract_name(text))
print("Email:", extract_email(text))
print("Phone:", extract_phone(text))

print("\nSkills:")
print(extract_skills(text))

print("\nEducation:")
print(extract_section(text, ["Education"]))

print("\nExperience:")
print(extract_section(text, ["Experience", "Work Experience"]))

print("\nProjects:")
print(extract_section(text, ["Projects"]))
