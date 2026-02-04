import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import InputField from "../components/InputFields";
import { signupUser } from "../api/auth";
import "../styles/auth.css";

const Signup = () => {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  const validateField = (name, value) => {
    let error = "";
    const nameRegex = /^[A-Za-z]+$/;

    switch (name) {
      case "username":
        if (value.length < 3) {
          error = "Username must be at least 3 characters";
        } else if (!nameRegex.test(value)) {
          error = "Username must contain only letters and no whitespaces";
        }
        break;
      case "email":
        if (!value.includes("@")) {
          error = "Enter a valid email";
        }
        break;
      case "password":
        if (value.length < 6) {
          error = "Password must be at least 6 characters";
        }
        break;
      case "confirm_password":
        if (value !== form.password) {
          error = "Passwords do not match";
        }
        break;
    }

    setErrors(prev => ({ ...prev, [name]: error }));
    return error === "";
  };

  const validate = () => {
    let newErrors = {};

    const nameRegex = /^[A-Za-z]+$/;

    if (form.username.length < 3)
      newErrors.username = "Username must be at least 3 characters";
    else if (!nameRegex.test(form.username))
      newErrors.username = "Username must contain only letters and no whitespaces";

    if (!form.email.includes("@"))
      newErrors.email = "Enter a valid email";

    if (form.password.length < 6)
      newErrors.password = "Password must be at least 6 characters";

    if (form.password !== form.confirm_password)
      newErrors.confirm_password = "Passwords do not match";

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (name, value) => {
    setForm({ ...form, [name]: value });
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors({ ...errors, [name]: "" });
    }
  };

  const handleBlur = (name, value) => {
    validateField(name, value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess("");
    setErrors({});

    if (!validate()) return;

    setLoading(true);
    try {
      await signupUser(form);
      setSuccess("Account created successfully!");
      setTimeout(() => {
        navigate("/login");
      }, 2000);
    } catch (err) {
      setErrors({
        api: err.response?.data?.detail || "Signup failed",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <form className="auth-card" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        
        {success && <div className="success-message">{success}</div>}
        {errors.api && <div className="error-message">{errors.api}</div>}

        <InputField
          label="Username"
          name="username"
          type="text"
          value={form.username}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.username}
          placeholder="Enter your username"
        />

        <InputField
          label="Email"
          name="email"
          type="email"
          value={form.email}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.email}
          placeholder="Enter your email"
        />

        <InputField
          label="Password"
          name="password"
          type="password"
          value={form.password}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.password}
          placeholder="Enter your password"
        />

        <InputField
          label="Confirm Password"
          name="confirm_password"
          type="password"
          value={form.confirm_password}
          onChange={handleChange}
          onBlur={handleBlur}
          error={errors.confirm_password}
          placeholder="Confirm your password"
        />

        <button type="submit" className="auth-button" disabled={loading}>
          {loading ? "Creating Account..." : "Sign Up"}
        </button>

        <div className="auth-link">
          Already have an account? <Link to="/login">Login</Link>
        </div>
      </form>
    </div>
  );
};

export default Signup;