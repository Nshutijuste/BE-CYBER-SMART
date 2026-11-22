import Header from "@/components/Header";
import Link from "next/link";

export default function AuthShell({
  title,
  mode = "login",
  children,
}: {
  title: string;
  mode?: "login" | "register";
  children: React.ReactNode;
}) {
  return (
    <div className="relative flex min-h-dvh flex-col overflow-hidden bg-gradient-to-b from-[#000e26] via-[#000819] to-[#000714] text-white">
      {/* Subtle cybernetic dot grid overlay */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(#ffffff0a_1px,transparent_1px)] [background-size:28px_28px] opacity-75"
      />
      {/* Ambient cosmic glow */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -left-32 top-1/4 size-[28rem] rounded-full bg-brand-blue/20 blur-3xl"
      />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 bottom-10 size-[28rem] rounded-full bg-brand-lime/10 blur-3xl"
      />

      <Header />
      <main className="relative z-10 flex flex-1 items-center justify-center px-4 pb-16 pt-32">
        <div className="w-full max-w-md rounded-[3px] border border-white/10 bg-[#0c121e]/90 p-7 shadow-[0_25px_60px_-15px_rgba(0,0,0,0.8)] backdrop-blur-2xl sm:p-9 text-white">
          {/* Header tabs matching the reference screencast */}
          <div className="flex items-center justify-between border-b border-white/10 pb-5 mb-6">
            <div className="flex items-center gap-7">
              <Link
                href="/login"
                className={`relative text-2xl font-bold tracking-tight transition-colors ${
                  mode === "login"
                    ? "text-white"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Sign In
                {mode === "login" && (
                  <span className="absolute -bottom-[21px] left-0 right-0 h-1 rounded-full bg-gradient-to-r from-orange-500 to-amber-400" />
                )}
              </Link>
              <Link
                href="/register"
                className={`relative text-2xl font-bold tracking-tight transition-colors ${
                  mode === "register"
                    ? "text-white"
                    : "text-slate-400 hover:text-white"
                }`}
              >
                Join
                {mode === "register" && (
                  <span className="absolute -bottom-[21px] left-0 right-0 h-1 rounded-full bg-gradient-to-r from-orange-500 to-amber-400" />
                )}
              </Link>
            </div>

            <Link
              href="/"
              aria-label="Close"
              className="rounded-[3px] p-1.5 text-slate-400 hover:bg-white/10 hover:text-white transition-colors"
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

          <h1 className="sr-only">{title}</h1>
          {children}

          {/* Social login buttons row matching the reference screencast */}
          <div className="mt-7 pt-6 border-t border-white/10">
            <div className="grid grid-cols-4 gap-3">
              {/* Google */}
              <button
                type="button"
                aria-label="Sign in with Google"
                className="flex h-11 items-center justify-center rounded-[3px] border border-white/10 bg-white/[0.04] text-white hover:bg-white/10 transition-colors"
              >
                <svg className="size-5" viewBox="0 0 24 24">
                  <path
                    fill="#EA4335"
                    d="M12 5c1.6 0 3 .6 4.1 1.7l3.1-3.1C17.3 1.8 14.8 1 12 1 7.5 1 3.7 3.6 1.9 7.3l3.7 2.9C6.5 7.4 9 5 12 5z"
                  />
                  <path
                    fill="#4285F4"
                    d="M23.5 12.3c0-.8-.1-1.7-.2-2.3H12v4.5h6.5c-.3 1.5-1.1 2.8-2.4 3.7l3.7 2.9c2.2-2 3.7-5 3.7-8.8z"
                  />
                  <path
                    fill="#FBBC05"
                    d="M5.6 14.8c-.2-.7-.4-1.5-.4-2.8s.2-2.1.4-2.8L1.9 6.3C.7 8.7 0 10.8 0 12s.7 3.3 1.9 5.7l3.7-2.9z"
                  />
                  <path
                    fill="#34A853"
                    d="M12 23c3.2 0 6-1.1 8-3l-3.7-2.9c-1.1.7-2.5 1.2-4.3 1.2-3 0-5.5-2.4-6.4-5.2L1.9 16C3.7 19.7 7.5 23 12 23z"
                  />
                </svg>
              </button>

              {/* Apple */}
              <button
                type="button"
                aria-label="Sign in with Apple"
                className="flex h-11 items-center justify-center rounded-[3px] border border-white/10 bg-white/[0.04] text-white hover:bg-white/10 transition-colors"
              >
                <svg className="size-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.89c.66-.82 1.11-1.96.99-3.1-.96.04-2.13.64-2.82 1.45-.61.71-1.14 1.87-1 2.98 1.07.08 2.17-.51 2.83-1.33z" />
                </svg>
              </button>

              {/* X (Twitter) */}
              <button
                type="button"
                aria-label="Sign in with X"
                className="flex h-11 items-center justify-center rounded-[3px] border border-white/10 bg-white/[0.04] text-white hover:bg-white/10 transition-colors"
              >
                <svg className="size-4" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                </svg>
              </button>

              {/* Discord */}
              <button
                type="button"
                aria-label="Sign in with Discord"
                className="flex h-11 items-center justify-center rounded-[3px] border border-white/10 bg-white/[0.04] text-[#5865F2] hover:bg-white/10 transition-colors"
              >
                <svg className="size-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028c.462-.63.874-1.295 1.226-1.994.021-.041.001-.09-.041-.106a13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.894.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
