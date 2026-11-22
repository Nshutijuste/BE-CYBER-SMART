import Logo from "@/components/Logo";
import { getDictionary } from "@/i18n/server";

export default async function Footer() {
  const { t } = await getDictionary();

  return (
    <footer className="relative bg-[#d0dbe6] border-t border-slate-300 dark:bg-[#000e24] dark:border-white/10 px-6 py-12 transition-colors duration-300">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 sm:flex-row sm:items-center sm:justify-between">
        <Logo size={36} />
        <p className="text-base text-slate-600 dark:text-slate-400 font-medium">{t.footer.tagline}</p>
      </div>
    </footer>
  );
}
