import Features from "@/components/Features";
import Footer from "@/components/Footer";
import GoldenRule from "@/components/GoldenRule";
import Header from "@/components/Header";
import Hero from "@/components/Hero";
import HowItWorks from "@/components/HowItWorks";
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
          <Hero />
          <WaveEdge />
        </div>
        <Features />
        <HowItWorks />
        <GoldenRule />
      </main>
      <Footer />
    </>
  );
}