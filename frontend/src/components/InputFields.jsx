const InputField = ({ label, type, value, onChange, error }) => {
  return (
    <div className="input-group">
      <label className="input-label">{label}</label>

      <input
        type={type}
        value={value}
        onChange={onChange}
        className="input-control"
      />

      {error && <p className="error-text">{error}</p>}
    </div>
  );
};

export default InputField;
