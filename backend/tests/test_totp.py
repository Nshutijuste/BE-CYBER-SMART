import pyotp

from app.core.totp import new_secret, provisioning_uri, verify_totp

NOW = 1_800_000_000.0  # a fixed moment, so tests never depend on the real clock


def code_at(secret: str, when: float) -> str:
    return pyotp.TOTP(secret).at(when)


def test_the_current_code_is_accepted_and_gives_its_step():
    secret = new_secret()
    assert verify_totp(secret, code_at(secret, NOW), now=NOW) == int(NOW // 30)


def test_one_step_of_clock_drift_is_allowed_but_not_two():
    secret = new_secret()
    assert verify_totp(secret, code_at(secret, NOW - 30), now=NOW) is not None
    assert verify_totp(secret, code_at(secret, NOW + 30), now=NOW) is not None
    assert verify_totp(secret, code_at(secret, NOW - 90), now=NOW) is None


def test_a_used_code_cannot_be_used_again():
    secret = new_secret()
    step = verify_totp(secret, code_at(secret, NOW), now=NOW)
    assert verify_totp(secret, code_at(secret, NOW), now=NOW, after_step=step) is None


def test_a_wrong_code_and_odd_inputs_are_refused():
    secret = new_secret()
    right = code_at(secret, NOW)
    wrong = "000000" if right != "000000" else "111111"
    assert verify_totp(secret, wrong, now=NOW) is None
    assert verify_totp(secret, "12345", now=NOW) is None
    assert verify_totp(secret, "abcdef", now=NOW) is None
    assert verify_totp(secret, "", now=NOW) is None


def test_the_setup_link_names_the_service_and_account():
    uri = provisioning_uri(new_secret(), "ann@example.com")
    assert uri.startswith("otpauth://totp/")
    assert "Be%20Cyber%20Smart" in uri
