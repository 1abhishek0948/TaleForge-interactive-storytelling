import { useEffect, useMemo, useState } from "react";

import api from "../services/api";

const normalizeListResponse = (data) => {
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.results)) return data.results;
  return [];
};

const CreatorPage = () => {
  const [storyForm, setStoryForm] = useState({ title: "", description: "", is_published: false });
  const [story, setStory] = useState(null);

  const [nodeForm, setNodeForm] = useState({ node_key: "", title: "", content: "", is_ending: false });
  const [choiceForm, setChoiceForm] = useState({
    node_id: "",
    text: "",
    next_node_id: "",
    order: 0,
    requires_ai_generation: false,
    ai_instruction: ""
  });

  const [nodes, setNodes] = useState([]);
  const [choices, setChoices] = useState([]);
  const [startingNodeId, setStartingNodeId] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const storyId = story?.id;

  const loadEditorData = async (id) => {
    const [nodesResponse, choicesResponse] = await Promise.all([
      api.get(`/nodes/?story=${id}&page_size=200`),
      api.get(`/choices/?story=${id}&page_size=200`)
    ]);
    setNodes(normalizeListResponse(nodesResponse.data));
    setChoices(normalizeListResponse(choicesResponse.data));
  };

  useEffect(() => {
    if (storyId) {
      loadEditorData(storyId).catch(() => setError("Failed to load story editor data."));
    }
  }, [storyId]);

  const nodeMap = useMemo(() => {
    const map = {};
    nodes.forEach((node) => {
      map[node.id] = node;
    });
    return map;
  }, [nodes]);

  const createStory = async (e) => {
    e.preventDefault();
    setError("");
    setMessage("");

    try {
      const response = await api.post("/stories/", storyForm);
      setStory(response.data);
      setMessage("Story created. Now add nodes and choices.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to create story.");
    }
  };

  const addNode = async (e) => {
    e.preventDefault();
    if (!storyId) return;

    setError("");
    setMessage("");
    try {
      await api.post("/nodes/", { ...nodeForm, story_id: storyId });
      setNodeForm({ node_key: "", title: "", content: "", is_ending: false });
      await loadEditorData(storyId);
      setMessage("Node added.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to add node.");
    }
  };

  const addChoice = async (e) => {
    e.preventDefault();
    if (!storyId) return;

    setError("");
    setMessage("");
    try {
      await api.post("/choices/", {
        ...choiceForm,
        next_node_id: choiceForm.next_node_id || null
      });
      setChoiceForm({
        node_id: "",
        text: "",
        next_node_id: "",
        order: 0,
        requires_ai_generation: false,
        ai_instruction: ""
      });
      await loadEditorData(storyId);
      setMessage("Choice added.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to add choice.");
    }
  };

  const updateStartingNode = async (e) => {
    e.preventDefault();
    if (!storyId || !startingNodeId) return;

    setError("");
    setMessage("");

    try {
      const response = await api.patch(`/stories/${storyId}/`, { starting_node_id: startingNodeId });
      setStory(response.data);
      setMessage("Starting node updated.");
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to update starting node.");
    }
  };

  return (
    <section className="space-y-6">
      <div className="glass-card rounded-2xl p-6 shadow-soft">
        <h1 className="text-2xl font-bold text-ink">Story Creator</h1>
        <p className="mt-2 text-sm text-slate-700">
          Build stories by creating a base story, then adding nodes and choices.
        </p>
      </div>

      {message && <div className="rounded-xl border border-emerald-300 bg-emerald-50 p-3 text-sm text-emerald-800">{message}</div>}
      {error && <div className="rounded-xl border border-red-300 bg-red-50 p-3 text-sm text-red-700">{error}</div>}

      <form onSubmit={createStory} className="glass-card space-y-3 rounded-2xl p-5 shadow-soft">
        <h2 className="text-lg font-semibold text-dusk">1) Create Story</h2>
        <input
          required
          placeholder="Story title"
          className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
          value={storyForm.title}
          onChange={(e) => setStoryForm((prev) => ({ ...prev, title: e.target.value }))}
        />
        <textarea
          placeholder="Story description"
          className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
          value={storyForm.description}
          onChange={(e) => setStoryForm((prev) => ({ ...prev, description: e.target.value }))}
        />
        <label className="flex items-center gap-2 text-sm text-slate-700">
          <input
            type="checkbox"
            checked={storyForm.is_published}
            onChange={(e) => setStoryForm((prev) => ({ ...prev, is_published: e.target.checked }))}
          />
          Publish immediately
        </label>
        <button className="rounded-lg bg-ink px-4 py-2 text-white hover:bg-dusk">Create Story</button>
      </form>

      {storyId && (
        <>
          <form onSubmit={addNode} className="glass-card space-y-3 rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">2) Add Story Node</h2>
            <input
              required
              placeholder="Node key (e.g. start, cave_entry)"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={nodeForm.node_key}
              onChange={(e) => setNodeForm((prev) => ({ ...prev, node_key: e.target.value }))}
            />
            <input
              placeholder="Node title"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={nodeForm.title}
              onChange={(e) => setNodeForm((prev) => ({ ...prev, title: e.target.value }))}
            />
            <textarea
              required
              placeholder="Narrative content"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={nodeForm.content}
              onChange={(e) => setNodeForm((prev) => ({ ...prev, content: e.target.value }))}
            />
            <label className="flex items-center gap-2 text-sm text-slate-700">
              <input
                type="checkbox"
                checked={nodeForm.is_ending}
                onChange={(e) => setNodeForm((prev) => ({ ...prev, is_ending: e.target.checked }))}
              />
              Mark as ending node
            </label>
            <button className="rounded-lg bg-ink px-4 py-2 text-white hover:bg-dusk">Add Node</button>
          </form>

          <form onSubmit={updateStartingNode} className="glass-card space-y-3 rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">3) Set Starting Node</h2>
            <select
              required
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={startingNodeId}
              onChange={(e) => setStartingNodeId(e.target.value)}
            >
              <option value="">Select starting node</option>
              {nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.node_key} {node.title ? `(${node.title})` : ""}
                </option>
              ))}
            </select>
            <button className="rounded-lg bg-ink px-4 py-2 text-white hover:bg-dusk">Save Starting Node</button>
          </form>

          <form onSubmit={addChoice} className="glass-card space-y-3 rounded-2xl p-5 shadow-soft">
            <h2 className="text-lg font-semibold text-dusk">4) Add Choice</h2>

            <select
              required
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={choiceForm.node_id}
              onChange={(e) => setChoiceForm((prev) => ({ ...prev, node_id: e.target.value }))}
            >
              <option value="">From node</option>
              {nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.node_key}
                </option>
              ))}
            </select>

            <input
              required
              placeholder="Choice text"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={choiceForm.text}
              onChange={(e) => setChoiceForm((prev) => ({ ...prev, text: e.target.value }))}
            />

            <select
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={choiceForm.next_node_id}
              onChange={(e) => setChoiceForm((prev) => ({ ...prev, next_node_id: e.target.value }))}
            >
              <option value="">To node (optional)</option>
              {nodes.map((node) => (
                <option key={node.id} value={node.id}>
                  {node.node_key}
                </option>
              ))}
            </select>

            <input
              type="number"
              placeholder="Display order"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={choiceForm.order}
              onChange={(e) => setChoiceForm((prev) => ({ ...prev, order: Number(e.target.value) }))}
            />

            <label className="flex items-center gap-2 text-sm text-slate-700">
              <input
                type="checkbox"
                checked={choiceForm.requires_ai_generation}
                onChange={(e) =>
                  setChoiceForm((prev) => ({
                    ...prev,
                    requires_ai_generation: e.target.checked
                  }))
                }
              />
              Generate next node with AI before optional fallback node
            </label>

            <textarea
              placeholder="AI instruction (optional)"
              className="w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
              value={choiceForm.ai_instruction}
              onChange={(e) => setChoiceForm((prev) => ({ ...prev, ai_instruction: e.target.value }))}
            />

            <button className="rounded-lg bg-ink px-4 py-2 text-white hover:bg-dusk">Add Choice</button>
          </form>

          <div className="grid gap-4 lg:grid-cols-2">
            <div className="glass-card rounded-2xl p-5 shadow-soft">
              <h3 className="mb-3 text-lg font-semibold text-dusk">Nodes ({nodes.length})</h3>
              <ul className="space-y-2 text-sm text-slate-700">
                {nodes.map((node) => (
                  <li key={node.id} className="rounded-lg border border-slate-200 bg-white/60 p-2">
                    <div className="font-medium">{node.node_key}</div>
                    <div>{node.title || "Untitled"}</div>
                  </li>
                ))}
              </ul>
            </div>

            <div className="glass-card rounded-2xl p-5 shadow-soft">
              <h3 className="mb-3 text-lg font-semibold text-dusk">Choices ({choices.length})</h3>
              <ul className="space-y-2 text-sm text-slate-700">
                {choices.map((choice) => (
                  <li key={choice.id} className="rounded-lg border border-slate-200 bg-white/60 p-2">
                    <div className="font-medium">{choice.text}</div>
                    <div>
                      {nodeMap[choice.node]?.node_key || choice.node} - {choice.next_node_key || "END"}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </>
      )}
    </section>
  );
};

export default CreatorPage;
