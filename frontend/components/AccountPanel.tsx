"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import type en from "@/i18n/dictionaries/en.json";
import { getJson, postJson } from "@/lib/api";

type AccountText = typeof en.account;
type Me = { id: string; role: string; permissions: string[]; mfa_verified: boolean };

export default function AccountPanel({ text }: { text: AccountText }) {
  const router = useRouter();
  const [me, setMe] = useState<Me | null>(null);

  useEffect(() => {
    getJson<Me>("/me")
      .then(setMe)
      .catch(() => router.replace("/login"));
  }, [router]);

  async function logOut() {
    await postJson("/auth/logout").catch(() => undefined);
    router.replace("/login");
  }

  if (!me) {
    return (
      <p role="status" className="mt-6 text-lg text-slate-700">
        {text.loading}
      </p>
    );
  }

  return (
    <div className="mt-6 space-y-5 text-lg text-slate-800">
      <p>
        <span className="font-semibold text-brand-navy">{text.role}:</span> {me.role}
      </p>
      <p>
        <span className="font-semibold text-brand-navy">{text.secondStep}:</span>{" "}
        {me.mfa_verified ? text.on : text.off}
      </p>
      <div>
        <p className="font-semibold text-brand-navy">{text.permissions}:</p>
        <ul className="mt-2 list-disc space-y-1 pl-6">
          {me.permissions.map((permission) => (
            <li key={permission}>{permission}</li>
          ))}
        </ul>
      </div>
      <button
        type="button"
        onClick={logOut}
        className="inline-flex min-h-12 items-center rounded-xl border-2 border-brand-navy px-6 text-lg font-bold text-brand-navy hover:bg-brand-navy hover:text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-blue"
      >
        {text.logOut}
      </button>
    </div>
  );
}
