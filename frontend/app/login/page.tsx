import AuthShell from "@/components/AuthShell";
import LoginForm from "@/components/LoginForm";
import { getDictionary } from "@/i18n/server";

export default async function LoginPage() {
  const { t } = await getDictionary();
  return (
    <AuthShell title={t.login.title}>
      <LoginForm text={t.login} />
    </AuthShell>
  );
}
