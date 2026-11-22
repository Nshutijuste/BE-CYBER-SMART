"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";
import type en from "@/i18n/dictionaries/en.json";
import { ApiRequestError, postJson } from "@/lib/api";

type LoginText = typeof en.login;
type LoginResult = { status: "ok" | "mfa_required"; mfa_token: string | null };

function identifierField(value: string) {
  const v = value.trim();
  return v.includes("@") ? { email: v } : { phone: v.replace(/[\s()-]/g, "") };
}

function messageFor(error: unknown, text: LoginText): string {
  if (!(error instanceof ApiRequestError)) return text.errors.server_error;
  const base =
    error.code in text.errors
      ? text.errors[error.code as keyof typeof text.errors]
      : text.errors.server_error;
  if (error.code === "too_many_attempts" && error.retryAfter) {
    return `${base} ${text.retryIn.replace("{seconds}", String(error.retryAfter))}`;
  }
  return base;
}

const inputClass =
  "w-full rounded-[3px] border border-white/10 bg-white/[0.04] px-4 py-3 text-base text-white placeholder-slate-500 transition-all focus:border-brand-lime/80 focus:bg-white/[0.07] focus:outline-none focus:ring-1 focus:ring-brand-lime/80";
const labelClass = "text-xs sm:text-sm font-medium text-slate-400 mb-1.5 block";

export default function LoginForm({ text }: { text: LoginText }) {
  const router = useRouter();
  const [step, setStep] = useState<"password" | "code">("password");
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [code, setCode] = useState("");
  const [mfaToken, setMfaToken] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    setSending(true);
    try {
      if (step === "password") {
        const result = await postJson<LoginResult>("/auth/login", {
          ...identifierField(identifier),
          password,
        });
        if (result.status === "mfa_required" && result.mfa_token) {
          setMfaToken(result.mfa_token);
          setPassword("");
          setStep("code");
          return;
        }
      } else {
        await postJson("/auth/login/mfa", { mfa_token: mfaToken, code: code.trim() });
      }
      router.push("/account");
    } catch (e) {
      setError(messageFor(e, text));
    } finally {
      setSending(false);
    }
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5" noValidate>
      {step === "password" ? (
        <>
          <div>
            <label htmlFor="identifier" className={labelClass}>
              {text.identifier}
            </label>
            <input
              id="identifier"
              className={inputClass}
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              placeholder="hey@vino.costa"
              autoComplete="username"
              autoCapitalize="none"
              spellCheck={false}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className={labelClass}>
              {text.password}
            </label>
            <div className="relative">
              <input
                id="password"
                className={`${inputClass} pr-11`}
                type={show ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="At least 12 symbols..."
                autoComplete="current-password"
                required
              />
              <button
                type="button"
                onClick={() => setShow(!show)}
                aria-label={show ? "Hide password" : "Show password"}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors p-1"
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
                  {show ? (
                    <>
                      <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24" />
                      <line x1="1" y1="1" x2="23" y2="23" />
                    </>
                  ) : (
                    <>
                      <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z" />
                      <circle cx="12" cy="12" r="3" />
                    </>
                  )}
                </svg>
              </button>
            </div>
          </div>
        </>
      ) : (
        <div>
          <p className="text-xl font-bold text-white">{text.codeTitle}</p>
          <label htmlFor="code" className={`${labelClass} mt-3`}>
            {text.codeLabel}
          </label>
          <input
            id="code"
            className={`${inputClass} tracking-[0.4em]`}
            value={code}
            onChange={(e) => setCode(e.target.value.replace(/\D/g, "").slice(0, 6))}
            inputMode="numeric"
            autoComplete="one-time-code"
            maxLength={6}
            autoFocus
            required
          />
        </div>
      )}

      {error && (
        <p role="alert" className="rounded-[3px] bg-red-950/70 border border-red-500/40 p-3 text-sm font-medium text-red-200">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={sending}
        className="inline-flex min-h-12 w-full items-center justify-center rounded-[3px] bg-brand-lime px-6 text-base font-bold text-brand-navy shadow-[0_0_20px_rgba(77,184,20,0.3)] transition-all duration-300 hover:bg-white hover:text-brand-navy disabled:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-lime"
      >
        {sending ? text.wait : step === "password" ? text.logIn : text.verify}
      </button>

      <p className="text-center text-sm text-slate-400">
        {text.noAccount}{" "}
        <Link href="/register" className="font-semibold text-brand-lime hover:underline">
          {text.registerLink}
        </Link>
      </p>
    </form>
  );
}
