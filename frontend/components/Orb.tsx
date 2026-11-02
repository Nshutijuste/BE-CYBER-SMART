import Image from "next/image";

export default function Orb({ safe, risky }: { safe: string; risky: string }) {
  const chip =
    "absolute flex items-center gap-2 rounded-xl bg-white px-3 py-2 text-sm font-bold text-brand-navy shadow-lg motion-safe:animate-float";

  return (
    <div className="relative mx-auto aspect-square w-64 sm:w-80 lg:w-[22rem]">
      <div className="absolute inset-0 rounded-full border border-white/25" />
      <div className="absolute inset-4 rounded-full border border-dashed border-brand-lime/70" />
      <div
        className="absolute inset-10 rounded-full shadow-[0_0_80px_rgba(120,170,255,0.45)]"
        style={{ background: "radial-gradient(circle at 35% 30%, #ffffff, #cfe0ff)" }}
      />
      <Image
        src="/brand/logo-brain.png"
        alt=""
        fill
        className="object-contain p-[22%]"
        priority
      />

      <div aria-hidden="true" className={`${chip} -right-3 top-8`}>
        <span className="grid size-6 place-items-center rounded-full bg-brand-green text-white">
          ✓
        </span>
        {safe}
      </div>
      <div
        aria-hidden="true"
        className={`${chip} -left-3 bottom-10 [animation-delay:-3s]`}
      >
        <span className="grid size-6 place-items-center rounded-full bg-amber-400 text-brand-navy">
          !
        </span>
        {risky}
      </div>
    </div>
  );
}