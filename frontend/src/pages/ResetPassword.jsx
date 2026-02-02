import { useState, useEffect } from "react";
import { useSearchParams, useNavigate, Link } from "react-router-dom";
import { resetPassword } from "../api/auth";
import InputField from "../components/InputFields";
import "../styles/auth.css";

const ResetPassword = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  const token = searchParams.get("token");
  const [form, setForm] = useState({
    password: "",
    confirmPassword: "",
  });
  const [errors, setErrors] = useState({});
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token) {
      setErrors({ token: "Invalid or missing reset token." });
    }
  }, [token]);

  const handleChange = (name, value) => {
    setForm({ ...form, [name]: value });
    // Clear errors when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const validate = () => {
    let newErrors = {};

    if (form.password.length < 6) {
      newErrors.password = "Password must be at least 6 characters";
    }

    if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validate()) return;

    setLoading(true);
    setMessage("");
    setErrors({});

    try {
      const res = await resetPassword(token, form.password);
      setMessage(res.message + " Redirecting to login...");

      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setErrors({
        api: err.response?.data?.detail || "Reset failed or token expired",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Reset Password</h2>
        <p style={{ textAlign: "center", color: "#6b7280", marginBottom: "24px" }}>
          Create a new secure password for your account
        </p>

        {errors.token && (
          <div className="error-message" style={{ marginBottom: "16px" }}>
            {errors.token}
          </div>
        )}

        {errors.api && (
          <div className="error-message" style={{ marginBottom: "16px" }}>
            {errors.api}
          </div>
        )}

        {message && (
          <div className="success-message" style={{ marginBottom: "16px" }}>
            {message}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <InputField
            label="New Password"
            name="password"
            type="password"
            value={form.password}
            onChange={handleChange}
            error={errors.password}
            placeholder="Enter new password"
          />

          <InputField
            label="Confirm Password"
            name="confirmPassword"
            type="password"
            value={form.confirmPassword}
            onChange={handleChange}
            error={errors.confirmPassword}
            placeholder="Confirm new password"
          />

          <button
            className="auth-button"
            type="submit"
            disabled={loading || !token || !!errors.token}
          >
            {loading ? "Resetting..." : "Reset Password"}
          </button>
        </form>

        <div className="auth-link" style={{ marginTop: "20px" }}>
          Remember your password? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
};

export default ResetPassword;
