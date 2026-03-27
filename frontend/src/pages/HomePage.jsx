import StoryList from "../components/StoryList";

const HomePage = () => {
  return (
    <section className="space-y-6">
      <div className="glass-card rounded-3xl border border-white/40 p-8 shadow-soft">
        <h1 className="text-3xl font-bold tracking-tight text-ink">TaleForge</h1>
        <p className="mt-3 max-w-3xl text-slate-700">
          Explore branching narratives, make decisions that change outcomes, and build your own stories.
        </p>
      </div>

      <StoryList />
    </section>
  );
};

export default HomePage;
