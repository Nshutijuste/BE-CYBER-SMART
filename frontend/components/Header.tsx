import LanguageMenu from "@/components/LanguageMenu";
import Logo from "@/components/Logo";
import MobileMenu from "@/components/MobileMenu";
import ThemeToggle from "@/components/ThemeToggle";
import { getDictionary } from "@/i18n/server";
import Link from "next/link";

export default async function Header() {
  const { locale, t } = await getDictionary();
  const links = [
    { href: "#what", label: t.nav.what },
    { href: "#how", label: t.nav.how },
    { href: "#rule", label: t.nav.rule },
  ];

  return (
    <header className="fixed inset-x-0 top-4 z-40 mx-auto w-full max-w-6xl px-4 sm:px-6 pointer-events-none">
      <div className="pointer-events-auto flex items-center justify-between gap-4 sm:gap-8 rounded-[2px] border border-slate-300/80 bg-white/85 dark:border-white/10 dark:bg-black/40 px-5 py-2.5 sm:px-6 sm:py-3 backdrop-blur-xl shadow-lg dark:shadow-[0_10px_30px_rgba(0,0,0,0.5)] transition-colors duration-300">
        <Link
          href="/"
          aria-label="Be Cyber Smart"
          className="shrink-0 rounded-[2px] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
        >
          <Logo size={32} />
        </Link>

        <nav aria-label={t.nav.menu} className="hidden items-center gap-8 lg:gap-10 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-sm sm:text-base font-medium text-slate-700 hover:text-brand-blue dark:text-slate-200 dark:hover:text-brand-lime transition-colors focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2.5 sm:gap-4 shrink-0">
          <Link
            href="/login"
            className="hidden text-sm sm:text-base font-semibold text-slate-700 hover:text-brand-blue dark:text-slate-200 dark:hover:text-white transition-colors md:inline"
          >
            {t.login.navLogin}
          </Link>
          <Link
            href="/register"
            className="hidden rounded-[2px] bg-brand-blue text-white shadow-sm hover:bg-brand-navy dark:bg-brand-lime dark:text-brand-navy dark:shadow-[0_0_15px_rgba(77,184,20,0.3)] dark:hover:bg-white px-4 py-1.5 text-xs sm:text-sm font-bold transition-all md:inline-block"
          >
            {t.login.navRegister}
          </Link>
          <LanguageMenu current={locale} label={t.header.changeLanguage} />
          <ThemeToggle />
          <MobileMenu links={links} label={t.nav.menu} />
        </div>
      </div>
    </header>
  );
}