import requests   # For making HTTP POST requests to the LLM API
import re         # For regex-based response cleaning
import time       # For retry delays
import json       # For parsing and writing JSON

# LLM API configuration
LLM_API_URL = "http://192.168.0.14:1234/v1/chat/completions"
LLM_MODEL = "mistral-7b-instruct-v0.2"

def clean_llm_response(text):
    """
    Remove backtick-wrapped code block markers like ```json from LLM response.
    """
    return re.sub(r"```(json)?", "", text).strip()

def safe_llm_request(payload, retries=2, delay=2):
    """
    Send a POST request to the LLM API with retry logic.

    Args:
        payload (dict): The request JSON body.
        retries (int): Number of retry attempts on failure.
        delay (int): Seconds to wait between retries.

    Returns:
        dict or None: Parsed JSON response or None if all attempts fail.
    """
    for attempt in range(retries):
        try:
            response = requests.post(LLM_API_URL, json=payload, timeout=20)
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[LLM ERROR] Attempt {attempt+1} failed: {e}")
            time.sleep(delay)
    return None

def ask_llm_reasoning(frame_id, detections, location="unknown area", shift="day shift"):
    """
    Ask the LLM whether a set of safety violations requires escalation.

    Args:
        frame_id (str): The identifier for the frame being processed.
        detections (list): List of detected violations (as dicts).
        location (str): The location context (e.g., "loading zone").
        shift (str): The time of shift (e.g., "night shift").

    Returns:
        str: A stringified JSON object containing escalation decisions.
    """
    # Build prompt dynamically
    prompt = f"""
You are a safety compliance assistant.

Frame ID: {frame_id}
Location: {location}
Shift: {shift}
Violations detected: {[d['type'] for d in detections]}

Based on safety protocols in mining and construction sites, analyze the violations and decide:

Respond with a VALID JSON object ONLY (no markdown, no explanation):
{{
  "escalate": true or false,
  "notify_roles": ["Safety Officer", "Supervisor"],
  "shutdown_required": true or false,
  "summary": "Brief one-sentence explanation of the issue in frame {frame_id} at {location} during {shift}"
}}
"""

    try:
        # Submit the prompt via safe request
        response = safe_llm_request({
            "model": LLM_MODEL,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a JSON-only safety analysis agent. Always return strict JSON. No Markdown or extra text."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3,
            "max_tokens": 256
        })

        # Extract and clean response
        content = response['choices'][0]['message']['content']
        content_cleaned = clean_llm_response(content).replace("'", '"')

        # Parse into JSON
        parsed_json = json.loads(content_cleaned)

        # Log response to file
        with open("llm_logs.txt", "a") as f:
            f.write(f"[Frame {frame_id}]\n{json.dumps(parsed_json, indent=2)}\n\n")

        return json.dumps(parsed_json)

    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "LLM failed to respond."

def ask_llm_action_plan(frame_id, violation_type):
    """
    Ask LLM to generate a site supervisor's step-by-step action plan.

    Args:
        frame_id (str): Frame identifier.
        violation_type (str): Type of safety violation.

    Returns:
        str: Text content of the action plan.
    """
    prompt = f"""
Frame ID: {frame_id}
Violation type: {violation_type}

Suggest a step-by-step action plan that a site supervisor should follow to address this violation.
"""
    try:
        # Request from LLM
        response = requests.post(
            url=LLM_API_URL,
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "You're an expert in industrial safety protocols."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 300
            },
            timeout=120
        )
        plan = response.json()['choices'][0]['message']['content']
        plan = clean_llm_response(plan)

        # Save to file
        with open("action_plan.txt", "a") as f:
            f.write(f"[Frame {frame_id}]\n{plan}\n\n")

        return plan
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "LLM failed to generate action plan."

def ask_llm_policy_recommendation(frame_id, violation_type):
    """
    Ask LLM for training, policy, or checklist recommendations to prevent violations.

    Args:
        frame_id (str): Frame identifier.
        violation_type (str): Type of violation.

    Returns:
        str: Text of policy/training suggestions.
    """
    prompt = f"""
Frame ID: {frame_id}
Violation type: {violation_type}

What training, checklist, or policy changes could prevent this type of violation in the future?
"""
    try:
        # Request from LLM
        response = requests.post(
            url=LLM_API_URL,
            json={
                "model": LLM_MODEL,
                "messages": [
                    {"role": "system", "content": "You're a safety training expert. Respond clearly without Markdown or bullets."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.5,
                "max_tokens": 300
            },
            timeout=120
        )
        rec = response.json()['choices'][0]['message']['content']
        rec = clean_llm_response(rec)

        # Save to file
        with open("policy_recommendations.txt", "a") as f:
            f.write(f"[Frame {frame_id}]\n{rec}\n\n")

        return rec
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return "LLM failed to suggest policy."