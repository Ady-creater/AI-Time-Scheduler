// Mirrors the detect_health node in agent_logic.py: same BMI thresholds,
// same rounding, computed client-side so the read is instant.
export function detectHealth(heightCm, weightKg) {
  if (!heightCm || !weightKg) {
    return { bmi: null, status: null };
  }
  const bmi = weightKg / Math.pow(heightCm / 100, 2);
  let status;
  if (bmi < 18.5) status = "underweight";
  else if (bmi < 25) status = "normal weight";
  else if (bmi < 30) status = "overweight";
  else status = "obese";
  return { bmi: Math.round(bmi * 100) / 100, status };
}
