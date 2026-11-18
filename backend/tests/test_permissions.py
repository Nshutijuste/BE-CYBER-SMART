from app.core.permissions import (
    MFA_REQUIRED_ROLES,
    ROLE_PERMISSIONS,
    Permission,
    permissions_for,
)


def test_every_role_can_read_its_own_profile():
    for role in ROLE_PERMISSIONS:
        assert Permission.READ_OWN_PROFILE in permissions_for(role)


def test_roles_get_only_their_own_powers():
    assert Permission.MANAGE_USERS in permissions_for("system_admin")
    assert Permission.MANAGE_USERS not in permissions_for("analyst")
    assert Permission.REVIEW_CASES in permissions_for("analyst")
    assert Permission.READ_AUDIT in permissions_for("auditor")
    assert Permission.READ_AUDIT not in permissions_for("system_admin")
    assert Permission.MANAGE_OWN_REPORTS in permissions_for("subscriber")
    assert Permission.REVIEW_CASES not in permissions_for("subscriber")


def test_an_unknown_role_gets_nothing():
    assert permissions_for("made-up-role") == frozenset()


def test_staff_and_institution_admins_need_a_second_step_but_subscribers_do_not():
    assert {"analyst", "system_admin", "auditor", "institution_admin"} <= MFA_REQUIRED_ROLES
    assert "subscriber" not in MFA_REQUIRED_ROLES
