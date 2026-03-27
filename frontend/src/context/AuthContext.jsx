import { createContext, useContext, useEffect, useMemo, useState } from "react";

import api, { clearTokens, getAccessToken, getRefreshToken, setTokens } from "../services/api";

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchMe = async () => {
    try {
      const response = await api.get("/auth/me/");
      setUser(response.data);
    } catch {
      clearTokens();
      setUser(null);
    }
  };

  useEffect(() => {
    const init = async () => {
      if (getAccessToken()) {
        await fetchMe();
      }
      setLoading(false);
    };

    init();
  }, []);

  const login = async (username, password) => {
    const response = await api.post("/auth/token/", { username, password });
    setTokens(response.data);
    await fetchMe();
  };

  const signup = async ({ username, email, password }) => {
    await api.post("/auth/signup/", { username, email, password });
  };

  const logout = async () => {
    const refresh = getRefreshToken();
    try {
      if (refresh) {
        await api.post("/auth/logout/", { refresh });
      }
    } catch {
      // Local token clear is enough when refresh is already invalid.
    }

    clearTokens();
    setUser(null);
  };

  const value = useMemo(
    () => ({
      user,
      loading,
      login,
      signup,
      logout,
      isAuthenticated: Boolean(user)
    }),
    [user, loading]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider");
  }
  return context;
};
