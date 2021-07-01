def score_grade(score):
  if score <= 10 and score >= 8:
    return 'A'
  elif score < 8 and score >= 6.5:
    return 'B'
  elif score < 6.5 and score >= 5:
    return 'C'
  elif score >= 0 and score < 5:
    return 'D'
  else:
    return "Invalid Score"