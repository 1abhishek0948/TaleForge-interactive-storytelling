import { useEffect, useMemo, useRef, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { useAuth } from "../context/AuthContext";
import api from "../services/api";

const StoryReader = () => {
  const { storyId } = useParams();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const [payload, setPayload] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] = useState(false);
  const [displayLanguage, setDisplayLanguage] = useState("original");
  const [translatedContent, setTranslatedContent] = useState(null);
  const [translateLoading, setTranslateLoading] = useState(false);
  const [translateError, setTranslateError] = useState("");
  const translationCacheRef = useRef(new Map());

  const node = payload?.node;
  const choices = node?.choices || [];

  const pathText = useMemo(() => payload?.progress?.path?.join(" -> ") || "No saved path yet", [payload]);

  const loadStory = async () => {
    try {
      setLoading(true);
      setError("");
      const response = await api.get(`/stories/${storyId}/read/`);
      setPayload(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to load story.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!payload?.story || displayLanguage === "original") {
      setTranslatedContent(null);
      setTranslateError("");
      return;
    }

    let isCancelled = false;

    const translateCurrentPayload = async () => {
      const cacheKey = `${storyId}:${payload?.node?.id || "none"}:${displayLanguage}`;
      if (translationCacheRef.current.has(cacheKey)) {
        const cachedValue = translationCacheRef.current.get(cacheKey);
        if (!isCancelled) {
          setTranslatedContent(cachedValue);
          setTranslateLoading(false);
          setTranslateError("");
        }
        return;
      }

      setTranslateLoading(true);
      setTranslateError("");

      try {
        const response = await api.post(`/stories/${storyId}/translate/`, {
          target_language: displayLanguage,
          node_id: payload?.node?.id || null
        });
        const translated = response.data;
        translationCacheRef.current.set(cacheKey, translated);

        if (!isCancelled) {
          setTranslatedContent(translated);
        }
      } catch (err) {
        if (!isCancelled) {
          const message =
            err?.response?.data?.detail ||
            err?.response?.data?.target_language ||
            err?.message ||
            "Translation is unavailable right now. Showing original text.";
          setTranslateError(Array.isArray(message) ? message[0] : message);
          setTranslatedContent(null);
        }
      } finally {
        if (!isCancelled) {
          setTranslateLoading(false);
        }
      }
    };

    translateCurrentPayload();

    return () => {
      isCancelled = true;
    };
  }, [payload, displayLanguage]);

  useEffect(() => {
    loadStory();
  }, [storyId]);

  const ensureSession = async () => {
    const response = await api.post(`/stories/${storyId}/start/`);
    setPayload(response.data);
  };

  const handleChoice = async (choiceId) => {
    if (!isAuthenticated) {
      navigate("/login", { state: { fromStory: storyId } });
      return;
    }

    try {
      setActionLoading(true);
      if (!payload?.progress) {
        await ensureSession();
      }
      const response = await api.post(`/stories/${storyId}/choose/`, { choice_id: choiceId });
      setPayload(response.data);
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to apply your choice.");
    } finally {
      setActionLoading(false);
    }
  };

  const restartStory = async () => {
    if (!isAuthenticated) {
      navigate("/login", { state: { fromStory: storyId } });
      return;
    }

    try {
      setActionLoading(true);
      const response = await api.post(`/stories/${storyId}/start/`);
      setPayload(response.data);
      setError("");
    } catch (err) {
      setError(err?.response?.data?.detail || "Unable to restart story.");
    } finally {
      setActionLoading(false);
    }
  };

  if (loading) {
    return <div className="glass-card rounded-2xl p-6 shadow-soft">Loading story scene...</div>;
  }

  if (error) {
    return (
      <div className="glass-card space-y-4 rounded-2xl p-6 shadow-soft">
        <p className="text-red-600">{error}</p>
        <button onClick={loadStory} className="rounded-lg bg-ink px-3 py-2 text-white">
          Retry
        </button>
      </div>
    );
  }

  if (!payload?.story) {
    return <div className="glass-card rounded-2xl p-6 shadow-soft">Story not found.</div>;
  }

  const storyTitle = translatedContent?.story_title || payload.story.title;
  const storyDescription = translatedContent?.story_description || payload.story.description;
  const sceneTitle = translatedContent?.node_title || (node?.title || (node ? `Scene: ${node.node_key}` : ""));
  const sceneContent = translatedContent?.node_content || node?.content;
  const translatedChoiceMap = (translatedContent?.choices || []).reduce((accumulator, item) => {
    if (item?.id) accumulator[item.id] = item.text;
    return accumulator;
  }, {});

  return (
    <section className="space-y-5">
      <div className="glass-card rounded-2xl border border-white/30 p-6 shadow-soft">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-2xl font-bold text-ink">{storyTitle}</h1>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-medium uppercase tracking-wide text-slate-500">Translate</span>
            <button
              onClick={() => setDisplayLanguage("en")}
              className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                displayLanguage === "en"
                  ? "bg-ink text-white"
                  : "border border-slate-300 bg-white/80 text-slate-700 hover:border-slate-500"
              }`}
            >
              English
            </button>
            <button
              onClick={() => setDisplayLanguage("hi")}
              className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                displayLanguage === "hi"
                  ? "bg-ink text-white"
                  : "border border-slate-300 bg-white/80 text-slate-700 hover:border-slate-500"
              }`}
            >
              Hindi
            </button>
            <button
              onClick={() => setDisplayLanguage("original")}
              className={`rounded-full px-3 py-1 text-xs font-semibold transition ${
                displayLanguage === "original"
                  ? "bg-ink text-white"
                  : "border border-slate-300 bg-white/80 text-slate-700 hover:border-slate-500"
              }`}
            >
              Original
            </button>
          </div>
        </div>
        <p className="text-sm text-slate-600">{storyDescription}</p>
        {translateLoading && displayLanguage !== "original" && (
          <p className="mt-2 text-xs text-slate-500">Translating story text...</p>
        )}
        {translateError && <p className="mt-2 text-xs text-amber-700">{translateError}</p>}
      </div>

      {!isAuthenticated && (
        <div className="rounded-xl border border-amber-300 bg-amber-50 p-4 text-sm text-amber-900">
          Login is required to make decisions and save progress.
          <Link to="/login" className="ml-2 font-semibold underline">
            Login now
          </Link>
        </div>
      )}

      <article className="glass-card rounded-2xl border border-white/30 p-6 shadow-soft fade-in">
        {node ? (
          <>
            <h2 className="mb-4 text-xl font-semibold text-dusk">{sceneTitle}</h2>
            <p className="mb-6 whitespace-pre-wrap leading-7 text-slate-800">{sceneContent}</p>

            {payload.completed ? (
              <div className="space-y-3">
                <p className="font-semibold text-mint">Story completed.</p>
                <button
                  onClick={restartStory}
                  disabled={actionLoading}
                  className="rounded-lg bg-ink px-4 py-2 text-white transition hover:bg-dusk disabled:opacity-50"
                >
                  Restart Story
                </button>
              </div>
            ) : choices.length ? (
              <div className="grid gap-3">
                {choices.map((choice) => (
                  <button
                    key={choice.id}
                    onClick={() => handleChoice(choice.id)}
                    disabled={actionLoading}
                    className="rounded-lg border border-slate-300 bg-white/70 px-4 py-3 text-left text-sm font-medium text-slate-800 transition hover:border-ember hover:bg-amber-50 disabled:opacity-60"
                  >
                    {translatedChoiceMap[choice.id] || choice.text}
                  </button>
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                <p className="text-slate-700">No further choices in this scene.</p>
                <button
                  onClick={restartStory}
                  disabled={actionLoading}
                  className="rounded-lg bg-ink px-4 py-2 text-white transition hover:bg-dusk disabled:opacity-50"
                >
                  Start Over
                </button>
              </div>
            )}
          </>
        ) : (
          <div className="space-y-3">
            <p className="text-slate-700">No active node yet.</p>
            <button
              onClick={restartStory}
              disabled={!isAuthenticated || actionLoading}
              className="rounded-lg bg-ink px-4 py-2 text-white transition hover:bg-dusk disabled:opacity-50"
            >
              Start Story
            </button>
          </div>
        )}
      </article>

      <div className="glass-card rounded-2xl border border-white/30 p-4 text-xs text-slate-600 shadow-soft">
        <span className="font-semibold text-slate-700">Path:</span> {pathText}
      </div>
    </section>
  );
};

export default StoryReader;
