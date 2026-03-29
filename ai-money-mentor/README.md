# AI Money Mentor

Your personal portfolio analyst.

## Setup Instructions

### Backend (FastAPI)
1. cd backend
2. python -m venv venv
3. source venv/bin/activate (or venv\Scripts\activate on Windows)
4. pip install -r requirements.txt
5. cp .env.example .env
6. python run.py (runs on port 8000)

### Frontend (React + Vite)
1. cd frontend
2. npm install
3. npm run dev (runs on port 5173)

### Demo
Click "Try with Sample Portfolio" on the UI to test the complete end-to-end data flow with mocked data. Upload a CSV to parse real mutual fund holdings.
