import AuthShell from "@/components/AuthShell";
import LoginForm from "@/components/LoginForm";
import { getDictionary } from "@/i18n/server";

export default async function LoginPage() {
  const { t } = await getDictionary();
  return (
    <AuthShell
      title="BeCyberSmart"
      subtitle={t.login.title === "Log in" ? "Log in to your account" : t.login.title}
    >
      <LoginForm text={t.login} />
    </AuthShell>
  );
}
