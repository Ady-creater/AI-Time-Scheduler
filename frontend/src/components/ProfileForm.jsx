import { useState } from "react";

const emptyProfile = {
  wakeup_time: "",
  sleep_time: "",
  profession: "student",
  class_time: "",
  work_time: "",
  age: "",
  height: "",
  weight: "",
  priorities: "",
};

export default function ProfileForm({ onSubmit, submitting }) {
  const [profile, setProfile] = useState(emptyProfile);

  const set = (field) => (e) =>
    setProfile((p) => ({ ...p, [field]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      wakeup_time: profile.wakeup_time,
      sleep_time: profile.sleep_time,
      profession: profile.profession,
      class_time: profile.profession === "student" ? profile.class_time : "",
      work_time: profile.profession !== "student" ? profile.work_time : "",
      age: Number(profile.age),
      height: Number(profile.height),
      weight: Number(profile.weight),
      priorities: profile.priorities
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean),
    });
  };

  return (
    <form className="profile-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label className="field">
          <span>Wake up at</span>
          <input
            type="time"
            required
            value={profile.wakeup_time}
            onChange={set("wakeup_time")}
          />
        </label>
        <label className="field">
          <span>Sleep at</span>
          <input
            type="time"
            required
            value={profile.sleep_time}
            onChange={set("sleep_time")}
          />
        </label>
      </div>

      <label className="field">
        <span>Profession</span>
        <select value={profile.profession} onChange={set("profession")}>
          <option value="student">Student</option>
          <option value="working">Working professional</option>
        </select>
      </label>

      {profile.profession === "student" ? (
        <label className="field">
          <span>College / school hours</span>
          <input
            type="text"
            placeholder="e.g. 9:00 AM – 3:30 PM"
            required
            value={profile.class_time}
            onChange={set("class_time")}
          />
        </label>
      ) : (
        <label className="field">
          <span>Working hours</span>
          <input
            type="text"
            placeholder="e.g. 10:00 AM – 6:00 PM"
            required
            value={profile.work_time}
            onChange={set("work_time")}
          />
        </label>
      )}

      <div className="form-row form-row--three">
        <label className="field">
          <span>Age</span>
          <input
            type="number"
            min="1"
            required
            value={profile.age}
            onChange={set("age")}
          />
        </label>
        <label className="field">
          <span>Height (cm)</span>
          <input
            type="number"
            min="1"
            required
            value={profile.height}
            onChange={set("height")}
          />
        </label>
        <label className="field">
          <span>Weight (kg)</span>
          <input
            type="number"
            min="1"
            required
            value={profile.weight}
            onChange={set("weight")}
          />
        </label>
      </div>

      <label className="field">
        <span>Priorities (comma separated)</span>
        <input
          type="text"
          placeholder="e.g. fitness, deep work, family time"
          required
          value={profile.priorities}
          onChange={set("priorities")}
        />
      </label>

      <button type="submit" className="btn-primary" disabled={submitting}>
        {submitting ? "Building your day…" : "Build my schedule"}
      </button>
    </form>
  );
}
