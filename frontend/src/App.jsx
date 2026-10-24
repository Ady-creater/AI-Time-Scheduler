import { useState } from "react";
import ProfileForm from "./components/ProfileForm.jsx";
import HealthCard from "./components/HealthCard.jsx";
import ScheduleTimeline from "./components/ScheduleTimeline.jsx";
import ModifyBar from "./components/ModifyBar.jsx";
import { detectHealth } from "./health.js";
import { generateSchedule, reviseSchedule } from "./api.js";

// Stage mirrors where the LangGraph agent currently is:
// "profile" -> user_profile_node / detect_health
// "schedule" -> create_schedule_node has returned a schedule
const STAGES = { PROFILE: "profile", SCHEDULE: "schedule" };

export default function App() {
  const [stage, setStage] = useState(STAGES.PROFILE);
  const [profile, setProfile] = useState(null);
  const [health, setHealth] = useState({ bmi: null, status: null });
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleProfileSubmit(submittedProfile) {
    setError(null);
    setLoading(true);
    const computedHealth = detectHealth(
      submittedProfile.height,
      submittedProfile.weight
    );
    setProfile(submittedProfile);
    setHealth(computedHealth);

    try {
      const result = await generateSchedule(submittedProfile, computedHealth);
      setSchedule(result);
      setStage(STAGES.SCHEDULE);
    } catch (err) {
      setError(
        `Couldn't reach the scheduling agent. Is the backend running? (${err.message})`
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleModify(message) {
    setError(null);
    setLoading(true);
    try {
      const updated = await reviseSchedule(message, schedule);
      setSchedule(updated);
    } catch (err) {
      setError(`Couldn't apply that change. (${err.message})`);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="page">
      <header className="page__header">
        <p className="page__eyebrow">A day, planned once, kept for 21</p>
        <h1>Daybook</h1>
      </header>

      {error && <div className="banner banner--error">{error}</div>}

      {stage === STAGES.PROFILE && (
        <section className="panel">
          <ProfileForm onSubmit={handleProfileSubmit} submitting={loading} />
        </section>
      )}

      {stage === STAGES.SCHEDULE && (
        <section className="panel panel--wide">
          <HealthCard bmi={health.bmi} status={health.status} />
          {loading && schedule.length === 0 ? (
            <p className="loading-text">Drafting your day…</p>
          ) : (
            <ScheduleTimeline schedule={schedule} />
          )}
          <ModifyBar onSubmit={handleModify} submitting={loading} />
        </section>
      )}
    </div>
  );
}
