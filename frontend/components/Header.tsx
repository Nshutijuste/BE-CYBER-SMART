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
    <header className="absolute inset-x-0 top-0 z-20">
      <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-5 sm:px-6">
        <Link
          href="/"
          aria-label="Be Cyber Smart"
          className="rounded-lg focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
        >
          <Logo size={36} onDark />
        </Link>

        <nav aria-label={t.nav.menu} className="hidden items-center gap-8 lg:flex">
          {links.map((l) => (
            <a
              key={l.href}
              href={l.href}
              className="text-lg font-medium text-white/90 underline-offset-8 hover:text-white hover:underline focus-visible:outline-2 focus-visible:outline-offset-4 focus-visible:outline-brand-lime"
            >
              {l.label}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-2 sm:gap-3">
          <LanguageMenu current={locale} label={t.header.changeLanguage} />
          <MobileMenu links={links} label={t.nav.menu} />
        </div>
      </div>
    </header>
  );
}