import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import InputField from "../components/InputFields";
import { loginUser } from "../api/auth";
import "../styles/auth.css";

const Login = () => {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (name, value) => {
    setForm({ ...form, [name]: value });
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrors({});

    if (!form.email || !form.password) {
      setErrors({ api: "Please fill in all fields" });
      return;
    }

    setLoading(true);
    try {
      const res = await loginUser(form);

      localStorage.setItem("token", res.access_token);
      localStorage.setItem("user", JSON.stringify(res.user));

      navigate("/dashboard");
    } catch (err) {
      setErrors({
        api: err.response?.data?.detail || "Login failed",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Login</h2>
        
        {errors.api && <div className="error-message">{errors.api}</div>}

        <InputField
          label="Email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          error={errors.email}
          placeholder="Enter your email"
        />

        <InputField
          label="Password"
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          error={errors.password}
          placeholder="Enter your password"
        />

        <button type="submit" className="auth-button" disabled={loading}>
          {loading ? "Logging in..." : "Login"}
        </button>

        <div className="auth-link">
          <Link to="/forgot-password">Forgot Password?</Link>
        </div>

        <div className="auth-link">
          Don't have an account? <Link to="/signup">Sign Up</Link>
        </div>
      </form>
    </div>
  );
};

export default Login;