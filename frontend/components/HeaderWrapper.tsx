"use client";

import { useEffect, useState } from "react";

export default function HeaderWrapper({
  children,
}: {
  children: React.ReactNode;
}) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };
    handleScroll();
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-40 w-full transition-all duration-300 backdrop-blur-xl border-b ${
        scrolled
          ? "border-slate-300/80 bg-white/70 py-3.5 shadow-sm dark:border-white/10 dark:bg-[#001433]/85 sm:py-4"
          : "border-white/70 bg-white/50 py-5 shadow-xs dark:border-white/10 dark:bg-[#001433]/65 sm:py-6"
      }`}
    >
      {children}
    </header>
  );
}
