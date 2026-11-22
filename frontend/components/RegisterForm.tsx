"use client";

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

const input =
  "mt-2 h-11 w-full rounded-[2px] border border-slate-300 px-4 text-base text-slate-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-blue";

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
      <p role="status" className="mt-6 rounded-[2px] bg-green-50 p-4 text-base font-semibold text-brand-green">
        {text.success}
      </p>
    );
  }

  return (
    <form onSubmit={onSubmit} className="mt-6 space-y-5" noValidate>
      <div>
        <label htmlFor="identifier" className="text-lg font-semibold text-brand-navy">
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
        <p className="mt-1 text-sm text-slate-600">{text.identifierHint}</p>
      </div>

      <div>
        <label htmlFor="password" className="text-lg font-semibold text-brand-navy">
          {text.password}
        </label>
        <input
          id="password"
          className={input}
          type={show ? "text" : "password"}
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="new-password"
          required
        />
        <p className="mt-1 text-sm text-slate-600">{text.passwordHint}</p>
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
        {sending ? text.wait : text.createAccount}
      </button>
    </form>
  );
}
