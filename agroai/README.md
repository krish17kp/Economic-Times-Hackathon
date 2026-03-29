# AgroAI — Agro-Waste Decision Support Platform

## Quick Start

```bash
# Clone and start
git clone https://github.com/yourname/agroai.git
cd agroai
cp .env.example .env
make dev
```
Backend API docs: http://localhost:8000/docs
Frontend: http://localhost:3000

Commands
Command	What it does
make dev	Start all services
make stop	Stop all services
make test	Run backend tests
make seed	Populate database with sample data
make migrate	Run database migrations
make clean	Remove everything including DB data

Tech Stack
Frontend: React (Vite) + Tailwind CSS
Backend: FastAPI (Python 3.11)
Database: PostgreSQL 16
AI: ChromaDB + OpenAI GPT-3.5 (RAG only)
