import Image from "next/image";

export default function Logo({
  size = 40,
  onDark,
}: {
  size?: number;
  onDark?: boolean;
}) {
  return (
    <span className="inline-flex items-center gap-2.5 sm:gap-3">
      <span className="rounded-full bg-white p-1 shadow-sm shrink-0">
        <Image
          src="/brand/logo-brain.png"
          alt=""
          width={size}
          height={size}
          style={{ width: "auto", height: "auto" }}
          className="object-contain"
          priority
        />
      </span>
      <span className="font-display text-lg sm:text-xl font-extrabold leading-none tracking-tight">
        <span className="mr-0.5 align-top text-xs font-extrabold italic text-brand-green dark:text-brand-lime">
          Be
        </span>
        <span className={onDark ? "text-white" : "text-slate-900 dark:text-white"}>Cyber</span>
        <span className="text-brand-blue dark:text-brand-lime">Smart</span>
      </span>
    </span>
  );
}