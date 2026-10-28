# BE CYBER SMART

A safety platform that teaches people to stay safe from scams and hacking,
helps them when something goes wrong, and warns them before they fall for a scam.

## Stack
- Website: Next.js, TypeScript, Tailwind
- Engine: Python, FastAPI
- Data: PostgreSQL with pgvector
- Chatbot: Ollama (local models)
- Delivery: Docker, GitHub Actions

## Setup
1. Copy `.env.example` to `.env` and fill in the values.
2. Start the database: `docker compose up -d` (added in Week 1).
3. Backend and frontend steps are added as we build them.

## Docs
See the `docs/` folder for the Design, SRS and threat model.

## Security
Never commit `.env`. Report security problems privately to the project owner.