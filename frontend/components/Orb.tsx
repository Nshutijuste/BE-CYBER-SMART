import Image from "next/image";

export default function Orb({ safe, risky }: { safe: string; risky: string }) {
  const chip =
    "absolute flex items-center gap-2.5 rounded-[3px] border border-slate-300/80 bg-white/95 px-3.5 py-2 text-[15px] sm:text-[17px] font-bold text-slate-900 shadow-xl backdrop-blur-md dark:border-white/20 dark:bg-[#001433]/95 dark:text-white motion-safe:animate-float";

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
        <span className="grid size-5 place-items-center rounded-[3px] bg-brand-green text-xs font-black text-white shadow-sm">
          ✓
        </span>
        <span className="text-slate-900 dark:text-white font-bold">{safe}</span>
      </div>
      <div
        aria-hidden="true"
        className={`${chip} -left-3 bottom-10 [animation-delay:-3s]`}
      >
        <span className="grid size-5 place-items-center rounded-[3px] bg-amber-400 text-xs font-black text-[#001433] shadow-sm">
          !
        </span>
        <span className="text-slate-900 dark:text-white font-bold">{risky}</span>
      </div>
    </div>
  );
}
