import Image from "next/image";

export default function Orb({ safe, risky }: { safe: string; risky: string }) {
  const chip =
    "absolute flex items-center gap-2 rounded-xl border border-white/30 bg-white/15 px-3 py-2 text-sm font-bold text-white shadow-lg backdrop-blur-md motion-safe:animate-float";

  return (
    <div className="relative mx-auto aspect-square w-64 sm:w-80 lg:w-[24rem]">
      <div className="absolute inset-0 rounded-full border border-white/20" />
      <div className="absolute inset-3 rounded-full border border-dashed border-brand-lime/60 motion-safe:animate-turn" />

      <div className="liquid inset-9" aria-hidden="true">
        <span className="liquid-sheen" />
      </div>

      <div className="absolute inset-[30%] grid place-items-center rounded-full bg-white/85 shadow-[inset_0_0_30px_rgba(0,102,255,0.25)]">
        <Image
          src="/brand/logo-brain.png"
          alt=""
          width={120}
          height={120}
          sizes="120px"
          style={{ height: "auto" }}
          className="w-3/4"
          priority
        />
      </div>

      <div aria-hidden="true" className={`${chip} -right-3 top-8`}>
        <span className="grid size-6 place-items-center rounded-full bg-brand-green text-white">
          ✓
        </span>
        <span>{safe}</span>
      </div>
      <div
        aria-hidden="true"
        className={`${chip} -left-3 bottom-10 [animation-delay:-3s]`}
      >
        <span className="grid size-6 place-items-center rounded-full bg-amber-400 text-brand-navy">
          !
        </span>
        <span>{risky}</span>
      </div>
    </div>
  );
}
