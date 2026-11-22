export default function WaveEdge() {
  return (
    <svg
      className="pointer-events-none absolute inset-x-0 bottom-0 h-28 w-full md:h-40"
      viewBox="0 0 1440 160"
      preserveAspectRatio="none"
      aria-hidden="true"
    >
      <path
        d="M0 74 C 240 134, 520 134, 760 84 S 1220 4, 1440 64"
        fill="none"
        stroke="#4db814"
        strokeWidth="6"
        strokeLinecap="round"
        vectorEffect="non-scaling-stroke"
        style={{ filter: "drop-shadow(0 0 10px rgba(77, 184, 20, 0.7))" }}
      />
      <path
        d="M0 100 C 240 150, 520 150, 760 106 S 1220 30, 1440 86 L1440 160 L0 160 Z"
        className="fill-[#f4f7fc] dark:fill-[#001433] transition-colors duration-300"
      />
    </svg>
  );
}
