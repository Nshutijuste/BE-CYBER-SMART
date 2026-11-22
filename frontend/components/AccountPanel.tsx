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
      <p role="status" className="mt-6 text-lg text-slate-600 dark:text-slate-300">
        {text.loading}
      </p>
    );
  }

  return (
    <div className="mt-6 space-y-5 text-base sm:text-lg text-slate-800 dark:text-slate-200">
      <p>
        <span className="font-semibold text-slate-900 dark:text-white">{text.role}:</span> {me.role}
      </p>
      <p>
        <span className="font-semibold text-slate-900 dark:text-white">{text.secondStep}:</span>{" "}
        {me.mfa_verified ? text.on : text.off}
      </p>
      <div>
        <p className="font-semibold text-slate-900 dark:text-white">{text.permissions}:</p>
        <ul className="mt-2 list-disc space-y-1 pl-6">
          {me.permissions.map((permission) => (
            <li key={permission}>{permission}</li>
          ))}
        </ul>
      </div>
      <button
        type="button"
        onClick={logOut}
        className="inline-flex min-h-11 items-center rounded-[3px] border border-slate-300 bg-white hover:bg-slate-100 text-slate-900 dark:border-white/20 dark:bg-white/5 dark:text-white dark:hover:bg-white/10 px-5 text-base font-bold shadow-sm transition-colors focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#0066ff]"
      >
        {text.logOut}
      </button>
    </div>
  );
}
