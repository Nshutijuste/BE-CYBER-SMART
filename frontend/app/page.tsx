export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-4 p-8">
      <h1 className="text-4xl font-bold text-brand-navy dark:text-white">
        Be Cyber Smart
      </h1>
      <p className="text-lg">Learn. Check. Report. Stay safe.</p>
      <button className="rounded-lg bg-brand-blue px-6 py-3 font-semibold text-white">
        Check a message
      </button>
      <span className="rounded-full bg-brand-green px-4 py-1 text-sm text-white">
        English now, Kinyarwanda next
      </span>
    </main>
  );
}
