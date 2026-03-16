# Project Context: ResumeAnalyzer

## Purpose
The project was created to empower students to understand their standing in various competitive environments. By providing a quantitative measure of resume-opportunity compatibility, it helps users optimize their applications and identify skill gaps.

## Key Features
- Multi-format resume support (PDF, DOCX).
- Web scraping for automated opportunity retrieval.
- Categorical analysis (Jobs vs. Hackathons).
- Secure user session management.

## Design Decisions
- **Framework**: Streamlit was chosen for its rapid prototyping capabilities and built-in responsiveness.
- **Database**: SQLite was selected for zero-configuration, local-first storage, making the app fully portable.
- **NLP**: Basic TF-IDF and keyword matching were used to ensure performance without requiring heavy machine learning models or API costs.
- **UI**: A minimalist aesthetic was prioritized to keep the user focused on the metrics and suggestions.

## Implementation Details
- The project follows a modular architecture, separating data storage, business logic, and UI rendering.
- Password hashing is implemented via the industry-standard `bcrypt` library.
- Custom CSS is injected to enhance the standard Streamlit components into "cards" and premium-feeling metrics.
