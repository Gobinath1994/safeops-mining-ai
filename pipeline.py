import json
from agents.notify_agent import handle_notifications, send_email_alert
from agents.llm_agent import (
    ask_llm_reasoning,
    ask_llm_action_plan,
    ask_llm_policy_recommendation
)
from utils.logger import log_action

def run_pipeline():
    """
    Main inference pipeline to simulate real-time safety violation handling.

    Steps:
    1. Load simulated detection data from JSON.
    2. Loop through each frame, and for each detection:
       - Trigger notification logic.
       - Log actions taken.
    3. Ask the LLM for escalation decision + reasoning.
    4. Ask the LLM for action plans and policy suggestions.
    5. Write LLM output to corresponding log files.

    Files used:
        - Input:  data/dummy_detections.json
        - Output: llm_logs.txt, action_plan.txt, policy_recommendations.txt
    """
    try:
        # Load detection results from JSON file
        with open("data/dummy_detections.json") as f:
            frames = json.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot read detection data: {e}")
        return

    # Clean previous logs before rerunning
    open("llm_logs.txt", "w").close()
    open("action_plan.txt", "w").close()
    open("policy_recommendations.txt", "w").close()

    # Process each frame
    for frame in frames:
        frame_id = frame["frame_id"]
        detections = frame["detections"]

        print(f"\n🔍 Processing Frame: {frame_id}")

        # Trigger notifications and log each detection
        for det in detections:
            notify_action = handle_notifications(frame_id, [det])
            for a in notify_action:
                log_action(frame_id, det["type"], a)
                print(f"[ACTION] {a}")

        # Ask LLM only if the frame has violations
        if detections:
            # Add basic contextual info (stubbed — replace with real sensor/site data later)
            location = "near blast zone" if "005" in frame_id else "loading area"
            shift = "night shift" if "night" in frame_id else "day shift"

            print("🧠 Asking LLM for escalation reasoning...")
            llm_response = ask_llm_reasoning(frame_id, detections, location=location, shift=shift)

            # Log and parse valid LLM responses
            if "LLM failed" not in llm_response:
                with open("llm_logs.txt", "a") as f:
                    f.write(f"[Frame {frame_id}]\n{llm_response}\n\n")
                print(f"[LLM] Frame {frame_id} Reasoning:\n{llm_response}")

                try:
                    # Parse LLM JSON safely (convert single quotes just in case)
                    parsed = json.loads(llm_response.replace("'", '"'))
                    if parsed.get("escalate", False):
                        summary = parsed.get("summary", "Violation detected.")
                        send_email_alert(frame_id, summary)
                except Exception as e:
                    print(f"[PARSE ERROR] Couldn't parse LLM JSON: {e}")
            else:
                print(f"[LLM] Frame {frame_id}: Failed to get reasoning.")

            # Use only first violation type for LLM action plan & policy suggestion
            violation_type = detections[0]["type"]

            print("🛠️ Generating Action Plan...")
            ask_llm_action_plan(frame_id, violation_type)

            print("📋 Suggesting Policy Recommendations...")
            ask_llm_policy_recommendation(frame_id, violation_type)

# Entry point for script execution
if __name__ == "__main__":
    run_pipeline()