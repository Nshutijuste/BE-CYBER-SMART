import Image from "next/image";

export default function Logo({
  size = 40,
  onDark = false,
}: {
  size?: number;
  onDark?: boolean;
}) {
  return (
    <span className="inline-flex items-center gap-3">
      <span className={onDark ? "rounded-full bg-white p-1.5 shadow-sm" : ""}>
        <Image
          src="/brand/logo-brain.png"
          alt=""
          width={size}
          height={size}
          className="object-contain"
          priority
        />
      </span>
      <span className="font-display text-2xl font-extrabold leading-none tracking-tight">
        <span
          className={`mr-0.5 align-top text-sm font-extrabold italic ${
            onDark ? "text-brand-lime" : "text-brand-green"
          }`}
        >
          Be
        </span>
        <span className={onDark ? "text-white" : "text-brand-navy"}>Cyber</span>
        <span className={onDark ? "text-brand-lime" : "text-brand-green"}>Smart</span>
      </span>
    </span>
  );
}