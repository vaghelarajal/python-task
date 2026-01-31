const API_URL = "http://127.0.0.1:8000";

export const signupUser = async (data) => {
  const response = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw result;
  }

  return result;
};
