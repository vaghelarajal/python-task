import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { updateProfile } from "../api/auth";

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const [showProfile, setShowProfile] = useState(false);
  const [editMode, setEditMode] = useState(false);
  const [profileForm, setProfileForm] = useState({
    address: "",
    gender: "",
    age: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!user) {
      navigate("/login");
      return;
    }
    
    setProfileForm({
      address: user.address || "",
      gender: user.gender || "",
      age: user.age || "",
    });
  }, [user, navigate]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/login");
  };

  const handleProfileUpdate = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage("");

    try {
      const response = await updateProfile({
        email: user.email,
        ...profileForm,
        age: profileForm.age ? parseInt(profileForm.age) : null,
      });

      // Update local storage and state
      const updatedUser = response.user;
      localStorage.setItem("user", JSON.stringify(updatedUser));
      setUser(updatedUser);
      setEditMode(false);
      setMessage("Profile updated successfully!");
      
      setTimeout(() => setMessage(""), 3000);
    } catch (err) {
      setMessage(err.response?.data?.detail || "Failed to update profile");
    } finally {
      setLoading(false);
    }
  };

  if (!user) return null;

  return (
    <div style={{ minHeight: "100vh", background: "#f8fafc" }}>
      {/* Header */}
      <header
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          padding: "15px 40px",
          background: "#0f172a",
          color: "#fff",
          boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
        }}
      >
        <h3 style={{ margin: 0 }}>Dashboard</h3>
        <div style={{ position: "relative" }}>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              cursor: "pointer",
              padding: "8px 16px",
              borderRadius: "8px",
              background: showProfile ? "#1e293b" : "transparent",
            }}
            onClick={() => setShowProfile(!showProfile)}
          >
            <div
              style={{
                width: "32px",
                height: "32px",
                borderRadius: "50%",
                background: "#3b82f6",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                marginRight: "8px",
                fontSize: "14px",
                fontWeight: "bold",
              }}
            >
              {user.username.charAt(0).toUpperCase()}
            </div>
            <span>Profile</span>
          </div>

          {/* Profile Dropdown */}
          {showProfile && (
            <div
              style={{
                position: "absolute",
                top: "100%",
                right: 0,
                background: "#fff",
                color: "#000",
                borderRadius: "8px",
                boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
                padding: "20px",
                minWidth: "300px",
                zIndex: 1000,
                marginTop: "8px",
              }}
            >
              {message && (
                <div
                  style={{
                    padding: "8px 12px",
                    borderRadius: "4px",
                    marginBottom: "16px",
                    background: message.includes("success") ? "#dcfce7" : "#fef2f2",
                    color: message.includes("success") ? "#166534" : "#dc2626",
                    fontSize: "14px",
                  }}
                >
                  {message}
                </div>
              )}

              {!editMode ? (
                <div>
                  <div style={{ marginBottom: "16px" }}>
                    <strong>Username:</strong> {user.username}
                  </div>
                  <div style={{ marginBottom: "16px" }}>
                    <strong>Email:</strong> {user.email}
                  </div>
                  <div style={{ marginBottom: "16px" }}>
                    <strong>Address:</strong> {user.address || "Not provided"}
                  </div>
                  <div style={{ marginBottom: "16px" }}>
                    <strong>Gender:</strong> {user.gender || "Not provided"}
                  </div>
                  <div style={{ marginBottom: "20px" }}>
                    <strong>Age:</strong> {user.age || "Not provided"}
                  </div>
                  
                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      onClick={() => setEditMode(true)}
                      style={{
                        padding: "8px 16px",
                        background: "#3b82f6",
                        color: "#fff",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "14px",
                      }}
                    >
                      Edit Profile
                    </button>
                    <button
                      onClick={handleLogout}
                      style={{
                        padding: "8px 16px",
                        background: "#ef4444",
                        color: "#fff",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "14px",
                      }}
                    >
                      Logout
                    </button>
                  </div>
                </div>
              ) : (
                <form onSubmit={handleProfileUpdate}>
                  <div style={{ marginBottom: "12px" }}>
                    <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>
                      Address:
                    </label>
                    <input
                      type="text"
                      value={profileForm.address}
                      onChange={(e) => setProfileForm({ ...profileForm, address: e.target.value })}
                      style={{
                        width: "100%",
                        padding: "8px",
                        border: "1px solid #d1d5db",
                        borderRadius: "4px",
                        fontSize: "14px",
                      }}
                      placeholder="Enter your address"
                    />
                  </div>

                  <div style={{ marginBottom: "12px" }}>
                    <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>
                      Gender:
                    </label>
                    <select
                      value={profileForm.gender}
                      onChange={(e) => setProfileForm({ ...profileForm, gender: e.target.value })}
                      style={{
                        width: "100%",
                        padding: "8px",
                        border: "1px solid #d1d5db",
                        borderRadius: "4px",
                        fontSize: "14px",
                      }}
                    >
                      <option value="">Select gender</option>
                      <option value="Male">Male</option>
                      <option value="Female">Female</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>

                  <div style={{ marginBottom: "16px" }}>
                    <label style={{ display: "block", marginBottom: "4px", fontSize: "14px" }}>
                      Age:
                    </label>
                    <input
                      type="number"
                      value={profileForm.age}
                      onChange={(e) => setProfileForm({ ...profileForm, age: e.target.value })}
                      style={{
                        width: "100%",
                        padding: "8px",
                        border: "1px solid #d1d5db",
                        borderRadius: "4px",
                        fontSize: "14px",
                      }}
                      placeholder="Enter your age"
                      min="13"
                      max="100"
                    />
                  </div>

                  <div style={{ display: "flex", gap: "8px" }}>
                    <button
                      type="submit"
                      disabled={loading}
                      style={{
                        padding: "8px 16px",
                        background: "#10b981",
                        color: "#fff",
                        border: "none",
                        borderRadius: "4px",
                        cursor: loading ? "not-allowed" : "pointer",
                        fontSize: "14px",
                        opacity: loading ? 0.7 : 1,
                      }}
                    >
                      {loading ? "Saving..." : "Save"}
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditMode(false)}
                      style={{
                        padding: "8px 16px",
                        background: "#6b7280",
                        color: "#fff",
                        border: "none",
                        borderRadius: "4px",
                        cursor: "pointer",
                        fontSize: "14px",
                      }}
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              )}
            </div>
          )}
        </div>
      </header>

      {/* Hero Banner */}
      <div
        style={{
          background: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
          color: "#fff",
          padding: "80px 40px",
          textAlign: "center",
        }}
      >
        <h1 style={{ fontSize: "3rem", margin: "0 0 16px 0", fontWeight: "bold" }}>
          Hello, {user.username}!
        </h1>
        <p style={{ fontSize: "1.25rem", margin: 0, opacity: 0.9 }}>
          Welcome to your dashboard!
        </p>
      </div>
    </div>
  );
};

export default Dashboard;