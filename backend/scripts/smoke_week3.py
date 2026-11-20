"""Live check of Week 3 against your real database.

Run from backend/ with (.venv) active and the Docker database up:
    Linux / Git Bash:  PYTHONPATH=. python scripts/smoke_week3.py
    PowerShell:        $env:PYTHONPATH="."; python scripts/smoke_week3.py

It creates throw-away test users (smoke...@example.com) in your DEVELOPMENT database.
"""

import os
import random
import sys
import time
import uuid

os.environ["APP_ENV"] = "test"  # plain-http cookies, so the test client can send them back

import pyotp
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

from app.core.config import get_settings
from app.main import app

IP = f"198.51.100.{random.randint(2, 250)}"  # a fresh address each run, so old runs never interfere
results: list[tuple[bool, str]] = []


def client() -> TestClient:
    return TestClient(app, client=(IP, 50000))


def check(label: str, got, expected) -> None:
    ok = got == expected
    results.append((ok, label))
    print(f"{'PASS' if ok else 'FAIL'}  {label:58} got={got!r}" + ("" if ok else f" expected={expected!r}"))


email = f"smoke{uuid.uuid4().hex[:8]}@example.com"
password = "a long enough passphrase"
c = client()

r = c.post("/api/v1/auth/register", json={"email": email, "password": password})
check("register", r.status_code, 201)
r = c.post("/api/v1/auth/register", json={"email": email.upper(), "password": password})
check("register the same email again (any case)", (r.status_code, r.json()["error"]["code"]), (409, "account_unavailable"))

wrong = c.post("/api/v1/auth/login", json={"email": email, "password": "wrong wrong wrong"})
unknown = c.post("/api/v1/auth/login", json={"email": "nobody@example.com", "password": "wrong wrong wrong"})
check("wrong password and unknown account: same 401", (wrong.status_code, unknown.status_code), (401, 401))
check("... and exactly the same body", wrong.json() == unknown.json(), True)

r = c.post("/api/v1/auth/login", json={"email": email, "password": password})
check("login ok", (r.status_code, r.json()), (200, {"status": "ok", "mfa_token": None}))
check("three cookies are set", sorted(c.cookies.keys()), ["access_token", "csrf_token", "refresh_token"])
flags = {h.split("=")[0]: h for h in r.headers.get_list("set-cookie")}
check("access cookie: HttpOnly + SameSite=lax", "HttpOnly" in flags["access_token"] and "SameSite=lax" in flags["access_token"], True)
check("refresh cookie: HttpOnly + Strict + auth path only", all(x in flags["refresh_token"] for x in ("HttpOnly", "SameSite=strict", "Path=/api/v1/auth")), True)
check("csrf cookie is readable by the page", "HttpOnly" not in flags["csrf_token"], True)

r = c.get("/api/v1/me")
check("GET /me with the cookie", (r.status_code, r.json()["role"], r.json()["mfa_verified"]), (200, "subscriber", False))
check("GET /me with no cookie", client().get("/api/v1/me").status_code, 401)
check("GET /me with a forged token", client().get("/api/v1/me", headers={"Authorization": "Bearer abc.def.ghi"}).status_code, 401)

old_refresh, csrf = c.cookies.get("refresh_token"), c.cookies.get("csrf_token")
r = c.post("/api/v1/auth/refresh")
check("refresh WITHOUT the csrf header", (r.status_code, r.json()["error"]["code"]), (403, "csrf_failed"))
r = c.post("/api/v1/auth/refresh", headers={"X-CSRF-Token": csrf})
check("refresh with the csrf header", r.status_code, 200)
check("the refresh token was replaced", c.cookies.get("refresh_token") != old_refresh, True)
r = client().post("/api/v1/auth/refresh", headers={"X-CSRF-Token": csrf, "Cookie": f"refresh_token={old_refresh}; csrf_token={csrf}"})
check("replay of the OLD refresh token", (r.status_code, r.json()["error"]["code"]), (401, "session_invalid"))
r = c.post("/api/v1/auth/refresh", headers={"X-CSRF-Token": c.cookies.get("csrf_token")})
check("the NEW token is dead after the replay alarm", r.status_code, 401)

c = client()
c.post("/api/v1/auth/login", json={"email": email, "password": password})
r = c.get("/api/v1/admin/ping")
check("admin area as a subscriber", (r.status_code, r.json()["error"]["code"]), (403, "forbidden"))

engine = create_engine(get_settings().sqlalchemy_url)
with engine.begin() as k:
    k.execute(text("update users set role_id=(select id from roles where name='system_admin') where email=:e"), {"e": email})
r = c.get("/api/v1/admin/ping")
check("admin area, admin WITHOUT the second step", (r.status_code, r.json()["error"]["code"]), (403, "mfa_required"))

csrf = c.cookies.get("csrf_token")
setup = c.post("/api/v1/auth/mfa/setup", headers={"X-CSRF-Token": csrf})
check("second step: setup", setup.status_code, 200)
secret = setup.json()["secret"]
r = c.post("/api/v1/auth/mfa/confirm", json={"code": pyotp.TOTP(secret).now()}, headers={"X-CSRF-Token": csrf})
check("second step: confirm with a right code", r.status_code, 200)
check("admin area WITH the second step", c.get("/api/v1/admin/ping").status_code, 200)

c2 = client()
r = c2.post("/api/v1/auth/login", json={"email": email, "password": password})
check("login again: asks for the second step, sets no cookies", (r.json()["status"], sorted(c2.cookies.keys())), ("mfa_required", []))
token = r.json()["mfa_token"]
check("second step with a wrong code", c2.post("/api/v1/auth/login/mfa", json={"mfa_token": token, "code": "000000"}).status_code, 401)
check("second step with a garbage pass", c2.post("/api/v1/auth/login/mfa", json={"mfa_token": "x.y.z", "code": "123456"}).status_code, 401)
r = c2.post("/api/v1/auth/login/mfa", json={"mfa_token": token, "code": pyotp.TOTP(secret).at(time.time() + 30)})
check("second step with the next right code", r.status_code, 200)
check("admin area after a second-step login", c2.get("/api/v1/admin/ping").status_code, 200)

bad = f"lock{uuid.uuid4().hex[:8]}@example.com"
codes = [client().post("/api/v1/auth/login", json={"email": bad, "password": "nope nope nope"}) for _ in range(6)]
check("5 wrong logins are free, the 6th is told to wait", [x.status_code for x in codes], [401] * 5 + [429])
check("... with a Retry-After header", codes[-1].headers.get("retry-after"), "30")

with engine.connect() as k:
    length = k.execute(text("select length(token_hash) from refresh_tokens limit 1")).scalar()
    sealed = k.execute(text("select left(secret_encrypted, 3) from mfa_credentials limit 1")).scalar()
    plain_pw = k.execute(text("select count(*) from users where password_hash = :p"), {"p": password}).scalar()
check("refresh tokens are stored as 64-character hashes", length, 64)
check("the second-step secret is stored encrypted", sealed, "v1.")
check("no password is stored in plain text", plain_pw, 0)

failed = [label for ok, label in results if not ok]
print(f"\n{len(results) - len(failed)} of {len(results)} checks passed.")
sys.exit(1 if failed else 0)