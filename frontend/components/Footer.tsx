import Logo from "@/components/Logo";
import { getDictionary } from "@/i18n/server";

export default async function Footer() {
  const { t } = await getDictionary();

  return (
    <footer className="bg-slate-100 px-6 py-10">
      <div className="mx-auto flex max-w-6xl flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <Logo size={32} />
        <p className="text-lg text-slate-700">{t.footer.tagline}</p>
      </div>
    </footer>
  );
}