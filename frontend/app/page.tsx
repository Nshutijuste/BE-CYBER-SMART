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
        className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-50 focus:rounded-lg focus:bg-white focus:px-4 focus:py-2 focus:font-semibold focus:text-brand-navy"
      >
        {t.skip}
      </a>
      <Header />
      <main>
        <div className="relative flex min-h-dvh flex-col overflow-hidden bg-linear-to-br from-calm to-brand-navy text-white">
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -left-32 top-1/3 z-0 size-[28rem] rounded-full bg-digital-500/30 blur-3xl motion-safe:animate-drift"
          />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -right-24 top-10 z-0 size-80 rounded-full bg-brand-lime/15 blur-3xl motion-safe:animate-drift [animation-delay:-9s]"
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
