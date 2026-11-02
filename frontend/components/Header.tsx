import LanguageSwitch from "@/components/LanguageSwitch";
import Logo from "@/components/Logo";
import { getDictionary } from "@/i18n/server";

export default async function Header() {
  const { locale, t } = await getDictionary();
  return (
    <header className="bg-slate-100">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Logo />
        <LanguageSwitch current={locale} label={t.header.language} />
      </div>
    </header>
  );
}