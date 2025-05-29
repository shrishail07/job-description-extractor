import re
import requests
from bs4 import BeautifulSoup
from docx import Document
from PyPDF2 import PdfReader
import os
import io

def scrape_job_description(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error scraping URL: {e}"

def extract_text_from_file(file_bytes, filename="uploaded_file.txt"):
    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext == ".txt":
        return file_bytes.decode("utf-8", errors="ignore")

    elif file_ext == ".pdf":
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

    elif file_ext == ".docx":
        doc = Document(io.BytesIO(file_bytes))
        return "\n".join([p.text for p in doc.paragraphs])

    else:
        return "Unsupported file type."

def extract_section(text, header):
    pattern = rf"{header}:(.*?)(\n[A-Z][a-zA-Z ]+:|\Z)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else "Not found"

def clean_and_parse_jd(text):
    cleaned_text = re.sub(r'\s+', ' ', text.strip())

    role = re.findall(r'(?i)hiring a[n]?\s+(.+?)\s+(with|who|that)', cleaned_text)
    role = role[0][0] if role else "Not found"

    experience = re.findall(r'(\d+\+?\s+years? of experience)', cleaned_text, re.IGNORECASE)
    experience_level = experience[0] if experience else "Not mentioned"

    skills_keywords = ['Python', 'SQL', 'Machine Learning', 'Deep Learning', 'NLP', 'Pandas', 'NumPy', 'Data Analysis', 'SPSS', 'SAS']
    skills_found = [skill for skill in skills_keywords if re.search(skill, cleaned_text, re.IGNORECASE)]

    preferred_skills = extract_section(text, "Preferred Skills")
    required_skills = extract_section(text, "Technical Requirements")
    responsibilities = extract_section(text, "Key Responsibilities")
    qualifications = extract_section(text, "Qualifications")
    location = extract_section(text, "Location")

    return {
        "Role / Title": role,
        "Responsibilities": responsibilities,
        "Required Skills": required_skills,
        "Preferred Skills": preferred_skills,
        "Qualifications": qualifications,
        "Experience Level": experience_level,
        "Location": location if location != "Not found" else "Remote",
        "Cleaned JD": cleaned_text,
        "Skills Found": skills_found,
        "Experience Mentioned": experience
    }
