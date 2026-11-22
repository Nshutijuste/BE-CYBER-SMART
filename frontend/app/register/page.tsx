import AuthShell from "@/components/AuthShell";
import RegisterForm from "@/components/RegisterForm";
import { getDictionary } from "@/i18n/server";

export default async function RegisterPage() {
  const { t } = await getDictionary();
  return (
    <AuthShell title={t.auth.registerTitle} mode="register">
      <RegisterForm text={t.auth} />
    </AuthShell>
  );
}
