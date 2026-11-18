import pytest
from cryptography.exceptions import InvalidTag

from app.core.crypto import FieldCipher, KeyedHasher

SECRET = "a-test-secret-long-enough"


def test_keyed_hash_is_stable_and_hides_the_value():
    keyed = KeyedHasher(SECRET)
    assert keyed("phone:+250781000000") == keyed("phone:+250781000000")
    assert "250781000000" not in keyed("phone:+250781000000")
    assert len(keyed("x")) == 64


def test_keyed_hash_depends_on_the_secret():
    assert KeyedHasher("secret-one")("same") != KeyedHasher("secret-two")("same")


def test_cipher_round_trip():
    cipher = FieldCipher(SECRET)
    sealed = cipher.encrypt("JBSWY3DPEHPK3PXP")
    assert sealed.startswith("v1.")
    assert "JBSWY3DPEHPK3PXP" not in sealed
    assert cipher.decrypt(sealed) == "JBSWY3DPEHPK3PXP"


def test_cipher_uses_a_new_nonce_every_time():
    cipher = FieldCipher(SECRET)
    assert cipher.encrypt("same text") != cipher.encrypt("same text")


def test_a_changed_ciphertext_is_rejected():
    cipher = FieldCipher(SECRET)
    sealed = cipher.encrypt("hello")
    tampered = sealed[:-4] + ("AAAA" if not sealed.endswith("AAAA") else "BBBB")
    with pytest.raises((InvalidTag, ValueError)):
        cipher.decrypt(tampered)


def test_ciphertext_is_tied_to_its_owner():
    cipher = FieldCipher(SECRET)
    sealed = cipher.encrypt("hello", aad=b"user-1")
    assert cipher.decrypt(sealed, aad=b"user-1") == "hello"
    with pytest.raises(InvalidTag):
        cipher.decrypt(sealed, aad=b"user-2")


def test_another_key_cannot_read_it_and_unknown_versions_are_refused():
    sealed = FieldCipher(SECRET).encrypt("hello")
    with pytest.raises(InvalidTag):
        FieldCipher("a-different-secret-entirely").decrypt(sealed)
    with pytest.raises(ValueError):
        FieldCipher(SECRET).decrypt("v9.abcd")
