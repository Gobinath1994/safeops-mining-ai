import datetime

def log_action(frame_id, violation_type, action):
    """
    Logs a safety-related action with timestamp and context.

    Args:
        frame_id (str): Identifier of the frame where the violation occurred.
        violation_type (str): Type of safety violation detected.
        action (str): The action taken in response to the violation.
    
    Behavior:
        - Appends a formatted log entry to 'logs.txt'
        - Prints the same entry to the console
    """
    # Format current timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construct the log line with metadata
    log_line = f"[{timestamp}] [Frame {frame_id}] [{violation_type}] {action}"
    
    # Write the log line to the file
    with open("logs.txt", "a") as log:
        log.write(log_line + "\n")
    
    # Print to console for real-time feedback
    print(f"[LOG] {log_line}")