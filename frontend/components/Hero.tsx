import Image from "next/image";
import { getDictionary } from "@/i18n/server";

const focus =
  "focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-blue";

export default async function Hero() {
  const { t } = await getDictionary();

  return (
    <section className="relative overflow-hidden bg-gradient-to-b from-slate-100 to-white">
      <div className="mx-auto grid max-w-6xl items-center gap-10 px-6 pb-44 pt-10 md:grid-cols-2 md:pb-60 md:pt-16">
        <div>
          <h1 className="font-display text-4xl font-extrabold leading-tight text-brand-navy md:text-5xl">
            {t.hero.title}
          </h1>
          <p className="mt-5 max-w-md text-lg text-slate-700">
            {t.hero.body}
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <a
              href="#"
              className={`rounded-lg bg-brand-blue px-6 py-3 font-semibold text-white hover:bg-brand-navy ${focus}`}
            >
              {t.hero.check}
            </a>
            <a
              href="#"
              className={`rounded-lg border-2 border-brand-navy px-6 py-3 font-semibold text-brand-navy hover:bg-brand-navy hover:text-white ${focus}`}
            >
              {t.hero.scammed}
            </a>
          </div>
        </div>

        <div className="relative mx-auto aspect-square w-64 md:w-80">
          <div className="absolute inset-0 rounded-full border border-brand-blue/30" />
          <div className="absolute inset-3 rounded-full border border-dashed border-brand-lime/60" />
          <Image
            src="/brand/logo-brain.png"
            alt=""
            fill
            className="object-contain p-10"
            priority
          />
        </div>
      </div>

      <svg
        className="absolute inset-x-0 bottom-0 h-40 w-full md:h-56"
        viewBox="0 0 1440 300"
        preserveAspectRatio="none"
        aria-hidden="true"
      >
        <defs>
          <linearGradient id="blueWave" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0" stopColor="#1f35ff" />
            <stop offset="1" stopColor="#0a1450" />
          </linearGradient>
          <linearGradient id="greenSwoosh" x1="0" x2="1" y1="0" y2="0">
            <stop offset="0" stopColor="#4db814" />
            <stop offset="1" stopColor="#1f6b2a" />
          </linearGradient>
        </defs>
        <path
          d="M0 150 C 240 60, 480 60, 720 130 S 1200 230, 1440 110 L1440 300 L0 300 Z"
          fill="url(#blueWave)"
        />
        <path
          d="M0 300 C 300 200, 700 250, 1440 190 L1440 300 Z"
          fill="url(#greenSwoosh)"
        />
      </svg>
    </section>
  );
}