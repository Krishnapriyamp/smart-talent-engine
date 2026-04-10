# Smart Talent Selection Engine

I built this project as a full-stack AI-based system to automate resume screening and candidate ranking. The goal is to reduce manual effort in shortlisting candidates when there are large volumes of applications.

The system extracts information from resumes, analyzes it using AI-based similarity matching, and ranks candidates based on how well they match the given job description.


## Features

- Upload resumes in PDF and DOCX formats
- Extract text and structured data from resumes automatically
- AI-based candidate ranking using semantic similarity
- Skill normalization using custom skill ontology
- Experience extraction from resume content
- User authentication system (register/login)
- Interactive dashboard with ranked candidates and visual charts

## Tech Stack

### Backend
- FastAPI (API development)
- SQLite (database)
- Sentence Transformers (semantic similarity)
- Scikit-learn (scoring and ML logic)
- PDFPlumber & python-docx (resume parsing)
- Pytesseract & Pillow (OCR for scanned documents)

### Frontend
- React.js (UI development)
- Axios (API communication)
- Recharts (data visualization)
- React Router (navigation)

## Installation

### Prerequisites
- Python 3.8+
- Node.js 14+
- Tesseract OCR (optional, for image-based PDFs)

### Backend Setup

cd backend
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt


### Frontend Setup

cd frontend
npm install


## Running the Application


1. Start the backend:

cd backend
# Activate venv first
uvicorn main:app --reload


2. Start the frontend:

cd frontend
npm start


The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs




## API Endpoints

- `POST /register` - User registration
- `POST /login` - User authentication
- `POST /upload` - Upload resumes for processing
- `POST /rank` - Rank candidates based on job description

## Project Structure


smart-talent-selection/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── auth.py              # Authentication logic
│   ├── parser.py            # Resume parsing
│   ├── ranking.py           # Candidate ranking
│   ├── scorer.py            # Scoring algorithms
│   ├── ontology.py          # Skill normalization
│   ├── experience_extractor.py # Experience calculation
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js           # Main React app
│   │   ├── components/      # React components
│   │   └── pages/           # Application pages
│   ├── package.json         # Node dependencies
│   └── public/              # Static assets
├── .gitignore               # Git ignore rules
└── README.md                



##  What I Learned

- Building full-stack applications using FastAPI and React  
- Working with NLP models for semantic similarity  
- Extracting and processing resume data  
- Designing ranking systems using scoring logic  
- Connecting backend APIs with frontend UI  



##  Future Improvements

- Improve ranking using fine-tuned transformer models  
- Add admin dashboard for recruiters  
- Deploy the project on cloud platforms (AWS / Render / Vercel)  
- Add support for multi-language resumes  




