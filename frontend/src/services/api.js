import axios from "axios";

const fallbackApiBase =
  typeof window !== "undefined" ? `${window.location.origin}/api` : "http://localhost:8000/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || fallbackApiBase;

const ACCESS_KEY = "story_access_token";
const REFRESH_KEY = "story_refresh_token";

export const getAccessToken = () => localStorage.getItem(ACCESS_KEY);
export const getRefreshToken = () => localStorage.getItem(REFRESH_KEY);

export const setTokens = ({ access, refresh }) => {
  if (access) localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
};

export const clearTokens = () => {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
};

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  const token = getAccessToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let isRefreshing = false;
let refreshQueue = [];

const processQueue = (error, token = null) => {
  refreshQueue.forEach(({ resolve, reject }) => {
    if (error) {
      reject(error);
    } else {
      resolve(token);
    }
  });
  refreshQueue = [];
};

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status !== 401 || originalRequest?._retry) {
      return Promise.reject(error);
    }

    const refresh = getRefreshToken();
    if (!refresh) {
      clearTokens();
      return Promise.reject(error);
    }

    originalRequest._retry = true;

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        refreshQueue.push({ resolve, reject });
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`;
        return api(originalRequest);
      });
    }

    isRefreshing = true;

    try {
      const refreshResponse = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, { refresh });
      const newAccessToken = refreshResponse.data.access;
      setTokens({ access: newAccessToken, refresh: refreshResponse.data.refresh || refresh });
      processQueue(null, newAccessToken);
      originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
      return api(originalRequest);
    } catch (refreshError) {
      processQueue(refreshError);
      clearTokens();
      return Promise.reject(refreshError);
    } finally {
      isRefreshing = false;
    }
  }
);

export default api;
