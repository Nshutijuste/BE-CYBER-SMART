import AccountPanel from "@/components/AccountPanel";
import AuthShell from "@/components/AuthShell";
import { getDictionary } from "@/i18n/server";

export default async function AccountPage() {
  const { t } = await getDictionary();
  return (
    <AuthShell title={t.account.title}>
      <AccountPanel text={t.account} />
    </AuthShell>
  );
}
