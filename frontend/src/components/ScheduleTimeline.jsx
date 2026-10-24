export default function ScheduleTimeline({ schedule }) {
  if (!schedule || schedule.length === 0) return null;

  return (
    <div className="timeline">
      {schedule.map((item, i) => (
        <div className="timeline__row" key={`${item.task}-${i}`}>
          <div className="timeline__time">
            <span>{item.start_time}</span>
            <span className="timeline__dash">–</span>
            <span>{item.end_time}</span>
          </div>
          <div className="timeline__rail">
            <span className="timeline__dot" />
            {i < schedule.length - 1 && <span className="timeline__line" />}
          </div>
          <div className="timeline__content">
            <div className="timeline__task-row">
              <h3>{item.task}</h3>
              {item.duration && (
                <span className="timeline__duration">{item.duration}</span>
              )}
            </div>
            {item.task_suggestion && (
              <p className="timeline__suggestion">{item.task_suggestion}</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
