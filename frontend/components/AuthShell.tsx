import Header from "@/components/Header";
import Link from "next/link";
import { getDictionary } from "@/i18n/server";

export default async function AuthShell({
  title,
  mode,
  children,
}: {
  title: string;
  mode?: "login" | "register";
  children: React.ReactNode;
}) {
  const { t } = await getDictionary();

  return (
    <div className="relative flex min-h-dvh flex-col overflow-hidden bg-[#d8e1eb] text-slate-900 dark:bg-gradient-to-b dark:from-[#002966] dark:via-[#001f4d] dark:to-[#001433] dark:text-white transition-colors duration-300">
      {/* Subtle cybernetic dot grid overlay */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(#00296615_1px,transparent_1px)] dark:bg-[radial-gradient(#ffffff0a_1px,transparent_1px)] [background-size:28px_28px] opacity-75"
      />
      {/* Ambient cosmic glow (dark theme only) */}
      <div
        aria-hidden="true"
        className="hidden dark:block pointer-events-none absolute -left-32 top-1/4 size-[28rem] rounded-full bg-brand-blue/20 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="hidden dark:block pointer-events-none absolute -right-32 bottom-10 size-[28rem] rounded-full bg-brand-lime/10 blur-3xl"
      />

      <Header />
      <main className="relative z-10 flex flex-1 items-center justify-center px-4 pb-16 pt-32">
        <div className="w-full max-w-md rounded-[3px] border border-slate-200/90 bg-white/95 text-slate-900 shadow-2xl backdrop-blur-2xl sm:p-9 dark:border-white/10 dark:bg-[#001433]/95 dark:text-white transition-colors duration-300">
          {/* Header tabs matching the reference screencast */}
          {mode ? (
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-5 mb-6">
              <div className="flex items-center gap-7">
                <Link
                  href="/login"
                  className={`relative text-2xl font-bold tracking-tight transition-colors ${
                    mode === "login"
                      ? "text-slate-900 dark:text-white"
                      : "text-slate-400 hover:text-slate-900 dark:text-slate-500 dark:hover:text-white"
                  }`}
                >
                  {t.login.navLogin}
                  {mode === "login" && (
                    <span className="absolute -bottom-[21px] left-0 right-0 h-1 rounded-full bg-[#004181] dark:bg-brand-lime" />
                  )}
                </Link>
                <Link
                  href="/register"
                  className={`relative text-2xl font-bold tracking-tight transition-colors ${
                    mode === "register"
                      ? "text-slate-900 dark:text-white"
                      : "text-slate-400 hover:text-slate-900 dark:text-slate-500 dark:hover:text-white"
                  }`}
                >
                  {t.login.navRegister}
                  {mode === "register" && (
                    <span className="absolute -bottom-[21px] left-0 right-0 h-1 rounded-full bg-[#004181] dark:bg-brand-lime" />
                  )}
                </Link>
              </div>

              <Link
                href="/"
                aria-label="Close"
                className="rounded-[3px] p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-white/10 dark:hover:text-white transition-colors"
              >
                <svg
                  viewBox="0 0 24 24"
                  className="size-5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </Link>
            </div>
          ) : (
            <div className="flex items-center justify-between border-b border-slate-200 dark:border-white/10 pb-5 mb-6">
              <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-white">{title}</h1>
              <Link
                href="/"
                aria-label="Close"
                className="rounded-[3px] p-1.5 text-slate-400 hover:bg-slate-100 hover:text-slate-900 dark:hover:bg-white/10 dark:hover:text-white transition-colors"
              >
                <svg
                  viewBox="0 0 24 24"
                  className="size-5"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  aria-hidden="true"
                >
                  <path d="M18 6L6 18M6 6l12 12" />
                </svg>
              </Link>
            </div>
          )}

          <h1 className="sr-only">{title}</h1>
          {children}
        </div>
      </main>
    </div>
  );
}
