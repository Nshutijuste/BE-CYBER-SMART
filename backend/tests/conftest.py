import os

# Safe fake settings, so tests never need a real .env or a real database.
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("DATABASE_URL", "postgresql://test:test@localhost:5432/test")
os.environ.setdefault("JWT_SIGNING_KEY", "test-only-not-a-secret-jwt")
os.environ.setdefault("HMAC_SECRET", "test-only-not-a-secret-hmac")
os.environ.setdefault("FIELD_ENCRYPTION_KEY", "test-only-not-a-secret-field")
