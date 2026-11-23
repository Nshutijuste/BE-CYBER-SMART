"""audit log: the database refuses edits, deletes and a forked chain

Revision ID: d3b81a7f5c02
Revises: c7d41f0a9b21
"""
from alembic import op

revision = "d3b81a7f5c02"
down_revision = "c7d41f0a9b21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Two entries may never follow the same entry: the chain cannot fork.
    op.create_unique_constraint("uq_audit_entries_prev_hash", "audit_entries", ["prev_hash"])

    op.execute(
        """
        CREATE FUNCTION audit_entries_block_changes() RETURNS trigger AS $$
        BEGIN
            RAISE EXCEPTION 'audit_entries is append-only: % is not allowed', TG_OP
                USING ERRCODE = 'integrity_constraint_violation';
        END;
        $$ LANGUAGE plpgsql
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_entries_no_update_delete
        BEFORE UPDATE OR DELETE ON audit_entries
        FOR EACH ROW EXECUTE FUNCTION audit_entries_block_changes()
        """
    )
    op.execute(
        """
        CREATE TRIGGER audit_entries_no_truncate
        BEFORE TRUNCATE ON audit_entries
        FOR EACH STATEMENT EXECUTE FUNCTION audit_entries_block_changes()
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER audit_entries_no_truncate ON audit_entries")
    op.execute("DROP TRIGGER audit_entries_no_update_delete ON audit_entries")
    op.execute("DROP FUNCTION audit_entries_block_changes()")
    op.drop_constraint("uq_audit_entries_prev_hash", "audit_entries", type_="unique")
