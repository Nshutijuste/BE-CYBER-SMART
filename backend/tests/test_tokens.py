import base64
import json
import uuid
from datetime import timedelta

import pytest

from app.core.tokens import InvalidTokenError, TokenService

SECRET = "a-test-secret-long-enough"
USER = uuid.uuid4()


def test_access_token_round_trip():
    tokens = TokenService(SECRET)
    claims = tokens.decode_access(tokens.issue_access(USER, mfa=True))
    assert claims.user_id == USER
    assert claims.mfa is True


def test_the_mfa_flag_is_kept_false():
    tokens = TokenService(SECRET)
    assert tokens.decode_access(tokens.issue_access(USER, mfa=False)).mfa is False


def test_an_expired_token_is_refused():
    tokens = TokenService(SECRET, access_lifetime=timedelta(seconds=-5))
    with pytest.raises(InvalidTokenError):
        tokens.decode_access(tokens.issue_access(USER, mfa=False))


def test_a_token_from_another_secret_is_refused():
    token = TokenService("another-secret-entirely-1").issue_access(USER, mfa=False)
    with pytest.raises(InvalidTokenError):
        TokenService(SECRET).decode_access(token)


def test_a_changed_token_is_refused():
    tokens = TokenService(SECRET)
    token = tokens.issue_access(USER, mfa=False)
    head, body, signature = token.split(".")
    claims = json.loads(base64.urlsafe_b64decode(body + "=="))
    claims["mfa"] = True
    forged_body = base64.urlsafe_b64encode(json.dumps(claims).encode()).decode().rstrip("=")
    with pytest.raises(InvalidTokenError):
        tokens.decode_access(f"{head}.{forged_body}.{signature}")


def test_the_none_algorithm_is_refused():
    tokens = TokenService(SECRET)
    token = tokens.issue_access(USER, mfa=True)
    _, body, _ = token.split(".")
    header = base64.urlsafe_b64encode(b'{"alg":"none","typ":"JWT"}').decode().rstrip("=")
    with pytest.raises(InvalidTokenError):
        tokens.decode_access(f"{header}.{body}.")


def test_a_second_step_pass_cannot_be_used_as_an_access_token():
    tokens = TokenService(SECRET)
    challenge = tokens.issue_mfa_challenge(USER)
    with pytest.raises(InvalidTokenError):
        tokens.decode_access(challenge)
    assert tokens.decode_mfa_challenge(challenge) == USER


def test_an_access_token_cannot_be_used_as_a_second_step_pass():
    tokens = TokenService(SECRET)
    with pytest.raises(InvalidTokenError):
        tokens.decode_mfa_challenge(tokens.issue_access(USER, mfa=True))


def test_garbage_is_refused():
    with pytest.raises(InvalidTokenError):
        TokenService(SECRET).decode_access("not.a.token")
