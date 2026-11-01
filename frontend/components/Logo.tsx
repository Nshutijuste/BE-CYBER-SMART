import Image from "next/image";

export default function Logo({ size = 40 }: { size?: number }) {
  return (
    <span className="inline-flex items-center gap-3">
      <Image
        src="/brand/logo-brain.png"
        alt=""
        width={size}
        height={size}
        className="object-contain"
        priority
      />
      <span className="font-display text-2xl font-extrabold leading-none tracking-tight">
        <span className="mr-0.5 align-top text-sm font-extrabold italic text-brand-green">
          Be
        </span>
        <span className="text-brand-navy">Cyber</span>
        <span className="text-brand-green">Smart</span>
      </span>
    </span>
  );
}