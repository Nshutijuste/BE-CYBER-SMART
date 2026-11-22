import ApiStatus from "@/components/ApiStatus";
import Features from "@/components/Features";
import Footer from "@/components/Footer";
import GoldenRule from "@/components/GoldenRule";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import HowItWorks from "@/components/HowItWorks";
import Reveal from "@/components/Reveal";
import WaveEdge from "@/components/WaveEdge";
import { getDictionary } from "@/i18n/server";

export default async function Home() {
  const { t } = await getDictionary();

  return (
    <>
      <a
        href="#start"
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-brand-lime focus:px-4 focus:py-2 focus:font-semibold focus:text-brand-navy"
      >
        {t.skip}
      </a>
      <Header />
      <main className="relative bg-[#000714] text-white overflow-hidden">
        <div className="relative flex min-h-dvh flex-col overflow-hidden bg-gradient-to-b from-[#000e26] via-[#00091c] to-[#000714] text-white">
          {/* Subtle cybernetic dot grid overlay */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute inset-0 bg-[radial-gradient(#ffffff0a_1px,transparent_1px)] [background-size:28px_28px] opacity-75"
          />

          {/* Fluid drifting cosmic glow spheres */}
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -left-36 top-1/4 z-0 size-[32rem] rounded-full bg-digital-500/25 blur-3xl motion-safe:animate-drift"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-28 top-16 z-0 size-[26rem] rounded-full bg-brand-lime/15 blur-3xl motion-safe:animate-drift [animation-delay:-9s]"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute left-1/3 bottom-12 z-0 size-80 rounded-full bg-calm/30 blur-3xl motion-safe:animate-drift [animation-delay:-4s]"
          />

          <Hero />
          <WaveEdge />
        </div>
        <Reveal>
          <Features />
        </Reveal>
        <Reveal>
          <HowItWorks />
        </Reveal>
        <Reveal>
          <GoldenRule />
        </Reveal>
      </main>
      <Footer />
      <ApiStatus />
    </>
  );
}
