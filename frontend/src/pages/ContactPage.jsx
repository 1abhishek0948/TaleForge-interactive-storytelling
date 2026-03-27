const contactCards = [
  {
    title: "General Support",
    value: "support@taleforge.app",
    detail: "Questions about your account, login, or reading experience."
  },
  {
    title: "Creator Support",
    value: "creators@taleforge.app",
    detail: "Help with publishing stories, branching logic, and creator tools."
  },
  {
    title: "Partnerships",
    value: "partners@taleforge.app",
    detail: "Collaboration requests, community events, and educational usage."
  }
];

const ContactPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">Contact Us</h1>
        <p className="mt-3 max-w-3xl text-slate-700">
          Reach out to the TaleForge team. We usually respond within 24-48 hours.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {contactCards.map((card) => (
          <article key={card.title} className="glass-card rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">{card.title}</h2>
            <a href={`mailto:${card.value}`} className="mt-2 block text-sm font-semibold text-ember hover:underline">
              {card.value}
            </a>
            <p className="mt-2 text-sm text-slate-700">{card.detail}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default ContactPage;
