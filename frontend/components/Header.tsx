import LanguageMenu from "@/components/LanguageMenu";
import Logo from "@/components/Logo";
import MobileMenu from "@/components/MobileMenu";
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
      <div className="pointer-events-auto flex items-center justify-between gap-6 sm:gap-10 rounded-[2px] border border-white/10 bg-black/40 px-5 py-2.5 sm:px-6 sm:py-3 backdrop-blur-xl shadow-[0_10px_30px_rgba(0,0,0,0.5)]">
        <Link
          href="/"
          aria-label="Be Cyber Smart"
          className="shrink-0 rounded-[2px] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
        >
          <Logo size={32} onDark />
        </Link>

        <nav aria-label={t.nav.menu} className="hidden items-center gap-8 lg:gap-10 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-sm sm:text-base font-medium text-slate-200 transition-colors hover:text-brand-lime focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3 sm:gap-5 shrink-0">
          <Link href="/login" className="hidden text-sm sm:text-base font-semibold text-slate-200 transition-colors hover:text-white md:inline">
            {t.login.navLogin}
          </Link>
          <Link
            href="/register"
            className="hidden rounded-[2px] bg-brand-lime px-4 py-1.5 text-xs sm:text-sm font-bold text-brand-navy shadow-[0_0_15px_rgba(77,184,20,0.3)] transition-all hover:bg-white md:inline-block"
          >
            {t.login.navRegister}
          </Link>
          <LanguageMenu current={locale} label={t.header.changeLanguage} />
          <MobileMenu links={links} label={t.nav.menu} />
        </div>
      </div>
    </header>
  );
}