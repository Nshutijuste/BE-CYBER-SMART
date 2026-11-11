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
Works on Linux and Windows. On Windows, use Git Bash in VS Code, or PowerShell with the alternatives shown.

1. Copy `.env.example` to `.env` and fill in the values. Never commit `.env`.
   The user, password and port in `DATABASE_URL` must match the `POSTGRES_*`
   values and the port in `docker-compose.yml`.
2. Start the database:
   ```sh
   docker compose up -d
   ```
3. Backend:
   ```sh
   cd backend
   python3 -m venv .venv                # Windows: python -m venv .venv
   source .venv/bin/activate            # Windows PowerShell: .\.venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   python -m alembic upgrade head
   python -m pytest
   python -m uvicorn app.main:app --reload --port 8001
   ```
4. Frontend:
   ```sh
   cd frontend
   npm ci
   npm run dev
   ```

## Docs
See the `docs/` folder for the Design, SRS and threat model.

## Security
Never commit `.env`. Report security problems privately to the project owner.