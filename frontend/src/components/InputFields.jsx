const InputField = ({ label, name, type, value, onChange, error, placeholder }) => {
  const handleChange = (e) => {
    onChange(name, e.target.value);
  };

  return (
    <div className="input-group">
      <label className="input-label">{label}</label>

      <input
        name={name}
        type={type}
        value={value}
        onChange={handleChange}
        className="input-control"
        placeholder={placeholder}
      />

      {error && <p className="error-text">{error}</p>}
    </div>
  );
};

export default InputField;
