const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:8000";

/**
 * Generic POST request handler for the API
 * @param {string} path - The API endpoint path
 * @param {object} payload - The JSON payload to send
 * @returns {Promise<any>}
 */
export async function postJson(path, payload) {
  const response = await fetch(`${API_BASE_URL}/api/v1${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || data.error || `Request failed with status ${response.status}`);
  }

  return data;
}

export { API_BASE_URL };
