import { useState } from "react";
import InputField from "../components/InputFields";
import { signupUser } from "../api/auth";
import "../styles/auth.css";

const Signup = () => {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "",
    confirm_password: "",
  });

  const [errors, setErrors] = useState({});
  const [success, setSuccess] = useState("");

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


  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSuccess("");

    if (!validate()) return;

    try {
      const res = await signupUser(form);
      setSuccess(res.message);
      setForm({
        username: "",
        email: "",
        password: "",
        confirm_password: "",
      });
    } 
    catch (err) {
  const message =
    err.response?.data?.detail ||
    err.response?.data?.message ||
    "Signup failed";

  setErrors({ api: message });
}

  };

  return (
  <div className="auth-wrapper">
    <form className="auth-card" onSubmit={handleSubmit}>
      <h2>Create Account</h2>
      <p className="subtitle">Sign up to continue</p>

        <InputField
          label="Username"
          type="text"
          value={form.username}
          onChange={(e) => handleChange({ ...e, target: { ...e.target, name: "username" } })}
          error={errors.username}
        />

        <InputField
          label="Email"
          type="email"
          value={form.email}
          onChange={(e) => handleChange({ ...e, target: { ...e.target, name: "email" } })}
          error={errors.email}
        />

        <InputField
          label="Password"
          type="password"
          value={form.password}
          onChange={(e) => handleChange({ ...e, target: { ...e.target, name: "password" } })}
          error={errors.password}
        />

        <InputField
          label="Confirm Password"
          type="password"
          value={form.confirm_password}
          onChange={(e) =>
            handleChange({ ...e, target: { ...e.target, name: "confirm_password" } })
          }
          error={errors.confirm_password}
        />

        {errors.api && <p className="error-text">{errors.api}</p>}
      {success && <p className="success-text">{success}</p>}

      <button className="primary-btn" type="submit">
        Sign Up
      </button>
    </form>
  </div>
);
};

export default Signup;
