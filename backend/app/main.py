from fastapi import FastAPI

app = FastAPI(
    title="Tele-Safe Guard API",
    description="Scam and fraud protection platform",
    version="0.1.0"
)

@app.get("/health")
def health() -> dict:
    return{"status": "Up and running", "service": "tele-safe-guard-api"}
