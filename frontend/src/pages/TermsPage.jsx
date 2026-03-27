const terms = [
  {
    title: "Acceptable Use",
    description:
      "Do not upload harmful, illegal, or abusive content. Respect other creators and community standards."
  },
  {
    title: "Content Ownership",
    description:
      "You retain ownership of the stories you create while granting TaleForge rights to host and display them in-app."
  },
  {
    title: "Service Availability",
    description:
      "We work to keep services available but cannot guarantee uninterrupted access at all times."
  },
  {
    title: "Account Responsibility",
    description: "You are responsible for actions taken from your account and for keeping credentials secure."
  }
];

const TermsPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">Terms of Service</h1>
        <p className="mt-3 max-w-3xl text-sm text-slate-700">
          By using TaleForge, you agree to these terms. This page is a concise product summary.
        </p>
      </div>

      <div className="space-y-3">
        {terms.map((item) => (
          <article key={item.title} className="glass-card rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">{item.title}</h2>
            <p className="mt-2 text-sm text-slate-700">{item.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default TermsPage;
