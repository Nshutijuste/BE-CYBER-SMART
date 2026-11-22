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

const input =
  "mt-2 h-11 w-full rounded-[2px] border border-slate-300 px-4 text-base text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-blue";
const label = "text-base font-semibold text-brand-navy";

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
    <form onSubmit={onSubmit} className="mt-6 space-y-5" noValidate>
      {step === "password" ? (
        <>
          <div>
            <label htmlFor="identifier" className={label}>
              {text.identifier}
            </label>
            <input
              id="identifier"
              className={input}
              value={identifier}
              onChange={(e) => setIdentifier(e.target.value)}
              autoComplete="username"
              autoCapitalize="none"
              spellCheck={false}
              required
            />
          </div>
          <div>
            <label htmlFor="password" className={label}>
              {text.password}
            </label>
            <input
              id="password"
              className={input}
              type={show ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
            <label className="mt-3 flex items-center gap-2 text-base text-slate-800">
              <input
                type="checkbox"
                checked={show}
                onChange={(e) => setShow(e.target.checked)}
                className="size-5"
              />
              {text.showPassword}
            </label>
          </div>
        </>
      ) : (
        <div>
          <p className="text-xl font-bold text-brand-navy">{text.codeTitle}</p>
          <label htmlFor="code" className={`${label} mt-3 block`}>
            {text.codeLabel}
          </label>
          <input
            id="code"
            className={`${input} tracking-[0.4em]`}
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
        <p role="alert" className="rounded-[2px] bg-red-50 p-3 text-sm font-medium text-red-800">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={sending}
        className="inline-flex min-h-11 w-full items-center justify-center rounded-[2px] bg-brand-blue px-6 text-base font-bold text-white hover:bg-brand-navy disabled:opacity-60 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-blue"
      >
        {sending ? text.wait : step === "password" ? text.logIn : text.verify}
      </button>

      <p className="text-base text-slate-700">
        {text.noAccount}{" "}
        <Link href="/register" className="font-semibold text-brand-blue underline">
          {text.registerLink}
        </Link>
      </p>
    </form>
  );
}
