export const fetchApi = async (endpoint: string, options: RequestInit = {}) => {
  const token = localStorage.getItem("token");
  
  // We mock the user ID header since backend auth is mock simulation
  const userId = localStorage.getItem("userId") || "u1";

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    "x-user-id": userId,
    ...options.headers,
  };

  const apiBase = import.meta.env.VITE_API_URL || "/api";
  const response = await fetch(`${apiBase}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    const errorDetails = await response.json().catch(() => ({}));
    throw new Error(errorDetails.detail || "API request failed");
  }

  return response.json();
};
