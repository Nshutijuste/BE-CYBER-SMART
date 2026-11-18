import hashlib

import httpx

from app.services.breach_check import PwnedPasswordsChecker

PASSWORD = "correct horse battery staple"
DIGEST = hashlib.sha1(PASSWORD.encode(), usedforsecurity=False).hexdigest().upper()
PREFIX, SUFFIX = DIGEST[:5], DIGEST[5:]


def checker(handler) -> PwnedPasswordsChecker:
    return PwnedPasswordsChecker(client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_a_leaked_password_is_found():
    def handler(request):
        return httpx.Response(200, text=f"0000000000000000000000000000000AAAA:2\r\n{SUFFIX}:3861\r\n")

    assert checker(handler).is_breached(PASSWORD) is True


def test_a_password_that_is_not_in_the_list_is_fine():
    def handler(request):
        return httpx.Response(200, text="0000000000000000000000000000000AAAA:2\r\n")

    assert checker(handler).is_breached(PASSWORD) is False


def test_padding_lines_with_a_zero_count_are_ignored():
    def handler(request):
        return httpx.Response(200, text=f"{SUFFIX}:0\r\n")

    assert checker(handler).is_breached(PASSWORD) is False


def test_only_the_first_five_characters_leave_the_server():
    seen = []

    def handler(request):
        seen.append(request)
        return httpx.Response(200, text="")

    checker(handler).is_breached(PASSWORD)
    request = seen[0]
    assert request.url.path.endswith(f"/range/{PREFIX}")
    assert SUFFIX not in str(request.url)
    assert PASSWORD not in str(request.url)
    assert request.headers["add-padding"] == "true"


def test_if_the_service_is_down_registration_is_not_blocked():
    def handler(request):
        raise httpx.ConnectError("no network")

    assert checker(handler).is_breached(PASSWORD) is False


def test_an_error_reply_is_treated_the_same_way():
    def handler(request):
        return httpx.Response(503)

    assert checker(handler).is_breached(PASSWORD) is False
