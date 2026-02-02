import { useState } from "react";
import { Link } from "react-router-dom";
import { forgotPassword } from "../api/auth";
import InputField from "../components/InputFields";
import "../styles/auth.css";

const ForgotPassword = () => {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (name, value) => {
    setEmail(value);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");
    setError("");

    if (!email) {
      setError("Please enter your email");
      setLoading(false);
      return;
    }

    try {
      const res = await forgotPassword(email);
      setMessage(res.message);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h2>Forgot Password</h2>
        <p style={{ textAlign: "center", color: "#6b7280", marginBottom: "24px" }}>
          Enter your registered email to receive a password reset link
        </p>

        <form onSubmit={handleSubmit}>
          <InputField
            label="Email"
            name="email"
            type="email"
            value={email}
            onChange={handleChange}
            error={error}
            placeholder="Enter your email"
          />

          <button className="auth-button" type="submit" disabled={loading}>
            {loading ? "Sending..." : "Send Reset Link"}
          </button>
        </form>

        {message && (
          <div className="success-message" style={{ marginTop: "16px" }}>
            {message}
          </div>
        )}

        <div className="auth-link" style={{ marginTop: "20px" }}>
          Remember your password? <Link to="/login">Login</Link>
        </div>
      </div>
    </div>
  );
};

export default ForgotPassword;
