const sections = [
  {
    title: "Data We Collect",
    description:
      "We collect account details (username and email), story progress, and content you create in the platform."
  },
  {
    title: "How We Use Data",
    description:
      "Data is used to authenticate users, save story state, and improve product reliability and security."
  },
  {
    title: "Data Sharing",
    description:
      "We do not sell personal data. Information is shared only with infrastructure providers required to run the service."
  },
  {
    title: "Your Controls",
    description:
      "You can update account details, request support for account issues, and choose what stories you publish."
  }
];

const PrivacyPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">Privacy Policy</h1>
        <p className="mt-3 max-w-3xl text-sm text-slate-700">
          This summary explains how TaleForge handles your data. For legal requests, contact privacy@taleforge.app.
        </p>
      </div>

      <div className="space-y-3">
        {sections.map((section) => (
          <article key={section.title} className="glass-card rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">{section.title}</h2>
            <p className="mt-2 text-sm text-slate-700">{section.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default PrivacyPage;
