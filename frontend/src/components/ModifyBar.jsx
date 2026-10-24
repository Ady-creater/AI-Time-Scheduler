import { useState } from "react";

export default function ModifyBar({ onSubmit, submitting }) {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    onSubmit(message.trim());
    setMessage("");
  };

  return (
    <form className="modify-bar" onSubmit={handleSubmit}>
      <input
        type="text"
        placeholder="e.g. move my workout to 6 PM, or delete the meeting"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button type="submit" className="btn-secondary" disabled={submitting}>
        {submitting ? "Updating…" : "Update"}
      </button>
    </form>
  );
}
