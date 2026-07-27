const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

function getAuthHeaders() {
  const headers = { "Content-Type": "application/json" };
  const token = localStorage.getItem("access_token");
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }
  return headers;
}

function handleResponseError(response, data) {
  if (response.status === 401) {
    // Clear local storage and let the AuthContext/ProtectedRoute handle the redirect
    localStorage.removeItem("access_token");
    window.dispatchEvent(new Event("auth-expired"));
  }
  throw new Error(data.detail || data.error || `Request failed with status ${response.status}`);
}

/**
 * Generic POST request handler for the API
 * @param {string} path - The API endpoint path
 * @param {object} payload - The JSON payload to send
 * @returns {Promise<any>}
 */
export async function postJson(path, payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1${path}`, {
    method: "POST",
    headers: getAuthHeaders(),
    body: JSON.stringify(payload)
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    handleResponseError(response, data);
  }

  return data;
}

/**
 * Login function (OAuth2 form-data)
 */
export async function loginUser(email, password) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/api/v1/login/access-token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: formData
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || "Login failed");
  }

  return data; // { access_token: "...", token_type: "bearer" }
}

export { API_BASE_URL };
