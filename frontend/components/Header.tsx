import HeaderWrapper from "@/components/HeaderWrapper";
import LanguageMenu from "@/components/LanguageMenu";
import Logo from "@/components/Logo";
import MobileMenu from "@/components/MobileMenu";
import ThemeToggle from "@/components/ThemeToggle";
import { getDictionary } from "@/i18n/server";
import Link from "next/link";

export default async function Header() {
  const { locale, t } = await getDictionary();
  const links = [
    { href: "/#what", label: t.nav.what },
    { href: "/#how", label: t.nav.how },
    { href: "/#rule", label: t.nav.rule },
  ];

  return (
    <HeaderWrapper>
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-2 sm:gap-6 px-3.5 sm:px-8">
        <Link
          href="/"
          aria-label="Be Cyber Smart"
          className="shrink-0 rounded-[3px] focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
        >
          <Logo size={32} />
        </Link>

        <nav aria-label={t.nav.menu} className="hidden items-center gap-6 lg:gap-10 md:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-[17px] sm:text-[18px] font-medium text-slate-700 hover:text-[#004181] dark:text-slate-200 dark:hover:text-brand-lime transition-colors focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
          <Link
            href="/login"
            className="hidden text-[17px] sm:text-[18px] font-semibold text-slate-700 hover:text-[#004181] dark:text-slate-200 dark:hover:text-white transition-colors md:inline"
          >
            {t.login.navLogin}
          </Link>
          <Link
            href="/register"
            className="hidden rounded-[3px] bg-[#004181] hover:bg-[#003466] text-white px-5 py-2 text-[15px] sm:text-[16px] font-bold shadow-sm transition-colors md:inline-block"
          >
            {t.login.navRegister}
          </Link>
          <LanguageMenu current={locale} label={t.header.changeLanguage} />
          <ThemeToggle />
          <MobileMenu
            links={links}
            authLinks={[
              { href: "/login", label: t.login.navLogin },
              { href: "/register", label: t.login.navRegister, primary: true },
            ]}
            label={t.nav.menu}
          />
        </div>
      </div>
    </HeaderWrapper>
  );
}
