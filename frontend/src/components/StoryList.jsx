import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../services/api";

const normalizeListResponse = (data) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
};

const StoryList = () => {
  const [stories, setStories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadStories = async () => {
      try {
        const response = await api.get("/stories/");
        setStories(normalizeListResponse(response.data));
      } catch (err) {
        setError(err?.response?.data?.detail || "Failed to load stories.");
      } finally {
        setLoading(false);
      }
    };

    loadStories();
  }, []);

  if (loading) {
    return <div className="glass-card rounded-2xl p-6 text-slate-600 shadow-soft">Loading stories...</div>;
  }

  if (error) {
    return <div className="glass-card rounded-2xl p-6 text-red-600 shadow-soft">{error}</div>;
  }

  if (!stories.length) {
    return <div className="glass-card rounded-2xl p-6 text-slate-700 shadow-soft">No stories available yet.</div>;
  }

  return (
    <section className="grid gap-5 md:grid-cols-2">
      {stories.map((story, index) => (
        <article
          key={story.id}
          className="glass-card fade-in rounded-2xl border border-white/30 p-5 shadow-soft"
          style={{ animationDelay: `${index * 70}ms` }}
        >
          <div className="mb-4 flex items-center justify-between">
            <h2 className="text-xl font-bold text-ink">{story.title}</h2>
            <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-800">
              {story.is_published ? "Published" : "Draft"}
            </span>
          </div>

          <p className="mb-4 min-h-16 text-sm leading-relaxed text-slate-700">
            {story.description || "No description provided."}
          </p>

          <div className="flex items-center justify-between text-xs text-slate-500">
            <span>By {story.creator?.username || "Unknown"}</span>
            <Link
              to={`/stories/${story.id}`}
              className="rounded-lg bg-ink px-3 py-2 text-sm font-semibold text-white transition hover:bg-dusk"
            >
              Read Story
            </Link>
          </div>
        </article>
      ))}
    </section>
  );
};

export default StoryList;
