# StudyMe – AI Powered Learning Assistant

StudyMe is a full-stack web application that analyzes recorded lectures (audio or video) and automatically transforms them into structured learning materials using Google Gemini AI.

The system generates:
- A clear summary
- Key learning points
- Tasks or assignments mentioned in the lecture
- A multiple-choice quiz

The goal of the project is to demonstrate a production-level AI integration suitable for a junior developer portfolio.

---

## Project Goal

To build a real, working web product that integrates AI in a meaningful way — not just prompt in / text out.

StudyMe processes real audio and video files and turns them into practical study content.

---

## Target Users

- Students who record lectures
- Self-learners studying from video or audio lessons
- Anyone who wants to convert passive listening into active learning

---

## Main Features

- Upload audio or video lecture files
- AI analysis using Gemini API
- Automatic generation of:
  - Summary
  - Key points
  - Tasks
  - Quiz questions
- Clean and simple web interface
- Fully Dockerized system

---

## AI Integration (Gemini API)

The backend communicates securely with the Gemini API.

Workflow:
1. User uploads a media file from the frontend
2. Backend receives and validates the file
3. The file is uploaded to Gemini
4. Gemini analyzes the lecture content
5. Gemini returns structured JSON
6. Backend parses and returns results to the frontend

This is a real AI workflow using uploaded media files.

---

## System Architecture

Frontend (React)  
→ Backend (FastAPI)  
→ Gemini API  
→ Structured AI response  
→ Frontend display

---

## Technology Stack

Frontend:
- React
- Vite
- JavaScript

Backend:
- Python
- FastAPI
- Uvicorn
- Gemini API

DevOps:
- Docker
- Docker Compose
- GitHub

---

## Docker Requirements

The entire project runs inside Docker containers.

Containers:
- Frontend container
- Backend container

Docker Compose is used to run the full system.

---

## Running the Project with Docker

### Prerequisites
- Docker Desktop
- Git

### Steps

Clone the repository:
```bash
git clone <REPOSITORY_URL>
cd StudyMe

Create .env file inside backend/:
GEMINI_API_KEY=your_api_key_here

Build and run:
docker compose up --build

Access the application at:
Application URLs
Frontend:
http://localhost:4173

Backend API:
http://localhost:8080

API Documentation (Swagger):
http://localhost:8080/docs

Testing
The project includes automated backend tests.

Testing tools:

pytest

httpx

Tests include:

API endpoint tests

File upload validation

Integration flow testing

Tests are located in:
backend/tests/
Project Structure
css

StudyMe/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── tests/
│   └── .env (ignored)
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   └── dist/ (ignored)
├── docker-compose.yml
├── .gitignore
└── README.md
CI/CD (Optional)
The project is prepared for CI/CD integration.

Possible pipeline stages:

Install dependencies

Run tests

Build Docker images

Deploy locally or to the cloud

Final Presentation Topics
Problem definition

Product demo

System architecture

AI integration workflow

Backend responsibilities

Testing strategy

Dockerization

Challenges and learnings

Team
This project was developed as a pair project.

Authors:

Elisheva Wislovsky

Chana Maayani

Summary
StudyMe is a complete, Dockerized AI web application that demonstrates real backend logic, AI integration, testing, and modern development practices.
---
