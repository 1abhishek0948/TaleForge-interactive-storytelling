const AboutPage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">About TaleForge</h1>
        <p className="mt-3 max-w-3xl text-slate-700">
          TaleForge is an interactive storytelling platform where readers shape outcomes through decisions and
          creators build rich branching narratives.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <article className="glass-card rounded-2xl p-5 shadow-soft">
          <h2 className="text-lg font-semibold text-dusk">Our Mission</h2>
          <p className="mt-2 text-sm text-slate-700">
            Make storytelling more participative by combining creative writing with meaningful reader choices.
          </p>
        </article>

        <article className="glass-card rounded-2xl p-5 shadow-soft">
          <h2 className="text-lg font-semibold text-dusk">For Readers</h2>
          <p className="mt-2 text-sm text-slate-700">
            Explore stories with multiple paths, revisit alternate endings, and save your progress.
          </p>
        </article>

        <article className="glass-card rounded-2xl p-5 shadow-soft">
          <h2 className="text-lg font-semibold text-dusk">For Creators</h2>
          <p className="mt-2 text-sm text-slate-700">
            Use the creator tools to design nodes, connect choices, and publish new interactive adventures.
          </p>
        </article>
      </div>
    </section>
  );
};

export default AboutPage;
