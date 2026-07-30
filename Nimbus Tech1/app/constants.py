# app/constants.py

VALID_PRIORITIES = {"Low", "Medium", "High"}

VALID_STATUSES = {
    "Open",
    "In Progress",
    "Closed"
}

# SLA thresholds in hours
SLA_HOURS = {
    "High": 24,
    "Medium": 48,
    "Low": 72
}

# Priority score mapping
PRIORITY_SCORE = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}

# Maximum percentage of invalid rows allowed
MAX_INVALID_PERCENTAGE = 10