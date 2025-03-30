# Resume-Job-Matcher
AI Resume & Job Matcher

This project is an AI-powered Resume and Job Matching system built with Django (backend) and Streamlit (frontend). The backend processes resume files, extracts relevant details, and matches candidates to job postings based on skills.

Prerequisites

Ensure you have the following installed:

Python (>=3.8)

pip

virtualenv (optional but recommended)

SQLite (default)

Setup Instructions

1. Clone the Repository

git clone https://github.com/sharuhaasan/Resume-Job-Matcher.git

cd Resume-Job-Matcher

2. Create and Activate a Virtual Environment

python -m venv venv  # Create a virtual environment
venv\Scripts\activate  # On Windows

3. Install Dependencies

pip install -r requirements.txt

4. Set Up Environment Variables

Create a .env file in the project root and add the following:

SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
DATABASE_URL=sqlite:///db.sqlite3  # Change for PostgreSQL if needed
LLM_API_KEY=your_llm_api_key  # If using an AI model for resume parsing

5. Run Database Migrations

python manage.py makemigrations
python manage.py migrate

6. Start the Django Backend

python manage.py runserver

This will start the API server at http://127.0.0.1:8000/

Running the Streamlit Frontend

The Streamlit app is located in app.py

1. Install Streamlit Dependencies

pip install streamlit requests

2. Start Streamlit

streamlit run app.py

This will launch the frontend at http://localhost:8501/

This will start both the Django API and Streamlit UI.
This url used to upload resume, list all the jobs that are created and to view matching result for a job based on uploaded resume.

API Endpoints(Backend)

POST /upload-resume/ - Upload and parse a resume

GET /upload-job/ - Retrieve job postings

POST /match/ - Match a candidate to a job

Troubleshooting

If streamlit run app.py fails, ensure all dependencies are installed.

If Django doesn't start, verify migrations again.

For permission issues, run chmod +x manage.py on Unix-based systems.


