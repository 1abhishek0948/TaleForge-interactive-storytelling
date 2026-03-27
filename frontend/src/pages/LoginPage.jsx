import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const QUICK_DEMO_ACCOUNTS = [
  { label: "Demo User", username: "demo_user", password: "demoxyz12@" },
  { label: "Moderator", username: "moderator_user", password: "moderatorxyz34@" },
  { label: "Admin", username: "admin_user", password: "adminxyz56@" }
];

const LoginPage = () => {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await login(form.username, form.password);
      const redirectStoryId = location.state?.fromStory;
      navigate(redirectStoryId ? `/stories/${redirectStoryId}` : "/");
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid credentials.");
    } finally {
      setLoading(false);
    }
  };

  const fillDemoCredentials = (username, password) => {
    setError("");
    setForm({ username, password });
  };

  return (
    <section className="mx-auto max-w-md space-y-4">
      <div className="glass-card rounded-2xl border border-amber-200/80 bg-amber-50/75 p-4 shadow-soft">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-amber-900">Quick Demo Accounts</h2>
        <p className="mt-1 text-sm text-amber-900/90">
          Click any account to auto-fill credentials.
        </p>
        <div className="mt-3 space-y-2">
          {QUICK_DEMO_ACCOUNTS.map((account) => (
            <button
              type="button"
              key={account.username}
              onClick={() => fillDemoCredentials(account.username, account.password)}
              className="flex w-full items-center justify-between rounded-lg border border-amber-300/80 bg-white/90 px-3 py-2 text-left transition hover:border-amber-500"
            >
              <span className="font-semibold text-ink">{account.label}</span>
              <span className="text-xs text-slate-600">
                {account.username} / {account.password}
              </span>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={onSubmit} className="glass-card space-y-4 rounded-2xl p-6 shadow-soft">
        <h1 className="text-2xl font-bold text-ink">Login</h1>

        <label className="block text-sm font-medium text-slate-700">
          Username
          <input
            type="text"
            required
            className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
            value={form.username}
            onChange={(e) => setForm((prev) => ({ ...prev, username: e.target.value }))}
          />
        </label>

        <label className="block text-sm font-medium text-slate-700">
          Password
          <input
            type="password"
            required
            className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
            value={form.password}
            onChange={(e) => setForm((prev) => ({ ...prev, password: e.target.value }))}
          />
        </label>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          className="w-full rounded-lg bg-ink px-4 py-2 font-semibold text-white transition hover:bg-dusk disabled:opacity-60"
        >
          {loading ? "Logging in..." : "Login"}
        </button>

        <p className="text-sm text-slate-600">
          New here? <Link to="/signup" className="font-semibold underline">Create an account</Link>
        </p>
      </form>
    </section>
  );
};

export default LoginPage;
