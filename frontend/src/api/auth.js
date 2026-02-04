const API_URL = "http://127.0.0.1:8000";

// api call pattern 
export const signupUser = async (data) => {
  // http req.
  const response = await fetch(`${API_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),  // convert js obj to json str
  });

  const result = await response.json();

  if (!response.ok) {
    throw { response: { data: result } };
  }

  return result;
};

export const loginUser = async (data) => {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw { response: { data: result } };
  }

  return result;
};

export const forgotPassword = async (email) => {
  const response = await fetch(`${API_URL}/auth/forgot-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email }),
  });

  const result = await response.json();

  if (!response.ok) {
    throw { response: { data: result } };
  }

  return result;
};

export const resetPassword = async (token, newPassword) => {
  const response = await fetch(`${API_URL}/auth/reset-password`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ token, new_password: newPassword }),
  });

  const result = await response.json();

  if (!response.ok) {
    throw { response: { data: result } };
  }

  return result;
};

export const updateProfile = async (data) => {
  const response = await fetch(`${API_URL}/auth/profile`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  const result = await response.json();

  if (!response.ok) {
    throw { response: { data: result } };
  }

  return result;
};
