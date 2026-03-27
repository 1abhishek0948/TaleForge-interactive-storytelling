const helpTopics = [
  {
    title: "Getting Started",
    points: [
      "Create an account or log in.",
      "Browse stories from the home page.",
      "Open a story and choose your path."
    ]
  },
  {
    title: "Account & Security",
    points: [
      "Keep your password secure.",
      "Log out on shared devices.",
      "Contact support if you suspect account misuse."
    ]
  },
  {
    title: "Creating Stories",
    points: [
      "Create a story from the creator page.",
      "Add nodes and connect them with choices.",
      "Set a starting node and publish when ready."
    ]
  }
];

const HelpCenterPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">Help Center</h1>
        <p className="mt-3 max-w-3xl text-slate-700">Quick guides to help you use TaleForge smoothly.</p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {helpTopics.map((topic) => (
          <article key={topic.title} className="glass-card rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">{topic.title}</h2>
            <ul className="mt-3 space-y-2 text-sm text-slate-700">
              {topic.points.map((point) => (
                <li key={point} className="flex gap-2">
                  <span className="mt-1 h-2 w-2 rounded-full bg-amber-500" />
                  <span>{point}</span>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </section>
  );
};

export default HelpCenterPage;
