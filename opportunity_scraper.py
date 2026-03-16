import requests
from bs4 import BeautifulSoup

def scrape_opportunity(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
            
        text = soup.get_text(separator='\n')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    except Exception as e:
        print(f"Scraping error: {e}")
        return None

def detect_opportunity_type(text):
    text = text.lower()
    if any(k in text for k in ["internship", "intern", "trainee"]):
        return "Internship"
    if any(k in text for k in ["hackathon", "hack", "coding competition"]):
        return "Hackathon"
    if any(k in text for k in ["committee", "society", "club", "student body"]):
        return "College Committee"
    if any(k in text for k in ["competition", "contest", "prize"]):
        return "Competition"
    return "Job" # default
