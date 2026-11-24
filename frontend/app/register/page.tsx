import AuthShell from "@/components/AuthShell";
import RegisterForm from "@/components/RegisterForm";
import { getDictionary } from "@/i18n/server";

export default async function RegisterPage() {
  const { t } = await getDictionary();
  return (
    <AuthShell
      title="BeCyberSmart"
      subtitle={t.auth.registerTitle}
    >
      <RegisterForm text={t.auth} />
    </AuthShell>
  );
}
