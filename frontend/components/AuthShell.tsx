import Header from "@/components/Header";

export default async function AuthShell({
  title,
  subtitle,
  children,
  icon,
}: {
  title: string;
  subtitle?: string;
  mode?: "login" | "register";
  children: React.ReactNode;
  icon?: React.ReactNode;
}) {
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
      <main className="relative z-10 flex flex-1 items-center justify-center px-4 pb-16 pt-28 sm:pt-32">
        <div className="w-full max-w-md rounded-[3px] border border-slate-200/90 bg-white/95 text-slate-900 shadow-2xl backdrop-blur-2xl p-6 sm:p-9 dark:border-blue-400/25 dark:bg-[#0b2b5c]/90 dark:shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8),inset_0_1px_0_0_rgba(255,255,255,0.18)] dark:text-white transition-colors duration-300">
          {/* Centered Security / Lock Icon */}
          <div className="mx-auto mb-4 flex size-14 items-center justify-center rounded-[3px] bg-slate-100 dark:bg-white/10 text-[#004181] dark:text-brand-lime shadow-xs">
            {icon ?? (
              <svg
                viewBox="0 0 24 24"
                className="size-7"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.2"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2" />
                <path d="M7 11V7a5 5 0 0 1 10 0v4" />
                <circle cx="12" cy="16" r="1.5" />
              </svg>
            )}
          </div>

          {/* Clean Title & Subtitle without top tabs */}
          <div className="text-center mb-6 sm:mb-8">
            <h1 className="text-2xl sm:text-[26px] font-extrabold tracking-tight text-slate-900 dark:text-white">
              {title}
            </h1>
            {subtitle && (
              <p className="mt-1.5 text-[15px] sm:text-base text-slate-500 dark:text-slate-300">
                {subtitle}
              </p>
            )}
          </div>

          {children}
        </div>
      </main>
    </div>
  );
}
