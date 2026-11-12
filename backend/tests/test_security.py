from argon2 import PasswordHasher as Argon2

from app.core.security import Argon2PasswordHasher


def test_hash_is_argon2id_and_hides_the_password():
    hashed = Argon2PasswordHasher().hash("correct horse battery staple")
    assert hashed.startswith("$argon2id$")
    assert "correct horse" not in hashed


def test_hash_uses_the_owasp_minimum_settings():
    hashed = Argon2PasswordHasher().hash("some password 123")
    assert "m=19456,t=2,p=1" in hashed


def test_same_password_gives_different_hashes():
    hasher = Argon2PasswordHasher()
    assert hasher.hash("same password 123") != hasher.hash("same password 123")


def test_verify_right_and_wrong_password():
    hasher = Argon2PasswordHasher()
    hashed = hasher.hash("right password 123")
    assert hasher.verify(hashed, "right password 123") is True
    assert hasher.verify(hashed, "wrong password 123") is False


def test_verify_a_garbage_hash_is_false_not_an_error():
    assert Argon2PasswordHasher().verify("not-a-hash", "anything") is False


def test_weaker_old_hash_needs_rehash():
    weak = Argon2(time_cost=1, memory_cost=8, parallelism=1).hash("x")
    hasher = Argon2PasswordHasher()
    assert hasher.needs_rehash(weak) is True
    assert hasher.needs_rehash(hasher.hash("x")) is False