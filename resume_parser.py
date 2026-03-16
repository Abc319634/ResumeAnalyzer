import io
import PyPDF2
import docx
import re

def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def parse_resume(text):
    sections = {
        "skills": "",
        "education": "",
        "projects": "",
        "experience": "",
        "certifications": ""
    }
    
    # Simple regex-based section splitting
    lines = text.split('\n')
    current_section = None
    
    keywords = {
        "skills": ["skills", "technical skills", "competencies", "technologies"],
        "education": ["education", "academic background", "qualification"],
        "projects": ["projects", "personal projects", "academic projects"],
        "experience": ["experience", "work experience", "professional experience", "internship"],
        "certifications": ["certifications", "certs", "courses", "awards"]
    }
    
    current_content = []
    
    for line in lines:
        clean_line = line.strip().lower()
        found_section = False
        
        for section, keys in keywords.items():
            if any(key == clean_line or (len(clean_line) > 5 and key in clean_line[:15]) for key in keys):
                if current_section and current_content:
                    sections[current_section] = "\n".join(current_content).strip()
                current_section = section
                current_content = []
                found_section = True
                break
        
        if not found_section and current_section:
            current_content.append(line)
            
    if current_section and current_content:
        sections[current_section] = "\n".join(current_content).strip()
    
    # If no sections were found at all, use the whole text as experience
    if not any(sections.values()):
        sections["experience"] = text

    return sections

def get_skills_list(text):
    # Very basic skill extraction - can be improved with a predefined list
    # For now, let's just clean up the text
    return [s.strip() for s in text.split(',') if s.strip()]
