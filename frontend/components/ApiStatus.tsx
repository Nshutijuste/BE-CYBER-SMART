"use client";

import { useEffect, useState } from "react";

type State = "checking" | "online" | "offline";

const looks: Record<State, { dot: string; text: string }> = {
  checking: { dot: "bg-slate-400", text: "Checking the API..." },
  online: { dot: "bg-brand-lime", text: "API connected" },
  offline: { dot: "bg-red-500", text: "API offline" },
};

// Temporary developer badge. We remove it before release.
export default function ApiStatus() {
  const [state, setState] = useState<State>("checking");

  useEffect(() => {
    fetch("/api/v1/health")
      .then((response) => setState(response.ok ? "online" : "offline"))
      .catch(() => setState("offline"));
  }, []);

  const look = looks[state];
  return (
    <p
      role="status"
      className="fixed bottom-4 left-4 z-50 flex items-center gap-2 rounded-full bg-white/95 px-4 py-2 text-sm font-semibold text-brand-navy shadow-lg ring-1 ring-black/10"
    >
      <span className={`size-2.5 rounded-full ${look.dot}`} aria-hidden="true" />
      {look.text}
    </p>
  );
}
