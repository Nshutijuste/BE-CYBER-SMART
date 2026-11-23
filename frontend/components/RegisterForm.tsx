"use client";

import Link from "next/link";
import { type FormEvent, useState } from "react";
import { ApiRequestError, postJson } from "@/lib/api";
import type en from "@/i18n/dictionaries/en.json";

type AuthText = typeof en.auth;

function identifierField(value: string) {
  const v = value.trim();
  return v.includes("@") ? { email: v } : { phone: v.replace(/[\s()-]/g, "") };
}

function messageFor(code: string, errors: AuthText["errors"]): string {
  return code in errors ? errors[code as keyof typeof errors] : errors.server_error;
}

const inputClass =
  "w-full rounded-[3px] border border-slate-300 bg-white px-4 py-3 text-[17px] text-slate-900 placeholder:text-[15px] placeholder-slate-400 shadow-sm transition-all focus:border-[#004181] focus:outline-none focus:ring-1 focus:ring-[#004181] dark:border-white/15 dark:bg-white/[0.05] dark:text-white dark:placeholder-slate-500 dark:focus:border-brand-lime dark:focus:ring-brand-lime";
const labelClass = "text-[13px] sm:text-[15px] font-semibold text-slate-700 dark:text-slate-300 mb-1.5 block";

export default function RegisterForm({ text }: { text: AuthText }) {
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [show, setShow] = useState(false);
  const [sending, setSending] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError(null);
    if (password.length < 12) {
      setError(text.errors.password_short);
      return;
    }
    setSending(true);
    try {
      await postJson("/auth/register", { ...identifierField(identifier), password });
      setDone(true);
      setPassword("");
    } catch (e) {
      setError(messageFor(e instanceof ApiRequestError ? e.code : "server_error", text.errors));
    } finally {
      setSending(false);
    }
  }

  if (done) {
    return (
      <div className="space-y-4">
        <p role="status" className="rounded-[3px] bg-emerald-50 border border-emerald-200 p-4 text-[17px] font-semibold text-emerald-800 dark:bg-emerald-950/70 dark:border-emerald-500/40 dark:text-emerald-200">
          {text.success}
        </p>
        <Link
          href="/login"
          className="inline-flex min-h-12 w-full items-center justify-center rounded-[3px] bg-[#004181] hover:bg-[#003466] text-white px-6 text-[17px] font-bold shadow-md transition-colors"
        >
          Sign In Now
        </Link>
      </div>
    );
  }

  return (
    <form onSubmit={onSubmit} className="space-y-5" noValidate>
      <div>
        <label htmlFor="identifier" className={labelClass}>
          {text.identifier}
        </label>
        <input
          id="identifier"
          className={inputClass}
          value={identifier}
          onChange={(e) => setIdentifier(e.target.value)}
          placeholder="name@gmail.com "
          autoComplete="username"
          autoCapitalize="none"
          spellCheck={false}
          required
        />
        <p className="mt-1.5 text-[13px] text-slate-500 dark:text-slate-400">{text.identifierHint}</p>
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
            placeholder="At least 12 Characters"
            autoComplete="new-password"
            required
          />
          <button
            type="button"
            onClick={() => setShow(!show)}
            aria-label={show ? "Hide password" : "Show password"}
            className="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 dark:text-slate-400 dark:hover:text-white transition-colors p-1"
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
        <p className="mt-1.5 text-[13px] text-slate-500 dark:text-slate-400">{text.passwordHint}</p>
      </div>

      {error && (
        <p role="alert" className="rounded-[3px] bg-rose-50 border border-rose-200 p-3.5 text-[15px] font-medium text-rose-700 dark:bg-rose-950/70 dark:border-rose-500/40 dark:text-rose-200">
          {error}
        </p>
      )}

      <button
        type="submit"
        disabled={sending}
        className="inline-flex min-h-12 w-full items-center justify-center rounded-[3px] bg-[#004181] hover:bg-[#003466] text-white px-6 text-[17px] font-bold shadow-md transition-colors disabled:opacity-50"
      >
        {sending ? text.wait : text.createAccount}
      </button>

      <div className="pt-2">
        <p className="text-center text-[15px] text-slate-600 dark:text-slate-400">
          Already have an account?{" "}
          <Link
            href="/login"
            className="font-semibold text-[#004181] hover:underline dark:text-brand-lime"
          >
            Log in
          </Link>
        </p>
      </div>
    </form>
  );
}
