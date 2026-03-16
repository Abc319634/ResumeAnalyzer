# ResumeAnalyzer

ResumeAnalyzer is a Streamlit-based application designed to help students and professionals analyze their resumes against specific opportunities like jobs, internships, hackathons, and competitions. It provides a compatibility score, skill matching, and actionable suggestions for improvement.

## Features

- **User Authentication**: Secure sign-up and login with hashed passwords.
- **Resume Management**: Upload PDF and DOCX resumes, with automatic section parsing.
- **Opportunity Analysis**: 
  - Paste job/internship descriptions.
  - Fetch opportunity details directly from a URL.
- **Smart Scoring**: Compatibility score (0-100%) based on TF-IDF similarity and keyword matching.
- **Type Detection**: Automatic classification of opportunities (Job, Internship, Hackathon, etc.) with logic adjustment.
- **Dashboard & History**: Track past analyses and view detailed reports.
- **Modern UI**: Clean, minimalist design with light/dark mode support and mobile responsiveness.

## Technologies Used

- **Python**: Core logic.
- **Streamlit**: Web interface.
- **SQLite**: Local data storage.
- **BeautifulSoup & Requests**: Web scraping.
- **PyPDF2 & python-docx**: Document parsing.
- **Scikit-learn**: TF-IDF for similarity analysis.
- **Bcrypt**: Secure password hashing.

## Installation

1. Ensure you have Python 3.8+ installed.
2. Clone this repository (or download the files).
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

1. Navigate to the project directory:
   ```bash
   cd ResumeAnalyzer
   ```
2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
3. Open your browser and go to `http://localhost:8501`.

## Project Structure

- `app.py`: Main entry point and routing.
- `auth.py`: Authentication and password hashing.
- `database.py`: SQLite database setup and queries.
- `resume_parser.py`: Text extraction and sectioning.
- `opportunity_scraper.py`: Web scraping and type detection.
- `analyzer.py`: Similarity logic and scoring.
- `ui_components.py`: Custom CSS and reusable UI parts.
- `utils/helpers.py`: Small utility functions.
- `data/`: Contains `database.db` (created on first run).

## Future Improvements

- Use Large Language Models (LLMs) for more accurate parsing and suggestions.
- Add LinkedIn profile scraping.
- Export analysis reports as PDFs.
- Real-time job recommendations based on resume.
