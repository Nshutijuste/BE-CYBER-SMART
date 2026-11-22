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
      className={`fixed inset-x-0 top-0 z-40 w-full transition-all duration-300 ${
        scrolled
          ? "border-b border-slate-300/60 bg-[#d8e1eb]/90 py-3.5 shadow-sm backdrop-blur-xl dark:border-white/10 dark:bg-[#001433]/85 sm:py-4"
          : "border-b border-transparent bg-transparent py-5 sm:py-6"
      }`}
    >
      {children}
    </header>
  );
}
