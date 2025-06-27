import yagmail  # For sending email alerts
from utils.logger import log_action  # Custom logger for recording actions

# 🎯 Centralized mapping of violation types to standard response actions
VIOLATION_ACTIONS = {
    "no_helmet": "Send alert to site supervisor: Worker without helmet.",
    "too_close_to_excavator": "Trigger proximity warning system: Worker too close to machinery.",
    "fatigue_posture": "Recommend break: Worker shows fatigue posture.",
    "trip_hazard": "Cordon off area and remove trip hazard.",
    "no_safety_vest": "Remind worker to wear high-visibility vest.",
    "obstructed_exit": "Clear emergency exit path immediately and inform supervisor.",
    "unsafe_manual_handling": "Assess lifting posture and retrain worker on manual handling protocols."
}

def send_email_alert(frame_id, summary):
    """
    Send an email alert to the safety supervisor.

    Args:
        frame_id (str): The frame identifier where the violation occurred.
        summary (str): Description of the issue or action needed.
    """
    try:
        yag = yagmail.SMTP("youremail@gmail.com", "app password")  # Use App Password, not Gmail password
        subject = f"🚨 Critical Safety Alert – Frame {frame_id}"
        body = f"Attention Supervisor,\n\n{summary}\n\nPlease take immediate action."
        yag.send("safety.officer@gmail.com", subject, body)
        print("[Email] Alert sent.")
    except Exception as e:
        print(f"[Email ERROR] {e}")

def notify_team(frame_id, violation_type):
    """
    Determine the appropriate action for a given violation and optionally trigger an email.

    Args:
        frame_id (str): The identifier for the frame where the issue occurred.
        violation_type (str): Type of safety violation.

    Returns:
        str: The action that was taken or logged.
    """
    # Get the predefined response or fallback to generic log message
    action = VIOLATION_ACTIONS.get(
        violation_type,
        f"Unknown violation '{violation_type}' detected. Log for review."
    )

    # Trigger email for critical or policy-violating events
    if violation_type in ["no_helmet", "obstructed_exit", "trip_hazard", "no_safety_vest"]:
        send_email_alert(frame_id, action)

    # Log the action regardless of email
    log_action(frame_id, violation_type, action)
    return action

def handle_notifications(frame_id, detections):
    """
    Process a list of detections for a frame and trigger alerts or logs.

    Args:
        frame_id (str): Frame being analyzed.
        detections (list): List of dicts with detected violations.

    Returns:
        list: Actions taken for each violation.
    """
    responses = []
    for det in detections:
        violation = det["type"]
        response = notify_team(frame_id, violation)
        responses.append(response)
    return responses