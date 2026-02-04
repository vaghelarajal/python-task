import { useState } from "react";

const InputField = ({ label, name, type, value, onChange, error, placeholder, onBlur }) => {
  const [showPassword, setShowPassword] = useState(false);
  
  const handleChange = (e) => {
    onChange(name, e.target.value);
  };

  const handleBlur = (e) => {
    if (onBlur) {
      onBlur(name, e.target.value);
    }
  };

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  const inputType = type === "password" && showPassword ? "text" : type;

  return (
    <div className="input-group">
      <label className="input-label">{label}</label>

      <div style={{ position: "relative" }}>
        <input
          name={name}
          type={inputType}
          value={value}
          onChange={handleChange}
          onBlur={handleBlur}
          className="input-control"
          placeholder={placeholder}
          style={type === "password" ? { paddingRight: "45px" } : {}}
        />

        {type === "password" && (
          <button
            type="button"
            onClick={togglePasswordVisibility}
            style={{
              position: "absolute",
              right: "12px",
              top: "50%",
              transform: "translateY(-50%)",
              background: "none",
              border: "none",
              cursor: "pointer",
              fontSize: "16px",
              color: showPassword ? "#3b82f6" : "#6b7280",
              padding: "4px",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              width: "24px",
              height: "24px",
              borderRadius: "4px",
              transition: "all 0.2s ease",
            }}
            onMouseEnter={(e) => {
              e.target.style.backgroundColor = "#f3f4f6";
            }}
            onMouseLeave={(e) => {
              e.target.style.backgroundColor = "transparent";
            }}
            aria-label={showPassword ? "Hide password" : "Show password"}
            title={showPassword ? "Hide password" : "Show password"}
          >
            {showPassword ? "🙈" : "👁️"}
          </button>
        )}
      </div>

      {error && <p className="error-text">{error}</p>}
    </div>
  );
};

export default InputField;
