# Economic-Times-Hackathon
AI Money Mentor

AI Money Mentor is a GenAI-powered portfolio analysis platform that converts mutual fund statements into clear, actionable insights.

Users can upload a CAMS PDF or CSV file and instantly receive a portfolio health score, detailed breakdown, and personalized recommendations.

The system focuses on reliability, explainability, and real-world usability instead of generic AI outputs.

Problem

Mutual fund investors receive statements that are difficult to interpret.

These documents are often:

unstructured
complex
filled with financial jargon

As a result, users do not clearly understand:

how their portfolio is performing
whether their investments are balanced
what actions they should take

Existing tools either provide generic advice or rely on unreliable AI outputs.

Solution

AI Money Mentor transforms raw financial statements into structured insights.

The system:

extracts portfolio data from PDF or CSV
normalizes the data into a standard format
computes deterministic financial metrics
generates a portfolio health score
produces actionable insights and a plain-English summary

All calculations are deterministic, while AI is used only for explanation and reasoning.

Key Features
PDF and CSV upload support
Gemini-based PDF extraction
Deterministic financial calculations
Portfolio health score out of 100
Sub-scores for diversification, overlap, cost efficiency, and risk balance
AI-generated insights based on real data
Plain-English summary for easy understanding
Sample portfolio mode for demo
Clean and intuitive dashboard
Architecture Overview

The system follows a multi-agent architecture with clear separation of responsibilities.

Flow
User uploads file from frontend
File is validated and routed
PDF is processed using Gemini for extraction
CSV is parsed using pandas
Data is normalized into a unified schema
Metrics are computed deterministically
Health score is calculated using rule-based logic
AI generates insights and summary
Dashboard renders final output

This ensures reliability and modularity.

Tech Stack
Frontend
React (Vite)
Tailwind CSS
Recharts
Backend
FastAPI
Pydantic
pandas
AI
Google Gemini API
Project Structure

ai-money-mentor
backend
app
routes
services
parsers
prompts
models
utils
data

frontend
src
pages
components
services
hooks
utils

Setup Instructions
Backend

cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python run.py

Backend runs on http://localhost:8000

Frontend

cd frontend
npm install
npm run dev

Frontend runs on http://localhost:5173

Environment Variables

Create a .env file inside backend:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-1.5-flash

API Endpoints

POST /api/upload
Upload PDF or CSV and get parsed portfolio

POST /api/analyze
Generate metrics, score, and insights

GET /api/sample
Load sample portfolio

GET /api/health
Check system status

Impact

AI Money Mentor delivers measurable value:

Reduces analysis time from 30 minutes to under 1 minute
Eliminates need for manual interpretation
Improves financial decision-making
Enables scalable insights for fintech platforms
Design Principles
Deterministic calculations over AI hallucinations
Clear separation between logic and AI reasoning
Honest error handling
Stateless architecture
Minimal dependencies
Limitations
PDF parsing depends on Gemini accuracy
No transaction-level analysis
No real-time market data
Focused on mutual funds only
Future Improvements
Support for stocks and ETFs
Goal-based investment planning
Historical performance tracking
Broker API integrations
Personalized risk profiling
Conclusion

AI Money Mentor simplifies complex financial data into actionable intelligence.

It combines structured computation with AI reasoning to deliver a reliable and user-friendly portfolio analysis experience.
