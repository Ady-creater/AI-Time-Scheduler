export default function HealthCard({ bmi, status }) {
  if (bmi == null) return null;
  return (
    <div className="health-card">
      <div className="health-card__bmi">
        <span className="health-card__value">{bmi}</span>
        <span className="health-card__label">BMI</span>
      </div>
      <p className="health-card__status">
        Reading: <strong>{status}</strong>. Task suggestions below are
        weighted with this in mind.
      </p>
    </div>
  );
}
