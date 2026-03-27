const faqs = [
  {
    question: "Do I need an account to read stories?",
    answer: "You can browse published stories, but an account is needed to save progress and create content."
  },
  {
    question: "How do branching choices work?",
    answer: "Each node can have multiple choices. Every choice can move you to another node or end the story."
  },
  {
    question: "Can I create private drafts?",
    answer: "Yes. Keep stories unpublished while you build and only publish when ready."
  },
  {
    question: "Does TaleForge support AI-generated story paths?",
    answer: "Yes, creators can enable AI generation on choices and provide a fallback next node when needed."
  }
];

const FaqPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">Frequently Asked Questions</h1>
      </div>

      <div className="space-y-3">
        {faqs.map((item) => (
          <article key={item.question} className="glass-card rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">{item.question}</h2>
            <p className="mt-2 text-sm text-slate-700">{item.answer}</p>
          </article>
        ))}
      </div>
    </section>
  );
};

export default FaqPage;
