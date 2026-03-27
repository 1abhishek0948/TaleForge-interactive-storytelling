import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const SignupPage = () => {
  const { signup, login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await signup(form);
      await login(form.username, form.password);
      navigate("/");
    } catch (err) {
      const firstError = err?.response?.data && Object.values(err.response.data)[0];
      setError(Array.isArray(firstError) ? firstError[0] : firstError || "Signup failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="mx-auto max-w-md">
      <form onSubmit={onSubmit} className="glass-card space-y-4 rounded-2xl p-6 shadow-soft">
        <h1 className="text-2xl font-bold text-ink">Create Account</h1>

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
          Email
          <input
            type="email"
            required
            className="mt-1 w-full rounded-lg border border-slate-300 bg-white px-3 py-2"
            value={form.email}
            onChange={(e) => setForm((prev) => ({ ...prev, email: e.target.value }))}
          />
        </label>

        <label className="block text-sm font-medium text-slate-700">
          Password (min 8 chars)
          <input
            type="password"
            required
            minLength={8}
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
          {loading ? "Creating account..." : "Sign up"}
        </button>

        <p className="text-sm text-slate-600">
          Already have an account? <Link to="/login" className="font-semibold underline">Login</Link>
        </p>
      </form>
    </section>
  );
};

export default SignupPage;
