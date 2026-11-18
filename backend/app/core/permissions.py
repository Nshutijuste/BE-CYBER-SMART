"""Who may do what. Anything not listed here is denied."""

from enum import StrEnum


class Permission(StrEnum):
    READ_OWN_PROFILE = "read_own_profile"
    MANAGE_OWN_REPORTS = "manage_own_reports"
    MANAGE_INSTITUTION = "manage_institution"
    REVIEW_CASES = "review_cases"
    PUBLISH_ALERTS = "publish_alerts"
    MANAGE_USERS = "manage_users"
    MANAGE_CONTENT = "manage_content"
    READ_AUDIT = "read_audit"


_EVERYONE = {Permission.READ_OWN_PROFILE}

ROLE_PERMISSIONS: dict[str, frozenset[Permission]] = {
    "subscriber": frozenset(_EVERYONE | {Permission.MANAGE_OWN_REPORTS}),
    "institution_admin": frozenset(_EVERYONE | {Permission.MANAGE_INSTITUTION}),
    "analyst": frozenset(_EVERYONE | {Permission.REVIEW_CASES, Permission.PUBLISH_ALERTS}),
    "system_admin": frozenset(_EVERYONE | {Permission.MANAGE_USERS, Permission.MANAGE_CONTENT}),
    "auditor": frozenset(_EVERYONE | {Permission.READ_AUDIT}),
}

# FR-AUTH-5: staff and institution admins must use a second step.
MFA_REQUIRED_ROLES = frozenset({"institution_admin", "analyst", "system_admin", "auditor"})


def permissions_for(role: str) -> frozenset[Permission]:
    return ROLE_PERMISSIONS.get(role, frozenset())  # unknown role: nothing
